# Combined Daily Task Manager + Digital Clock/Calendar (HUD Theme)
# LAYOUT:
#   LEFT:  Clock/Calendar (top) + Goals (bottom)
#   RIGHT: Widgets Panel (top) + Reminder Goals (bottom)
#
# WIDGET PANEL FEATURES:
#   - Panel visibility toggles (Clock, Goals, Reminders)
#   - 12H / 24H clock format toggle
#   - Theme switcher (HUD Blue, Terminal Green, Amber Retro, Violet)
#   - Today's Top 3 Focus items
#   - Scratch Pad (auto-saved to notes.txt)

import os
import json
import calendar
import datetime
import tkinter as tk
from tkinter import messagebox, simpledialog

calendar.setfirstweekday(calendar.SUNDAY)

BASE_DIR   = os.path.dirname(os.path.abspath(__file__))
TASKS_FILE = os.path.join(BASE_DIR, "tasks.json")
NOTES_FILE = os.path.join(BASE_DIR, "notes.txt")

# ---------------------------------------------------------------------------
# THEMES
# ---------------------------------------------------------------------------

THEMES = {
    "HUD": {
        "bg":           "#0e1621",
        "panel_outer":  "#101c2a",
        "panel_inner":  "#182636",
        "stroke_dark":  "#0a111a",
        "stroke_mid":   "#2a3c52",
        "stroke_light": "#47647f",
        "accent":       "#6fb3c8",
        "text":         "#dce8f2",
        "muted":        "#9fb4c6",
        "danger":       "#ff5a5a",
        "ok":           "#44ff99",
        "btn_bg":       "#1a2a3c",
        "btn_bg_hover": "#22384f",
        "row_bg":       "#162536",
        "row_bg_alt":   "#142231",
        "cell_bg":      "#162536",
        "cell_bg_alt":  "#142231",
    },
    "Terminal": {
        "bg":           "#0a140a",
        "panel_outer":  "#0c180c",
        "panel_inner":  "#122012",
        "stroke_dark":  "#081008",
        "stroke_mid":   "#1e3a1e",
        "stroke_light": "#2e5a2e",
        "accent":       "#44cc44",
        "text":         "#cceecc",
        "muted":        "#7aaa7a",
        "danger":       "#ff5555",
        "ok":           "#44ffaa",
        "btn_bg":       "#162816",
        "btn_bg_hover": "#1e381e",
        "row_bg":       "#122212",
        "row_bg_alt":   "#101e10",
        "cell_bg":      "#122212",
        "cell_bg_alt":  "#101e10",
    },
    "Amber": {
        "bg":           "#1a1209",
        "panel_outer":  "#1e160a",
        "panel_inner":  "#28200e",
        "stroke_dark":  "#120d06",
        "stroke_mid":   "#42300e",
        "stroke_light": "#6a4e18",
        "accent":       "#d4900a",
        "text":         "#f0dca0",
        "muted":        "#b09050",
        "danger":       "#ff6644",
        "ok":           "#aadd44",
        "btn_bg":       "#2e2010",
        "btn_bg_hover": "#3e2c14",
        "row_bg":       "#261e0c",
        "row_bg_alt":   "#221a0a",
        "cell_bg":      "#261e0c",
        "cell_bg_alt":  "#221a0a",
    },
    "Violet": {
        "bg":           "#13111e",
        "panel_outer":  "#171425",
        "panel_inner":  "#201c30",
        "stroke_dark":  "#0e0c18",
        "stroke_mid":   "#352e52",
        "stroke_light": "#564a80",
        "accent":       "#9a7fdc",
        "text":         "#e0d8f8",
        "muted":        "#9080c0",
        "danger":       "#ff5a7a",
        "ok":           "#66ffcc",
        "btn_bg":       "#2a2240",
        "btn_bg_hover": "#362c50",
        "row_bg":       "#1e1a2e",
        "row_bg_alt":   "#1a162a",
        "cell_bg":      "#1e1a2e",
        "cell_bg_alt":  "#1a162a",
    },
}

THEME = dict(THEMES["HUD"])  # active theme (mutable copy)

# ---------------------------------------------------------------------------
# HELPERS
# ---------------------------------------------------------------------------

def _on_hover(btn, normal_bg, hover_bg):
    btn.bind("<Enter>", lambda e: btn.configure(bg=hover_bg))
    btn.bind("<Leave>", lambda e: btn.configure(bg=normal_bg))

def load_tasks():
    if os.path.exists(TASKS_FILE):
        try:
            with open(TASKS_FILE, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception:
            return {}
    return {}

def save_tasks(tasks):
    with open(TASKS_FILE, "w", encoding="utf-8") as f:
        json.dump(tasks, f, indent=4)

def load_notes():
    if os.path.exists(NOTES_FILE):
        try:
            with open(NOTES_FILE, "r", encoding="utf-8") as f:
                return f.read()
        except Exception:
            return ""
    return ""

def save_notes(text):
    with open(NOTES_FILE, "w", encoding="utf-8") as f:
        f.write(text)

def get_today():
    return datetime.date.today().isoformat()

def _get_status_display(status):
    if status == "completed":
        return "[✓]", THEME["ok"]
    elif status == "failed":
        return "[X]", THEME["danger"]
    else:
        return "[ ]", THEME["text"]

def _next_status(status):
    if status == "pending":   return "completed"
    if status == "completed": return "failed"
    return "pending"

def _fire_callback(cb):
    if callable(cb):
        cb()

def _build_task_row(parent, row_bg, description, box_text, box_color, toggle_cmd):
    f = tk.Frame(parent, bg=row_bg, bd=0,
                 highlightthickness=1, highlightbackground=THEME["stroke_mid"])
    f.pack(fill=tk.X, pady=4)
    tk.Button(f, text=box_text, fg=box_color,
        bg=row_bg, activebackground=row_bg, activeforeground=box_color,
        font=("Consolas", 16, "bold"), bd=0, padx=12, pady=10,
        command=toggle_cmd).pack(side=tk.LEFT)
    tk.Label(f, text=description,
        fg=THEME["text"], bg=row_bg,
        font=("Arial", 12), anchor="w", padx=8, pady=10).pack(
        side=tk.LEFT, fill=tk.X, expand=True)

# ---------------------------------------------------------------------------
# HUD PANEL (canvas frame)
# ---------------------------------------------------------------------------

class HudPanel(tk.Canvas):
    _DECO_LINE_X_INSET = 16
    _DECO_LINE_Y       = 10
    _DECO_BOX_RIGHT    = 88
    _DECO_BOX_MARGIN   = 14
    _CORNER_SIZE       = 18

    def __init__(self, master, width=700, height=620, padding=22, **kwargs):
        super().__init__(
            master, width=width, height=height,
            bg=THEME["bg"], highlightthickness=0, bd=0, **kwargs
        )
        self.padding = padding
        self._cw = width
        self._ch = height

        self.content = tk.Frame(self, bg=THEME["panel_inner"])
        self._content_window = self.create_window(
            padding, padding, anchor="nw",
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
        self.itemconfig(self._content_window,
                        width=max(10, w - 2 * pad),
                        height=max(10, h - 2 * pad))
        self.delete("hud")
        self.create_rectangle(
            pad-10, pad-10, w-(pad-10), h-(pad-10),
            fill=THEME["panel_outer"], outline=THEME["stroke_dark"], width=2, tags="hud"
        )
        self.create_rectangle(
            pad, pad, w-pad, h-pad,
            fill=THEME["panel_inner"], outline=THEME["stroke_mid"], width=2, tags="hud"
        )
        lx = self._DECO_LINE_X_INSET; ly = self._DECO_LINE_Y
        br = self._DECO_BOX_RIGHT;    bm = self._DECO_BOX_MARGIN
        self.create_line(pad+lx, pad+ly, w-pad-br, pad+ly,
                         fill=THEME["accent"], width=2, tags="hud")
        self.create_rectangle(
            w-pad-br+2, pad+4, w-pad-bm, pad+16,
            fill=THEME["panel_inner"], outline=THEME["accent"], width=2, tags="hud"
        )
        c = self._CORNER_SIZE
        for coords in [
            [pad, pad+c, pad, pad, pad+c, pad],
            [w-pad-c, pad, w-pad, pad, w-pad, pad+c],
            [pad, h-pad-c, pad, h-pad, pad+c, h-pad],
            [w-pad-c, h-pad, w-pad, h-pad, w-pad, h-pad-c],
        ]:
            self.create_line(*coords, fill=THEME["stroke_light"], width=2, tags="hud")

    def apply_theme(self):
        self.configure(bg=THEME["bg"])
        self.content.configure(bg=THEME["panel_inner"])
        self._redraw()

# ---------------------------------------------------------------------------
# SCROLLABLE FRAME
# ---------------------------------------------------------------------------

class ScrollableFrame(tk.Frame):
    def __init__(self, master, bg, *args, **kwargs):
        super().__init__(master, bg=bg, *args, **kwargs)
        self.canvas = tk.Canvas(self, bg=bg, highlightthickness=0, bd=0)
        self.vsb    = tk.Scrollbar(self, orient="vertical", command=self.canvas.yview)
        self.canvas.configure(yscrollcommand=self.vsb.set)
        self.vsb.pack(side="right", fill="y")
        self.canvas.pack(side="left", fill="both", expand=True)
        self.inner = tk.Frame(self.canvas, bg=bg)
        self._wid  = self.canvas.create_window((0, 0), window=self.inner, anchor="nw")
        self.inner.bind("<Configure>", lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all")))
        self.canvas.bind("<Configure>", lambda e: self.canvas.itemconfig(self._wid, width=e.width))
        self.canvas.bind("<Enter>", self._enter)
        self.canvas.bind("<Leave>", self._leave)

    def _enter(self, _):
        self.canvas.bind_all("<MouseWheel>", self._wheel)
        self.canvas.bind_all("<Button-4>", lambda _: self.canvas.yview_scroll(-1, "units"))
        self.canvas.bind_all("<Button-5>", lambda _: self.canvas.yview_scroll(1,  "units"))

    def _leave(self, _):
        self.canvas.unbind_all("<MouseWheel>")
        self.canvas.unbind_all("<Button-4>")
        self.canvas.unbind_all("<Button-5>")

    def _wheel(self, e):
        self.canvas.yview_scroll(-1 if e.delta > 0 else 1, "units")

    def apply_theme(self, bg):
        self.configure(bg=bg)
        self.canvas.configure(bg=bg)
        self.inner.configure(bg=bg)

# ---------------------------------------------------------------------------
# GOALS PANEL
# ---------------------------------------------------------------------------

class TaskManagerApp:
    def __init__(self, content_frame):
        self.content = content_frame
        self.root    = content_frame.winfo_toplevel()
        self.tasks   = load_tasks()
        self.selected_date = get_today()
        self.on_change     = None

        self.header_frame = tk.Frame(self.content, bg=THEME["panel_inner"])
        self.header_frame.pack(fill=tk.X, padx=14, pady=(12, 8))

        self.title_lbl = tk.Label(self.header_frame, text="GOALS",
            font=("Arial", 18, "bold"), fg=THEME["text"], bg=THEME["panel_inner"])
        self.title_lbl.pack(side=tk.LEFT)

        self.subtitle = tk.Label(self.header_frame, text=self.selected_date,
            font=("Arial", 10, "bold"), fg=THEME["muted"], bg=THEME["panel_inner"])
        self.subtitle.pack(side=tk.RIGHT)

        self.tasks_container = tk.Frame(self.content, bg=THEME["panel_inner"])
        self.tasks_container.pack(fill=tk.BOTH, expand=True, padx=14, pady=(0, 10))

        self.scroll = ScrollableFrame(self.tasks_container, bg=THEME["panel_inner"])
        self.scroll.pack(fill=tk.BOTH, expand=True)

        self.buttons_frame = tk.Frame(self.content, bg=THEME["panel_inner"])
        self.buttons_frame.pack(fill=tk.X, padx=14, pady=(0, 14))

        for text, side, padx, cmd in [
            ("Add a Task",    tk.LEFT,  (0, 8), self.add_task),
            ("Remove a Task", tk.LEFT,  8,      self.remove_task),
            ("Exit",          tk.RIGHT, 0,      self.exit_app),
            ("Save",          tk.RIGHT, (0, 8), self.save),
        ]:
            btn = tk.Button(self.buttons_frame, text=text,
                bg=THEME["btn_bg"], fg=THEME["text"],
                activebackground=THEME["btn_bg_hover"], activeforeground=THEME["text"],
                font=("Arial", 10, "bold"), bd=0, highlightthickness=1,
                highlightbackground=THEME["stroke_mid"], highlightcolor=THEME["accent"],
                padx=14, pady=8, command=cmd)
            btn.pack(side=side, padx=padx)
            _on_hover(btn, THEME["btn_bg"], THEME["btn_bg_hover"])

        self.display_tasks()

    def set_date(self, iso_date):
        self.selected_date = iso_date
        self.subtitle.config(text=self.selected_date)
        self.display_tasks()
        _fire_callback(self.on_change)

    def display_tasks(self):
        for w in self.scroll.inner.winfo_children():
            w.destroy()

        tk.Label(self.scroll.inner, text="DAILY OBJECTIVES",
            fg=THEME["muted"], bg=THEME["panel_inner"],
            font=("Arial", 10, "bold")).pack(anchor="w", pady=(2, 8))

        d = self.selected_date
        if d not in self.tasks or not self.tasks[d]:
            tk.Label(self.scroll.inner, text="No tasks.",
                fg=THEME["text"], bg=THEME["panel_inner"],
                font=("Arial", 12)).pack(pady=14)
            return

        for i, task in enumerate(self.tasks[d]):
            row_bg = THEME["row_bg"] if i % 2 == 0 else THEME["row_bg_alt"]
            box_text, box_color = _get_status_display(task.get("status", "pending"))
            _build_task_row(self.scroll.inner, row_bg, task.get("description", ""),
                            box_text, box_color, lambda idx=i: self.toggle_status(idx))

    def toggle_status(self, index):
        d = self.selected_date
        if d in self.tasks and 0 <= index < len(self.tasks[d]):
            self.tasks[d][index]["status"] = _next_status(
                self.tasks[d][index].get("status", "pending"))
            self.display_tasks()
            _fire_callback(self.on_change)

    def add_task(self):
        desc = simpledialog.askstring("Add Task", "Enter task description:")
        if desc and desc.strip():
            d = self.selected_date
            if d not in self.tasks:
                self.tasks[d] = []
            self.tasks[d].append({"description": desc.strip(), "status": "pending"})
            self.display_tasks()
            _fire_callback(self.on_change)

    def remove_task(self):
        d = self.selected_date
        if d not in self.tasks or not self.tasks[d]:
            messagebox.showinfo("No Tasks", "No tasks to remove.")
            return
        index = simpledialog.askinteger(
            "Remove Task", f"Enter task number to remove (1-{len(self.tasks[d])}):")
        if index is None:
            return
        if 1 <= index <= len(self.tasks[d]):
            removed = self.tasks[d].pop(index - 1)
            self.display_tasks()
            _fire_callback(self.on_change)
            messagebox.showinfo("Removed", f"Task removed: {removed.get('description', '')}")
        else:
            messagebox.showerror("Invalid", "Invalid task number.")

    def save(self):
        save_tasks(self.tasks)
        _fire_callback(self.on_change)

    def exit_app(self):
        if messagebox.askyesno("Exit", "Save tasks before exiting?"):
            save_tasks(self.tasks)
        self.root.destroy()

    def apply_theme(self):
        self.content.configure(bg=THEME["panel_inner"])
        self.header_frame.configure(bg=THEME["panel_inner"])
        self.title_lbl.configure(fg=THEME["text"], bg=THEME["panel_inner"])
        self.subtitle.configure(fg=THEME["muted"], bg=THEME["panel_inner"])
        self.tasks_container.configure(bg=THEME["panel_inner"])
        self.scroll.apply_theme(THEME["panel_inner"])
        self.buttons_frame.configure(bg=THEME["panel_inner"])
        for btn in self.buttons_frame.winfo_children():
            btn.configure(bg=THEME["btn_bg"], fg=THEME["text"],
                          activebackground=THEME["btn_bg_hover"], activeforeground=THEME["text"],
                          highlightbackground=THEME["stroke_mid"], highlightcolor=THEME["accent"])
            _on_hover(btn, THEME["btn_bg"], THEME["btn_bg_hover"])
        self.display_tasks()

# ---------------------------------------------------------------------------
# REMINDER GOALS PANEL
# ---------------------------------------------------------------------------

class ReminderGoalsApp:
    def __init__(self, content_frame, tasks_ref, get_selected_date_callable):
        self.content          = content_frame
        self.tasks            = tasks_ref
        self.get_selected_date = get_selected_date_callable
        self.on_change        = None

        self.header_frame = tk.Frame(self.content, bg=THEME["panel_inner"])
        self.header_frame.pack(fill=tk.X, padx=14, pady=(12, 8))

        self.title_lbl = tk.Label(self.header_frame, text="REMINDER GOALS",
            font=("Arial", 18, "bold"), fg=THEME["text"], bg=THEME["panel_inner"])
        self.title_lbl.pack(side=tk.LEFT)

        tk.Label(self.header_frame, text="Past incomplete tasks",
            font=("Arial", 10, "bold"), fg=THEME["muted"],
            bg=THEME["panel_inner"]).pack(side=tk.RIGHT)

        body = tk.Frame(self.content, bg=THEME["panel_inner"])
        body.pack(fill=tk.BOTH, expand=True, padx=14, pady=(0, 14))

        self.scroll = ScrollableFrame(body, bg=THEME["panel_inner"])
        self.scroll.pack(fill=tk.BOTH, expand=True)

        self.refresh()

    def _iter_incomplete_past(self, selected_date):
        for d in sorted(self.tasks.keys()):
            if d >= selected_date:
                continue
            incomplete = [(i, t) for i, t in enumerate(self.tasks[d])
                          if t.get("status", "pending") != "completed"]
            if incomplete:
                yield d, incomplete

    def toggle_status_for(self, date_key, index):
        if date_key in self.tasks and 0 <= index < len(self.tasks[date_key]):
            self.tasks[date_key][index]["status"] = _next_status(
                self.tasks[date_key][index].get("status", "pending"))
            self.refresh()
            _fire_callback(self.on_change)

    def refresh(self):
        for w in self.scroll.inner.winfo_children():
            w.destroy()

        tk.Label(self.scroll.inner, text="PAST INCOMPLETE",
            fg=THEME["muted"], bg=THEME["panel_inner"],
            font=("Arial", 10, "bold")).pack(anchor="w", pady=(2, 8))

        sel = self.get_selected_date()
        had_any = False

        for dk, incomplete in self._iter_incomplete_past(sel):
            had_any = True
            tk.Label(self.scroll.inner, text=dk,
                fg=THEME["accent"], bg=THEME["panel_inner"],
                font=("Arial", 11, "bold")).pack(anchor="w", pady=(10, 6))

            for row_i, (idx, task) in enumerate(incomplete):
                row_bg = THEME["row_bg"] if row_i % 2 == 0 else THEME["row_bg_alt"]
                box_text, box_color = _get_status_display(task.get("status", "pending"))
                _build_task_row(self.scroll.inner, row_bg, task.get("description", ""),
                                box_text, box_color, lambda d=dk, i=idx: self.toggle_status_for(d, i))

        if not had_any:
            tk.Label(self.scroll.inner, text="No past incomplete tasks.",
                fg=THEME["text"], bg=THEME["panel_inner"],
                font=("Arial", 12)).pack(pady=14)

    def apply_theme(self):
        self.content.configure(bg=THEME["panel_inner"])
        self.header_frame.configure(bg=THEME["panel_inner"])
        self.title_lbl.configure(fg=THEME["text"], bg=THEME["panel_inner"])
        self.scroll.apply_theme(THEME["panel_inner"])
        self.refresh()

# ---------------------------------------------------------------------------
# WIDGET PANEL  (new)
# ---------------------------------------------------------------------------

class WidgetPanel:
    """
    Top-right panel with:
      - Panel visibility toggles (Clock, Goals, Reminders)
      - 12H / 24H clock toggle
      - Theme switcher
      - Today's Top 3 Focus
      - Scratch Pad
    """

    def __init__(self, content_frame, combined_app):
        self.content  = content_frame
        self.app      = combined_app   # reference to CombinedApp for callbacks

        # ---------- outer scroll so it never gets squished ----------
        self.scroll = ScrollableFrame(self.content, bg=THEME["panel_inner"])
        self.scroll.pack(fill=tk.BOTH, expand=True)
        p = self.scroll.inner   # shorthand — everything lives here

        # ---- Header ----
        hdr = tk.Frame(p, bg=THEME["panel_inner"])
        hdr.pack(fill=tk.X, padx=14, pady=(12, 8))
        self.title_lbl = tk.Label(hdr, text="WIDGETS",
            font=("Arial", 18, "bold"), fg=THEME["text"], bg=THEME["panel_inner"])
        self.title_lbl.pack(side=tk.LEFT)
        self.sub_lbl = tk.Label(hdr, text="DAILY CONTROL",
            font=("Arial", 10, "bold"), fg=THEME["muted"], bg=THEME["panel_inner"])
        self.sub_lbl.pack(side=tk.RIGHT)

        # ---- Section: Panel visibility ----
        self._section_label(p, "PANEL VISIBILITY")
        vis_frame = tk.Frame(p, bg=THEME["panel_inner"])
        vis_frame.pack(fill=tk.X, padx=14, pady=(0, 10))

        self._toggle_btns = {}
        panels = [("CLOCK", "clock"), ("GOALS", "goals"), ("REMINDERS", "reminders")]
        for col, (label, key) in enumerate(panels):
            vis_frame.grid_columnconfigure(col, weight=1)

            f = tk.Frame(vis_frame, bg=THEME["panel_inner"])
            f.grid(row=0, column=col, padx=4, sticky="nsew")

            name_lbl = tk.Label(f, text=label,
                font=("Arial", 9, "bold"), fg=THEME["muted"], bg=THEME["panel_inner"])
            name_lbl.pack(pady=(4, 4))

            # Slider toggle drawn on a canvas
            toggle_canvas = tk.Canvas(f, width=46, height=24,
                bg=THEME["panel_inner"], highlightthickness=0, bd=0)
            toggle_canvas.pack(pady=(0, 6))

            self._toggle_btns[key] = {
                "canvas": toggle_canvas,
                "name_lbl": name_lbl,
                "state": True,
                "frame": f,
            }
            self._draw_slider(key, True)

            toggle_canvas.bind("<Button-1>", lambda e, k=key: self._toggle_panel(k))
            name_lbl.bind("<Button-1>",      lambda e, k=key: self._toggle_panel(k))
            f.bind("<Button-1>",             lambda e, k=key: self._toggle_panel(k))

        # ---- Section: Clock format ----
        self._section_label(p, "CLOCK FORMAT")
        cf = tk.Frame(p, bg=THEME["panel_inner"])
        cf.pack(fill=tk.X, padx=14, pady=(0, 10))

        for fmt in ("12H", "24H"):
            rb = tk.Button(cf, text=fmt, width=5,
                bg=THEME["btn_bg"] if fmt != "12H" else THEME["btn_bg_hover"],
                fg=THEME["accent"] if fmt == "12H" else THEME["muted"],
                font=("Arial", 10, "bold"), bd=0,
                highlightthickness=1, highlightbackground=THEME["stroke_mid"],
                padx=10, pady=6,
                command=lambda f=fmt: self._set_clock_fmt(f))
            rb.pack(side=tk.LEFT, padx=(0, 6))
            self._toggle_btns[f"fmt_{fmt}"] = {"btn": rb}

        # ---- Section: Theme ----
        self._section_label(p, "THEME")
        tf = tk.Frame(p, bg=THEME["panel_inner"])
        tf.pack(fill=tk.X, padx=14, pady=(0, 10))

        self._theme_btns = {}
        self._theme_col_frames = {}
        self._theme_name_labels = {}
        for name, data in THEMES.items():
            col_frame = tk.Frame(tf, bg=THEME["panel_inner"])
            col_frame.pack(side=tk.LEFT, padx=6)

            swatch = tk.Label(col_frame, width=4, height=2,
                bg=data["bg"],
                highlightthickness=2,
                highlightbackground=THEME["accent"] if name == "HUD" else THEME["stroke_mid"])
            swatch.pack()
            name_lbl = tk.Label(col_frame, text=name.upper(),
                font=("Arial", 7, "bold"), fg=THEME["muted"],
                bg=THEME["panel_inner"])
            name_lbl.pack()

            self._theme_btns[name] = swatch
            self._theme_col_frames[name] = col_frame
            self._theme_name_labels[name] = name_lbl
            swatch.bind("<Button-1>", lambda e, n=name: self._set_theme(n))
            swatch.bind("<Enter>", lambda e, s=swatch: s.configure(highlightbackground=THEME["accent"]))
            swatch.bind("<Leave>", lambda e, n=name, s=swatch:
                s.configure(highlightbackground=THEME["accent"]
                             if n == self.app.active_theme_name else THEME["stroke_mid"]))

        # ---- Divider ----
        tk.Frame(p, bg=THEME["stroke_mid"], height=1).pack(fill=tk.X, padx=14, pady=(4, 0))

        # ---- Section: Scratch Pad ----
        self._section_label(p, "SCRATCH PAD")
        pad_frame = tk.Frame(p, bg=THEME["panel_inner"])
        pad_frame.pack(fill=tk.X, padx=14, pady=(0, 14))

        self.notes_text = tk.Text(pad_frame,
            bg=THEME["row_bg_alt"], fg=THEME["text"],
            insertbackground=THEME["accent"],
            font=("Consolas", 11),
            height=14, bd=0,
            highlightthickness=1, highlightbackground=THEME["stroke_mid"],
            padx=8, pady=8, wrap=tk.WORD)
        self.notes_text.pack(fill=tk.X)
        self.notes_text.insert(tk.END, load_notes())

        save_btn = tk.Button(pad_frame, text="Save Notes",
            bg=THEME["btn_bg"], fg=THEME["text"],
            activebackground=THEME["btn_bg_hover"], activeforeground=THEME["text"],
            font=("Arial", 9, "bold"), bd=0,
            highlightthickness=1, highlightbackground=THEME["stroke_mid"],
            padx=10, pady=5,
            command=self._save_notes)
        save_btn.pack(anchor="e", pady=(6, 0))
        _on_hover(save_btn, THEME["btn_bg"], THEME["btn_bg_hover"])
        self.save_btn = save_btn

        # auto-save notes on every keystroke (debounced)
        self._autosave_id = None
        self.notes_text.bind("<KeyRelease>", self._autosave_notes)

    def _draw_slider(self, key, state):
        c = self._toggle_btns[key]["canvas"]
        c.delete("all")
        track_color = THEME["accent"] if state else THEME["stroke_mid"]
        knob_x      = 34 if state else 12
        # track
        c.create_oval(2,  4, 22, 20, fill=track_color, outline="")
        c.create_oval(24, 4, 44, 20, fill=track_color, outline="")
        c.create_rectangle(12, 4, 34, 20, fill=track_color, outline="")
        # knob
        c.create_oval(knob_x-10, 2, knob_x+10, 22,
                      fill=THEME["text"], outline=THEME["stroke_mid"], width=1)

    # ------------------------------------------------------------------ helpers

    def _section_label(self, parent, text):
        tk.Label(parent, text=text,
            font=("Arial", 9, "bold"), fg=THEME["muted"],
            bg=THEME["panel_inner"]).pack(anchor="w", padx=14, pady=(10, 4))

    def _save_notes(self):
        save_notes(self.notes_text.get("1.0", tk.END))

    def _autosave_notes(self, _=None):
        if self._autosave_id:
            self.notes_text.after_cancel(self._autosave_id)
        self._autosave_id = self.notes_text.after(1500, self._save_notes)

    # ------------------------------------------------------------------ toggles

    def _toggle_panel(self, key):
        info  = self._toggle_btns[key]
        new   = not info["state"]
        info["state"] = new
        self._draw_slider(key, new)
        info["name_lbl"].configure(fg=THEME["accent"] if new else THEME["muted"])

        self.app.set_panel_visible(key, new)

    def _set_clock_fmt(self, fmt):
        self.app.clock_24h = (fmt == "24H")
        for f in ("12H", "24H"):
            key = f"fmt_{f}"
            btn = self._toggle_btns[key]["btn"]
            active = (f == fmt)
            btn.config(
                bg=THEME["btn_bg_hover"] if active else THEME["btn_bg"],
                fg=THEME["accent"]       if active else THEME["muted"])

    def _set_theme(self, name):
        self.app.apply_theme(name)

    # ------------------------------------------------------------------ theme refresh

    def apply_theme(self):
        self.scroll.apply_theme(THEME["panel_inner"])
        p = self.scroll.inner
        self._retheme_children(p)

        # redraw panel toggle sliders
        for key, info in self._toggle_btns.items():
            if "canvas" not in info:
                continue
            info["canvas"].configure(bg=THEME["panel_inner"])
            info["frame"].configure(bg=THEME["panel_inner"])
            info["name_lbl"].configure(
                bg=THEME["panel_inner"],
                fg=THEME["accent"] if info["state"] else THEME["muted"])
            self._draw_slider(key, info["state"])
        for n, swatch in self._theme_btns.items():
            # always restore the swatch's original bg color from THEMES dict
            swatch.configure(
                bg=THEMES[n]["bg"],
                highlightbackground=THEME["accent"]
                if n == self.app.active_theme_name else THEME["stroke_mid"])
            self._theme_col_frames[n].configure(bg=THEME["panel_inner"])
            self._theme_name_labels[n].configure(bg=THEME["panel_inner"], fg=THEME["muted"])

        self.notes_text.configure(
            bg=THEME["row_bg_alt"], fg=THEME["text"],
            insertbackground=THEME["accent"],
            highlightbackground=THEME["stroke_mid"])
        self.save_btn.configure(
            bg=THEME["btn_bg"], fg=THEME["text"],
            activebackground=THEME["btn_bg_hover"],
            highlightbackground=THEME["stroke_mid"])

    def _retheme_children(self, widget):
        cls = widget.__class__.__name__
        try:
            if cls == "Frame":
                widget.configure(bg=THEME["panel_inner"])
            elif cls == "Label":
                fg = widget.cget("fg")
                # Keep semantic colors (ok/danger) as-is; re-map others
                if fg not in (THEME["ok"], THEME["danger"]):
                    widget.configure(bg=THEME["panel_inner"])
            elif cls == "Button":
                widget.configure(
                    bg=THEME["btn_bg"], fg=THEME["text"],
                    activebackground=THEME["btn_bg_hover"],
                    highlightbackground=THEME["stroke_mid"])
        except Exception:
            pass
        for child in widget.winfo_children():
            self._retheme_children(child)

# ---------------------------------------------------------------------------
# MAIN APP
# ---------------------------------------------------------------------------

class CombinedApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Daily HUD - Clock + Tasks")
        self.root.geometry("1400x1000")
        self.root.minsize(1100, 900)
        self.root.configure(bg=THEME["bg"])

        self.active_theme_name = "HUD"
        self.clock_24h = False

        now = datetime.datetime.now()
        self.current_year  = now.year
        self.current_month = now.month
        self.selected_date = get_today()

        # Paned layout -------------------------------------------------------
        self.main_paned = tk.PanedWindow(root, orient=tk.HORIZONTAL,
            bg=THEME["bg"], sashrelief=tk.FLAT, showhandle=False, bd=0)
        self.main_paned.pack(fill=tk.BOTH, expand=True, padx=14, pady=14)

        self.left_container  = tk.Frame(self.main_paned, bg=THEME["bg"])
        self.right_container = tk.Frame(self.main_paned, bg=THEME["bg"])
        self.main_paned.add(self.left_container,  minsize=720, stretch="never")
        self.main_paned.add(self.right_container, minsize=450, stretch="always")

        # Left column --------------------------------------------------------
        self.left_paned = tk.PanedWindow(self.left_container, orient=tk.VERTICAL,
            bg=THEME["bg"], sashrelief=tk.FLAT, showhandle=False, bd=0)
        self.left_paned.pack(fill=tk.BOTH, expand=True)

        self.clock_panel = HudPanel(self.left_paned, width=700, height=620, padding=22)
        self._build_clock_calendar(self.clock_panel.content)
        self.left_paned.add(self.clock_panel, minsize=620, stretch="never")

        self.tasks_panel = HudPanel(self.left_paned, width=700, height=480, padding=22)
        self.tasks_app   = TaskManagerApp(self.tasks_panel.content)
        self.left_paned.add(self.tasks_panel, minsize=260, stretch="always")

        # Right column -------------------------------------------------------
        self.right_paned = tk.PanedWindow(self.right_container, orient=tk.VERTICAL,
            bg=THEME["bg"], sashrelief=tk.FLAT, showhandle=False, bd=0)
        self.right_paned.pack(fill=tk.BOTH, expand=True)

        self.widgets_panel = HudPanel(self.right_paned, width=700, height=620, padding=22)
        self.widget_app    = WidgetPanel(self.widgets_panel.content, self)
        self.right_paned.add(self.widgets_panel, minsize=620, stretch="never")

        self.reminder_panel = HudPanel(self.right_paned, width=700, height=480, padding=22)
        self.reminder_app   = ReminderGoalsApp(
            self.reminder_panel.content,
            tasks_ref=self.tasks_app.tasks,
            get_selected_date_callable=lambda: self.tasks_app.selected_date)
        self.right_paned.add(self.reminder_panel, minsize=260, stretch="always")

        # Cross-panel callbacks
        self.tasks_app.on_change   = self._on_tasks_change
        self.reminder_app.on_change = self.tasks_app.display_tasks

        # Track which panels are visible
        self._panel_visible = {"clock": True, "goals": True, "reminders": True}

        self.root.after(0, self._place_sashes)
        self.tasks_app.set_date(self.selected_date)
        self.update_calendar()
        self.update_clock()

    def _on_tasks_change(self):
        self.reminder_app.refresh()

    def _place_sashes(self):
        self.main_paned.sash_place(0, 900, 0)
        self.left_paned.sash_place(0, 0, 705)
        self.right_paned.sash_place(0, 0, 705)

    # ------------------------------------------------------------------ panel visibility

    def set_panel_visible(self, key, visible):
        self._panel_visible[key] = visible
        panel_map = {
            "clock":    (self.left_paned,  self.clock_panel,   620, "never"),
            "goals":    (self.left_paned,  self.tasks_panel,   260, "always"),
            "reminders":(self.right_paned, self.reminder_panel, 260, "always"),
        }
        paned, panel, minsize, stretch = panel_map[key]
        if visible:
            paned.add(panel, minsize=minsize, stretch=stretch)
        else:
            paned.remove(panel)

    # ------------------------------------------------------------------ theme

    def apply_theme(self, name):
        global THEME
        self.active_theme_name = name
        THEME.update(THEMES[name])

        self.root.configure(bg=THEME["bg"])
        self.main_paned.configure(bg=THEME["bg"])
        self.left_container.configure(bg=THEME["bg"])
        self.right_container.configure(bg=THEME["bg"])
        self.left_paned.configure(bg=THEME["bg"])
        self.right_paned.configure(bg=THEME["bg"])

        for panel in (self.clock_panel, self.tasks_panel,
                      self.widgets_panel, self.reminder_panel):
            panel.apply_theme()

        self._retheme_clock()
        self.tasks_app.apply_theme()
        self.reminder_app.apply_theme()
        self.widget_app.apply_theme()
        self.update_calendar()

    # ------------------------------------------------------------------ clock

    def update_clock(self):
        now = datetime.datetime.now()
        fmt = "%H:%M:%S" if self.clock_24h else "%I:%M:%S %p"
        self.time_label.config(text=now.strftime(fmt))
        self.date_label.config(text=now.strftime("%B %d, %Y"))
        self.day_label.config(text=now.strftime("%A"))
        self.root.after(1000, self.update_clock)

    def _retheme_clock(self):
        """Re-apply theme colors to the clock/calendar section."""
        bg = THEME["panel_inner"]
        for w in (self.clock_header_frame, self.clock_label_widget):
            w.configure(bg=bg)
        self.time_label.configure(fg=THEME["ok"],     bg=bg)
        self.day_label.configure( fg=THEME["accent"], bg=bg)
        self.date_label.configure(fg=THEME["text"],   bg=bg)
        self.clock_divider.configure(bg=THEME["stroke_mid"])
        self.cal_container.configure(bg=bg)
        self.nav_row.configure(bg=bg)
        self.month_year_label.configure(fg=THEME["text"], bg=bg)
        for btn in self._nav_btns:
            btn.configure(bg=THEME["btn_bg"], fg=THEME["text"],
                          activebackground=THEME["btn_bg_hover"],
                          highlightbackground=THEME["stroke_mid"],
                          highlightcolor=THEME["accent"])
        self.grid_frame.configure(bg=bg)
        for lbl in self._dow_labels:
            lbl.configure(fg=THEME["muted"], bg=bg)

    # ------------------------------------------------------------------ calendar

    def prev_month(self):
        self.current_month -= 1
        if self.current_month == 0:
            self.current_month = 12
            self.current_year -= 1
        self.update_calendar()

    def next_month(self):
        self.current_month += 1
        if self.current_month == 13:
            self.current_month = 1
            self.current_year += 1
        self.update_calendar()

    def on_calendar_day_click(self, iso_date):
        if not iso_date:
            return
        self.selected_date = iso_date
        self.tasks_app.set_date(iso_date)
        self.update_calendar()

    def update_calendar(self):
        self.month_year_label.config(
            text=f"{calendar.month_name[self.current_month]} {self.current_year}")
        cal   = calendar.monthcalendar(self.current_year, self.current_month)
        today = datetime.date.today()

        for r in range(6):
            for c in range(7):
                self.day_cell_dates[r][c] = None

        for wi in range(6):
            for di in range(7):
                base_bg = THEME["cell_bg"] if (wi + di) % 2 == 0 else THEME["cell_bg_alt"]
                if wi < len(cal) and cal[wi][di] != 0:
                    dn = cal[wi][di]
                    cd = datetime.date(self.current_year, self.current_month, dn).isoformat()
                    self.day_cell_dates[wi][di] = cd
                    is_today    = (dn == today.day and
                                   self.current_month == today.month and
                                   self.current_year  == today.year)
                    is_selected = (cd == self.selected_date)
                    fg = THEME["text"]   if is_selected else (THEME["ok"] if is_today else THEME["accent"])
                    bg = THEME["btn_bg_hover"] if is_selected else base_bg
                    text = str(dn)
                else:
                    text, fg, bg = "", THEME["muted"], base_bg

                self.day_grid[wi][di].config(text=text, fg=fg, bg=bg)
                self.day_cell_base_bg[wi][di] = base_bg

    def _build_clock_calendar(self, content):
        # Clock section
        self.clock_header_frame = tk.Frame(content, bg=THEME["panel_inner"])
        self.clock_header_frame.pack(fill=tk.X, padx=14, pady=(14, 6))

        self.clock_label_widget = tk.Label(self.clock_header_frame, text="CLOCK",
            font=("Arial", 16, "bold"), fg=THEME["muted"], bg=THEME["panel_inner"])
        self.clock_label_widget.pack(side=tk.LEFT)

        self.time_label = tk.Label(content, font=("Courier", 52, "bold"),
            fg=THEME["ok"], bg=THEME["panel_inner"])
        self.time_label.pack(pady=(6, 6))

        self.day_label = tk.Label(content, font=("Arial", 20, "bold"),
            fg=THEME["accent"], bg=THEME["panel_inner"])
        self.day_label.pack()

        self.date_label = tk.Label(content, font=("Arial", 18),
            fg=THEME["text"], bg=THEME["panel_inner"])
        self.date_label.pack(pady=(0, 12))

        self.clock_divider = tk.Frame(content, bg=THEME["stroke_mid"], height=1)
        self.clock_divider.pack(fill=tk.X, padx=14, pady=(4, 12))

        # Calendar section
        self.cal_container = tk.Frame(content, bg=THEME["panel_inner"])
        self.cal_container.pack(fill=tk.BOTH, expand=True, padx=14, pady=(0, 14))

        self.nav_row = tk.Frame(self.cal_container, bg=THEME["panel_inner"])
        self.nav_row.pack(fill=tk.X, pady=(0, 10))

        self._nav_btns = []
        for text, side, cmd in [("<", tk.LEFT, self.prev_month), (">", tk.RIGHT, self.next_month)]:
            btn = tk.Button(self.nav_row, text=text, command=cmd,
                font=("Arial", 14, "bold"), fg=THEME["text"], bg=THEME["btn_bg"],
                activebackground=THEME["btn_bg_hover"], activeforeground=THEME["text"],
                bd=0, highlightthickness=1,
                highlightbackground=THEME["stroke_mid"], highlightcolor=THEME["accent"],
                padx=14, pady=8)
            btn.pack(side=side)
            _on_hover(btn, THEME["btn_bg"], THEME["btn_bg_hover"])
            self._nav_btns.append(btn)

        self.month_year_label = tk.Label(self.nav_row, font=("Arial", 16, "bold"),
            fg=THEME["text"], bg=THEME["panel_inner"])
        self.month_year_label.pack(side=tk.LEFT, expand=True)

        self.grid_frame = tk.Frame(self.cal_container, bg=THEME["panel_inner"])
        self.grid_frame.pack(fill=tk.BOTH, expand=True)

        for c in range(7):
            self.grid_frame.grid_columnconfigure(c, weight=1, uniform="cal")

        self._dow_labels = []
        for col, label in enumerate(["Su", "Mo", "Tu", "We", "Th", "Fr", "Sa"]):
            lbl = tk.Label(self.grid_frame, text=label,
                font=("Arial", 11, "bold"), fg=THEME["muted"], bg=THEME["panel_inner"],
                width=4, pady=6)
            lbl.grid(row=0, column=col, padx=2, pady=(0, 6), sticky="nsew")
            self._dow_labels.append(lbl)

        self.day_grid          = []
        self.day_cell_dates    = [[None]*7 for _ in range(6)]
        self.day_cell_base_bg  = [[None]*7 for _ in range(6)]

        def on_enter(e, r, c):
            if self.day_cell_dates[r][c]:
                self.day_grid[r][c].config(bg=THEME["btn_bg_hover"], fg=THEME["text"])

        def on_leave(e, r, c):
            cd = self.day_cell_dates[r][c]
            if not cd:
                return
            base_bg = self.day_cell_base_bg[r][c]
            if cd == self.selected_date:
                self.day_grid[r][c].config(bg=THEME["btn_bg_hover"], fg=THEME["text"])
            else:
                date_obj = datetime.date.fromisoformat(cd)
                fg = THEME["ok"] if date_obj == datetime.date.today() else THEME["accent"]
                self.day_grid[r][c].config(bg=base_bg, fg=fg)

        for wi in range(6):
            week = []
            for di in range(7):
                base_bg = THEME["cell_bg"] if (wi + di) % 2 == 0 else THEME["cell_bg_alt"]
                lbl = tk.Label(self.grid_frame, text="",
                    font=("Arial", 12, "bold"), fg=THEME["accent"], bg=base_bg,
                    width=4, height=2,
                    highlightthickness=1, highlightbackground=THEME["stroke_mid"])
                lbl.grid(row=wi+1, column=di, padx=2, pady=2, sticky="nsew")
                self.day_cell_base_bg[wi][di] = base_bg
                lbl.bind("<Enter>",    lambda e, r=wi, c=di: on_enter(e, r, c))
                lbl.bind("<Leave>",    lambda e, r=wi, c=di: on_leave(e, r, c))
                lbl.bind("<Button-1>", lambda _, r=wi, c=di:
                    self.on_calendar_day_click(self.day_cell_dates[r][c]))
                week.append(lbl)
            self.day_grid.append(week)

# ---------------------------------------------------------------------------

if __name__ == "__main__":
    root = tk.Tk()
    app  = CombinedApp(root)
    root.mainloop()
    root.mainloop()