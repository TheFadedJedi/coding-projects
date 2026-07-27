#!/usr/bin/env python3
"""
Focus Timer — a standalone PyQt6 widget styled to match JediHub
(dark blue/teal theme). Drop this into JediHub's widget panel later,
or run it as its own small always-on-top window for now.

Controls:
  - Interval buttons: 15 / 20 / 25 / 30 min (sets the base time)
  - +/- buttons: nudge the current time by 1 minute (only while stopped)
  - Start -> becomes Pause / Cancel while running
  - Pause -> becomes Resume / Cancel while paused
  - When time hits 0:00, it rings (system beep x3) and flashes the display
"""

import sys
import math
import struct
import wave
import tempfile
import os
import shutil
import subprocess
from PyQt6.QtCore import Qt, QTimer
from PyQt6.QtGui import QFont
from PyQt6.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QHBoxLayout,
    QLabel, QPushButton, QSizePolicy
)

# ---- JediHub-style palette (dark blue / teal) ----
BG          = "#0d1b21"   # near-black blue background
PANEL       = "#132a33"   # slightly lighter panel
ACCENT      = "#17c3b2"   # teal accent
ACCENT_DIM  = "#0f8f83"   # dimmed teal (hover/inactive)
TEXT        = "#e6f6f4"   # off-white with a cool tint
TEXT_DIM    = "#7fa8a3"   # muted teal-grey for secondary text
DANGER      = "#e05a5a"   # for cancel

INTERVALS = [15, 20, 25, 30]  # minutes


def _generate_beep_wav(path, freq=880, duration=0.35, volume=0.6, samplerate=44100):
    """Write a short sine-wave beep to `path` as a real WAV file, with a tiny
    fade in/out so it doesn't click/pop."""
    n_samples = int(samplerate * duration)
    with wave.open(path, "w") as wf:
        wf.setnchannels(1)
        wf.setsampwidth(2)
        wf.setframerate(samplerate)
        frames = bytearray()
        for i in range(n_samples):
            t = i / samplerate
            envelope = max(0.0, min(1.0, t * 20, (duration - t) * 20))
            sample = volume * envelope * math.sin(2 * math.pi * freq * t)
            frames += struct.pack("<h", int(sample * 32767))
        wf.writeframes(bytes(frames))


def _play_wav(path):
    """Play a WAV file through whatever system audio player is available.
    Non-blocking (fire-and-forget subprocess), no extra Python deps needed."""
    for player in ("paplay", "aplay", "afplay"):
        exe = shutil.which(player)
        if exe:
            subprocess.Popen(
                [exe, path],
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL,
            )
            return True
    return False


class FocusTimer(QWidget):
    def __init__(self):
        super().__init__()
        self.total_seconds = 25 * 60
        self.remaining = self.total_seconds
        self.running = False
        self.paused = False

        self.timer = QTimer(self)
        self.timer.setInterval(1000)
        self.timer.timeout.connect(self.tick)

        self._setup_sound()
        self._build_ui()
        self._update_display()

    # ---------------------------------------------------------- sound setup
    def _setup_sound(self):
        tmp_dir = tempfile.gettempdir()
        self.beep_path = os.path.join(tmp_dir, "focus_timer_beep.wav")
        if not os.path.exists(self.beep_path):
            _generate_beep_wav(self.beep_path)
        self.has_player = any(shutil.which(p) for p in ("paplay", "aplay", "afplay"))

    # ---------------------------------------------------------- UI build
    def _build_ui(self):
        self.setWindowTitle("Focus Timer")
        self.setFixedSize(300, 260)
        self.setStyleSheet(f"background-color: {BG};")

        root = QVBoxLayout(self)
        root.setContentsMargins(18, 16, 18, 18)
        root.setSpacing(14)

        # Title
        title = QLabel("FOCUS TIMER")
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        title.setStyleSheet(f"color: {ACCENT}; letter-spacing: 2px;")
        title.setFont(QFont("Sans", 11, QFont.Weight.Bold))
        root.addWidget(title)

        # Interval selector row
        interval_row = QHBoxLayout()
        interval_row.setSpacing(6)
        self.interval_buttons = {}
        for mins in INTERVALS:
            btn = QPushButton(f"{mins}")
            btn.setFixedHeight(28)
            btn.setCursor(Qt.CursorShape.PointingHandCursor)
            btn.clicked.connect(lambda _, m=mins: self._select_interval(m))
            interval_row.addWidget(btn)
            self.interval_buttons[mins] = btn
        root.addLayout(interval_row)

        # Time display with +/- on either side
        display_row = QHBoxLayout()
        display_row.setSpacing(10)

        self.minus_btn = QPushButton("–")
        self.plus_btn = QPushButton("+")
        for b in (self.minus_btn, self.plus_btn):
            b.setFixedSize(36, 36)
            b.setCursor(Qt.CursorShape.PointingHandCursor)
            b.setStyleSheet(f"""
                QPushButton {{
                    background-color: {PANEL};
                    color: {ACCENT};
                    border: 1px solid {ACCENT_DIM};
                    border-radius: 18px;
                    font-size: 16px;
                    font-weight: bold;
                }}
                QPushButton:hover {{ background-color: {ACCENT_DIM}; color: {BG}; }}
                QPushButton:disabled {{ color: {TEXT_DIM}; border-color: {PANEL}; }}
            """)
        self.minus_btn.clicked.connect(lambda: self._nudge(-1))
        self.plus_btn.clicked.connect(lambda: self._nudge(1))

        self.display = QLabel("25:00")
        self.display.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.display.setFont(QFont("Monospace", 34, QFont.Weight.Bold))
        self.display.setStyleSheet(f"color: {TEXT};")
        self.display.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Preferred)

        display_row.addWidget(self.minus_btn)
        display_row.addWidget(self.display)
        display_row.addWidget(self.plus_btn)
        root.addLayout(display_row)

        # Action buttons row
        self.action_row = QHBoxLayout()
        self.action_row.setSpacing(8)
        root.addLayout(self.action_row)

        self.start_btn = QPushButton("Start")
        self.start_btn.setFixedHeight(36)
        self.start_btn.clicked.connect(self.start)
        self.action_row.addWidget(self.start_btn)

        self._style_idle_buttons()
        self._select_interval(25)

    # ---------------------------------------------------------- styling helpers
    def _style_idle_buttons(self):
        for mins, btn in self.interval_buttons.items():
            active = (mins * 60 == self.total_seconds) and not self.running
            btn.setStyleSheet(self._pill_style(active))
            btn.setEnabled(not self.running)
        self.minus_btn.setEnabled(not self.running)
        self.plus_btn.setEnabled(not self.running)

    def _pill_style(self, active):
        if active:
            return f"""
                QPushButton {{
                    background-color: {ACCENT}; color: {BG};
                    border: none; border-radius: 6px; font-weight: bold;
                }}
            """
        return f"""
            QPushButton {{
                background-color: {PANEL}; color: {TEXT_DIM};
                border: 1px solid {ACCENT_DIM}; border-radius: 6px;
            }}
            QPushButton:hover {{ color: {ACCENT}; border-color: {ACCENT}; }}
        """

    def _primary_btn_style(self, color=ACCENT):
        return f"""
            QPushButton {{
                background-color: {color}; color: {BG};
                border: none; border-radius: 6px; font-weight: bold; font-size: 13px;
            }}
            QPushButton:hover {{ background-color: {ACCENT_DIM}; }}
        """

    def _secondary_btn_style(self, color=DANGER):
        return f"""
            QPushButton {{
                background-color: {PANEL}; color: {color};
                border: 1px solid {color}; border-radius: 6px; font-size: 13px;
            }}
            QPushButton:hover {{ background-color: {color}; color: {BG}; }}
        """

    # ---------------------------------------------------------- interval / nudge
    def _select_interval(self, mins):
        if self.running:
            return
        self.total_seconds = mins * 60
        self.remaining = self.total_seconds
        self._style_idle_buttons()
        self._update_display()

    def _nudge(self, delta_minutes):
        if self.running:
            return
        new_total = self.total_seconds + delta_minutes * 60
        new_total = max(60, min(new_total, 180 * 60))  # clamp 1min - 3hr
        self.total_seconds = new_total
        self.remaining = new_total
        self._style_idle_buttons()
        self._update_display()

    # ---------------------------------------------------------- run controls
    def start(self):
        self.running = True
        self.paused = False
        self.timer.start()
        self._style_idle_buttons()
        self._show_running_controls()

    def pause(self):
        self.paused = True
        self.timer.stop()
        self._show_paused_controls()

    def resume(self):
        self.paused = False
        self.timer.start()
        self._show_running_controls()

    def cancel(self):
        self.running = False
        self.paused = False
        self.timer.stop()
        self.remaining = self.total_seconds
        self._style_idle_buttons()
        self._update_display()
        self._show_start_control()

    def tick(self):
        self.remaining -= 1
        self._update_display()
        if self.remaining <= 0:
            self.timer.stop()
            self.running = False
            self.paused = False
            self._ring()
            self._style_idle_buttons()
            self._show_start_control()

    # ---------------------------------------------------------- button state swaps
    def _clear_action_row(self):
        while self.action_row.count():
            item = self.action_row.takeAt(0)
            w = item.widget()
            if w:
                w.setParent(None)

    def _show_start_control(self):
        self._clear_action_row()
        self.start_btn = QPushButton("Start")
        self.start_btn.setFixedHeight(36)
        self.start_btn.setStyleSheet(self._primary_btn_style())
        self.start_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        self.start_btn.clicked.connect(self.start)
        self.action_row.addWidget(self.start_btn)

    def _show_running_controls(self):
        self._clear_action_row()
        pause_btn = QPushButton("Pause")
        cancel_btn = QPushButton("Cancel")
        for b in (pause_btn, cancel_btn):
            b.setFixedHeight(36)
            b.setCursor(Qt.CursorShape.PointingHandCursor)
        pause_btn.setStyleSheet(self._primary_btn_style())
        cancel_btn.setStyleSheet(self._secondary_btn_style())
        pause_btn.clicked.connect(self.pause)
        cancel_btn.clicked.connect(self.cancel)
        self.action_row.addWidget(pause_btn)
        self.action_row.addWidget(cancel_btn)

    def _show_paused_controls(self):
        self._clear_action_row()
        resume_btn = QPushButton("Resume")
        cancel_btn = QPushButton("Cancel")
        for b in (resume_btn, cancel_btn):
            b.setFixedHeight(36)
            b.setCursor(Qt.CursorShape.PointingHandCursor)
        resume_btn.setStyleSheet(self._primary_btn_style())
        cancel_btn.setStyleSheet(self._secondary_btn_style())
        resume_btn.clicked.connect(self.resume)
        cancel_btn.clicked.connect(self.cancel)
        self.action_row.addWidget(resume_btn)
        self.action_row.addWidget(cancel_btn)

    # ---------------------------------------------------------- display / alarm
    def _update_display(self):
        m, s = divmod(max(self.remaining, 0), 60)
        self.display.setText(f"{m:02d}:{s:02d}")

    def _ring(self):
        self.display.setText("DONE")
        self.display.setStyleSheet(f"color: {ACCENT}; font-weight: bold;")
        QTimer.singleShot(2000, lambda: self.display.setStyleSheet(f"color: {TEXT};"))
        if self.has_player:
            for i in range(3):
                QTimer.singleShot(i * 500, lambda: _play_wav(self.beep_path))
        else:
            # Fallback in case no audio player binary is found on this system
            for i in range(3):
                QTimer.singleShot(i * 400, QApplication.beep)


def main():
    app = QApplication(sys.argv)
    w = FocusTimer()
    w.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()