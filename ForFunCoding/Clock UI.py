# Digital Clock + Calendar (HUD Theme matching Task Manager UI)
# Based on Clock.py and Task Manager UI theme/panel

import tkinter as tk
from datetime import datetime
import calendar

# Set calendar to start on Sunday (same behavior as original)
calendar.setfirstweekday(calendar.SUNDAY)

# Initialize current year and month
current_year = datetime.now().year
current_month = datetime.now().month

# --- THEME (matches your Task Manager UI palette) ---
THEME = {
    "bg": "#0e1621",
    "panel_outer": "#101c2a",
    "panel_inner": "#182636",
    "stroke_dark": "#0a111a",
    "stroke_mid": "#2a3c52",
    "stroke_light": "#47647f",
    "accent": "#6fb3c8",
    "text": "#dce8f2",
    "muted": "#9fb4c6",
    "danger": "#ff5a5a",
    "ok": "#44ff99",
    "btn_bg": "#1a2a3c",
    "btn_bg_hover": "#22384f",
    "cell_bg": "#162536",
    "cell_bg_alt": "#142231",
}

def _on_hover(btn, normal_bg, hover_bg):
    btn.bind("<Enter>", lambda e: btn.configure(bg=hover_bg))
    btn.bind("<Leave>", lambda e: btn.configure(bg=normal_bg))

class HudPanel(tk.Canvas):
    """
    Same HUD panel approach as your Task Manager UI:
    - Canvas draws a sci-fi panel
    - content frame sits inside for normal Tk widgets
    """
    def __init__(self, master, width=640, height=560, padding=22, **kwargs):
        super().__init__(
            master,
            width=width,
            height=height,
            bg=THEME["bg"],
            highlightthickness=0,
            bd=0,
            **kwargs
        )
        self.padding = padding
        self._cw = width
        self._ch = height

        self.content = tk.Frame(self, bg=THEME["panel_inner"])
        self._content_window = self.create_window(
            padding, padding,
            anchor="nw",
            window=self.content,
            width=width - 2 * padding,
            height=height - 2 * padding
        )

        self.bind("<Configure>", self._redraw)
        self._redraw()

    def _redraw(self, event=None):
        w = event.width if event else self._cw
        h = event.height if event else self._ch
        self._cw, self._ch = w, h

        pad = self.padding
        inner_w = max(10, w - 2 * pad)
        inner_h = max(10, h - 2 * pad)
        self.itemconfig(self._content_window, width=inner_w, height=inner_h)

        self.delete("hud")

        # Outer panel
        self.create_rectangle(
            pad - 10, pad - 10, w - (pad - 10), h - (pad - 10),
            fill=THEME["panel_outer"],
            outline=THEME["stroke_dark"],
            width=2,
            tags="hud"
        )

        # Inner panel
        self.create_rectangle(
            pad, pad, w - pad, h - pad,
            fill=THEME["panel_inner"],
            outline=THEME["stroke_mid"],
            width=2,
            tags="hud"
        )

        # Accent top line + right tab
        self.create_line(
            pad + 16, pad + 10, w - pad - 90, pad + 10,
            fill=THEME["accent"],
            width=2,
            tags="hud"
        )
        self.create_rectangle(
            w - pad - 88, pad + 4, w - pad - 14, pad + 16,
            fill=THEME["panel_inner"],
            outline=THEME["accent"],
            width=2,
            tags="hud"
        )

        # Corner bevel hints
        corner = 18
        self.create_line(pad, pad + corner, pad, pad, pad + corner, pad,
                         fill=THEME["stroke_light"], width=2, tags="hud")
        self.create_line(w - pad - corner, pad, w - pad, pad, w - pad, pad + corner,
                         fill=THEME["stroke_light"], width=2, tags="hud")
        self.create_line(pad, h - pad - corner, pad, h - pad, pad + corner, h - pad,
                         fill=THEME["stroke_light"], width=2, tags="hud")
        self.create_line(w - pad - corner, h - pad, w - pad, h - pad, w - pad, h - pad - corner,
                         fill=THEME["stroke_light"], width=2, tags="hud")

# ---------------- Clock + Calendar logic ----------------

def update_clock():
    now = datetime.now()
    time_str = now.strftime("%I:%M:%S %p")
    date_str = now.strftime("%B %d, %Y")
    day_str = now.strftime("%A")

    time_label.config(text=time_str)
    date_label.config(text=date_str)
    day_label.config(text=day_str)

    root.after(1000, update_clock)

def prev_month():
    global current_month, current_year
    current_month -= 1
    if current_month == 0:
        current_month = 12
        current_year -= 1
    update_calendar()

def next_month():
    global current_month, current_year
    current_month += 1
    if current_month == 13:
        current_month = 1
        current_year += 1
    update_calendar()

def exit_app():
    root.destroy()  # cleanly closes the Tk window and ends the program

def update_calendar():
    month_year_label.config(text=f"{calendar.month_name[current_month]} {current_year}")
    cal = calendar.monthcalendar(current_year, current_month)
    now = datetime.now()

    for week_idx in range(6):  # fixed 6 rows for uniformity
        for day_idx in range(7):
            if week_idx < len(cal) and cal[week_idx][day_idx] != 0:
                day_num = cal[week_idx][day_idx]
                text = str(day_num)
                is_today = (day_num == now.day and current_month == now.month and current_year == now.year)
                fg_color = THEME["ok"] if is_today else THEME["accent"]
            else:
                text = ""
                fg_color = THEME["muted"]

            day_grid[week_idx][day_idx].config(text=text, fg=fg_color)

# ------------------------------ UI Construction ------------------------------

root = tk.Tk()
root.title("Digital Clock")
root.geometry("700x680")
root.minsize(640, 620)
root.configure(bg=THEME["bg"])

panel = HudPanel(root, width=700, height=620, padding=22)
panel.pack(fill=tk.BOTH, expand=True, padx=14, pady=14)

# Header section (clock)
header = tk.Frame(panel.content, bg=THEME["panel_inner"])
header.pack(fill=tk.X, padx=14, pady=(14, 6))

title = tk.Label(
    header,
    text="CLOCK",
    font=("Arial", 16, "bold"),
    fg=THEME["muted"],
    bg=THEME["panel_inner"]
)
title.pack(side=tk.LEFT)

# Time label (large)
time_label = tk.Label(
    panel.content,
    font=("Courier", 52, "bold"),
    fg=THEME["ok"],
    bg=THEME["panel_inner"]
)
time_label.pack(pady=(6, 6))

# Day of week + date
day_label = tk.Label(
    panel.content,
    font=("Arial", 20, "bold"),
    fg=THEME["accent"],
    bg=THEME["panel_inner"]
)
day_label.pack()

date_label = tk.Label(
    panel.content,
    font=("Arial", 18),
    fg=THEME["text"],
    bg=THEME["panel_inner"]
)
date_label.pack(pady=(0, 12))

# Divider line (HUD-ish)
divider = tk.Frame(panel.content, bg=THEME["stroke_mid"], height=1)
divider.pack(fill=tk.X, padx=14, pady=(4, 12))

# Calendar container
cal_container = tk.Frame(panel.content, bg=THEME["panel_inner"])
cal_container.pack(fill=tk.BOTH, expand=True, padx=14, pady=(0, 14))

# Month nav row
nav_row = tk.Frame(cal_container, bg=THEME["panel_inner"])
nav_row.pack(fill=tk.X, pady=(0, 10))

prev_button = tk.Button(
    nav_row,
    text="<",
    command=prev_month,
    font=("Arial", 14, "bold"),
    fg=THEME["text"],
    bg=THEME["btn_bg"],
    activebackground=THEME["btn_bg_hover"],
    activeforeground=THEME["text"],
    bd=0,
    highlightthickness=1,
    highlightbackground=THEME["stroke_mid"],
    highlightcolor=THEME["accent"],
    padx=14,
    pady=8
)
prev_button.pack(side=tk.LEFT)
_on_hover(prev_button, THEME["btn_bg"], THEME["btn_bg_hover"])

month_year_label = tk.Label(
    nav_row,
    font=("Arial", 16, "bold"),
    fg=THEME["text"],
    bg=THEME["panel_inner"]
)
month_year_label.pack(side=tk.LEFT, expand=True)

next_button = tk.Button(
    nav_row,
    text=">",
    command=next_month,
    font=("Arial", 14, "bold"),
    fg=THEME["text"],
    bg=THEME["btn_bg"],
    activebackground=THEME["btn_bg_hover"],
    activeforeground=THEME["text"],
    bd=0,
    highlightthickness=1,
    highlightbackground=THEME["stroke_mid"],
    highlightcolor=THEME["accent"],
    padx=14,
    pady=8
)
next_button.pack(side=tk.RIGHT)
_on_hover(next_button, THEME["btn_bg"], THEME["btn_bg_hover"])

# Calendar grid (weekday header + 6 weeks)
grid_frame = tk.Frame(cal_container, bg=THEME["panel_inner"])
grid_frame.pack()

# Make columns expand evenly (helps alignment on resize)
for c in range(7):
    grid_frame.grid_columnconfigure(c, weight=1, uniform="cal")

# --- Weekday header INSIDE the same grid as cells ---
days = ["S", "M", "T", "W", "Th", "F", "S"]
for day_idx, d in enumerate(days):
    hdr = tk.Label(
        grid_frame,
        text=d,
        font=("Arial", 11, "bold"),
        fg=THEME["muted"],
        bg=THEME["panel_inner"],
        width=4,
        pady=6
    )
    hdr.grid(row=0, column=day_idx, padx=2, pady=(0, 6), sticky="nsew")

# --- Calendar cells (6 rows x 7 cols) start at row=1 ---
day_grid = []
for week_idx in range(6):
    week = []
    for day_idx in range(7):
        bg = THEME["cell_bg"] if (week_idx + day_idx) % 2 == 0 else THEME["cell_bg_alt"]
        lbl = tk.Label(
            grid_frame,
            text="",
            font=("Arial", 12, "bold"),
            fg=THEME["accent"],
            bg=bg,
            width=4,
            height=2,
            highlightthickness=1,
            highlightbackground=THEME["stroke_mid"]
        )
        lbl.grid(row=week_idx + 1, column=day_idx, padx=2, pady=2, sticky="nsew")
        week.append(lbl)
    day_grid.append(week)

# ---------------- Exit Button (BOTTOM RIGHT, guaranteed visible) ----------------
exit_button = tk.Button(
    cal_container,
    text="Exit",
    command=exit_app,
    font=("Arial", 14, "bold"),
    fg=THEME["text"],
    bg=THEME["btn_bg"],
    activebackground=THEME["btn_bg_hover"],
    activeforeground=THEME["text"],
    bd=0,
    highlightthickness=1,
    highlightbackground=THEME["stroke_mid"],
    highlightcolor=THEME["accent"],
    padx=14,
    pady=8
)
_on_hover(exit_button, THEME["btn_bg"], THEME["btn_bg_hover"])

# Anchor inside cal_container, bottom-right corner
# Increase the negative x/y values to move it inward from the edge.
exit_button.place(relx=1.0, rely=1.0, anchor="se", x=-2, y=-2)

# Initial calendar + clock start
update_calendar()
update_clock()

root.mainloop()
