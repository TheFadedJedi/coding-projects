# Daily Task Manager - GUI Version with Sci-Fi HUD Theme + Scroll + [ ]/[✓]/[X]
import datetime
import json
import os
import tkinter as tk
from tkinter import messagebox, simpledialog
#----------------------------------------------------------------------------------------------
TASKS_FILE = 'tasks.json'
#----------------------------------------------------------------------------------------------
def load_tasks():
    if os.path.exists(TASKS_FILE):
        with open(TASKS_FILE, 'r') as f:
            return json.load(f)
    return {}
#----------------------------------------------------------------------------------------------
def save_tasks(tasks):
    with open(TASKS_FILE, 'w') as f:
        json.dump(tasks, f, indent=4)
#----------------------------------------------------------------------------------------------
def get_today():
    return datetime.date.today().isoformat()
#----------------------------------------------------------------------------------------------
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
    "row_bg": "#162536",
    "row_bg_alt": "#142231",
}
#----------------------------------------------------------------------------------------------
def _on_hover(btn, normal_bg, hover_bg):
    btn.bind("<Enter>", lambda e: btn.configure(bg=hover_bg))
    btn.bind("<Leave>", lambda e: btn.configure(bg=normal_bg))
#----------------------------------------------------------------------------------------------
class HudPanel(tk.Canvas):
    def __init__(self, master, width=560, height=460, padding=22, **kwargs):
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
        # Do NOT use self._w / self._h (Tkinter uses them internally)
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

        self.create_rectangle(
            pad-10, pad-10, w-(pad-10), h-(pad-10),
            fill=THEME["panel_outer"],
            outline=THEME["stroke_dark"],
            width=2,
            tags="hud"
        )
        self.create_rectangle(
            pad, pad, w-pad, h-pad,
            fill=THEME["panel_inner"],
            outline=THEME["stroke_mid"],
            width=2,
            tags="hud"
        )

        self.create_line(
            pad+16, pad+10, w-pad-80, pad+10,
            fill=THEME["accent"],
            width=2,
            tags="hud"
        )
        self.create_rectangle(
            w-pad-78, pad+4, w-pad-14, pad+16,
            fill=THEME["panel_inner"],
            outline=THEME["accent"],
            width=2,
            tags="hud"
        )

        corner = 18
        self.create_line(pad, pad+corner, pad, pad, pad+corner, pad,
                         fill=THEME["stroke_light"], width=2, tags="hud")
        self.create_line(w-pad-corner, pad, w-pad, pad, w-pad, pad+corner,
                         fill=THEME["stroke_light"], width=2, tags="hud")
        self.create_line(pad, h-pad-corner, pad, h-pad, pad+corner, h-pad,
                         fill=THEME["stroke_light"], width=2, tags="hud")
        self.create_line(w-pad-corner, h-pad, w-pad, h-pad, w-pad, h-pad-corner,
                         fill=THEME["stroke_light"], width=2, tags="hud")
#----------------------------------------------------------------------------------------------
class ScrollableFrame(tk.Frame):
    """
    A frame with a vertical scrollbar. Put children inside `self.inner`.
    """
    def __init__(self, master, bg, *args, **kwargs):
        super().__init__(master, bg=bg, *args, **kwargs)

        self.canvas = tk.Canvas(self, bg=bg, highlightthickness=0, bd=0)
        self.vsb = tk.Scrollbar(self, orient="vertical", command=self.canvas.yview)

        self.canvas.configure(yscrollcommand=self.vsb.set)

        self.vsb.pack(side="right", fill="y")
        self.canvas.pack(side="left", fill="both", expand=True)

        self.inner = tk.Frame(self.canvas, bg=bg)
        self._window_id = self.canvas.create_window((0, 0), window=self.inner, anchor="nw")

        # Keep scrollregion updated
        self.inner.bind("<Configure>", self._on_inner_configure)
        self.canvas.bind("<Configure>", self._on_canvas_configure)

        # Mouse wheel scrolling (Windows/macOS/Linux)
        self._bind_mousewheel(self.canvas)

    def _on_inner_configure(self, event):
        self.canvas.configure(scrollregion=self.canvas.bbox("all"))

    def _on_canvas_configure(self, event):
        # Make inner frame match canvas width
        self.canvas.itemconfig(self._window_id, width=event.width)

    def _bind_mousewheel(self, widget):
        # Windows/macOS
        widget.bind_all("<MouseWheel>", self._on_mousewheel)
        # Linux
        widget.bind_all("<Button-4>", lambda e: self.canvas.yview_scroll(-1, "units"))
        widget.bind_all("<Button-5>", lambda e: self.canvas.yview_scroll(1, "units"))

    def _on_mousewheel(self, event):
        # On Windows, event.delta is multiples of 120
        # On macOS it can be smaller; this still works fine.
        direction = -1 if event.delta > 0 else 1
        self.canvas.yview_scroll(direction, "units")
#----------------------------------------------------------------------------------------------
class TaskManagerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Daily Task Manager")
        self.root.configure(bg=THEME["bg"])

        self.tasks = load_tasks()
        self.today = get_today()

        self.panel = HudPanel(root, width=560, height=460, padding=22)
        self.panel.pack(fill=tk.BOTH, expand=True, padx=14, pady=14)
#----------------------------------------------------------------------------------------------
        # Header (keep layout similar to earlier)
        self.header_frame = tk.Frame(self.panel.content, bg=THEME["panel_inner"])
        self.header_frame.pack(fill=tk.X, padx=14, pady=(12, 8))

        self.title_label = tk.Label(
            self.header_frame,
            text="GOALS",
            font=("Arial", 18, "bold"),
            fg=THEME["text"],
            bg=THEME["panel_inner"]
        )
        self.title_label.pack(side=tk.LEFT)

        self.subtitle = tk.Label(
            self.header_frame,
            text=f"{self.today}",
            font=("Arial", 10, "bold"),
            fg=THEME["muted"],
            bg=THEME["panel_inner"]
        )
        self.subtitle.pack(side=tk.RIGHT)

        # Scrollable tasks container
        self.tasks_container = tk.Frame(self.panel.content, bg=THEME["panel_inner"])
        self.tasks_container.pack(fill=tk.BOTH, expand=True, padx=14, pady=(0, 10))

        self.scroll = ScrollableFrame(self.tasks_container, bg=THEME["panel_inner"])
        self.scroll.pack(fill=tk.BOTH, expand=True)

        # Buttons at bottom (same as your original)
        self.buttons_frame = tk.Frame(self.panel.content, bg=THEME["panel_inner"])
        self.buttons_frame.pack(fill=tk.X, padx=14, pady=(0, 14))

        self.add_button = tk.Button(
            self.buttons_frame, text="Add a Task",
            bg=THEME["btn_bg"], fg=THEME["text"],
            activebackground=THEME["btn_bg_hover"], activeforeground=THEME["text"],
            font=("Arial", 10, "bold"),
            bd=0, highlightthickness=1,
            highlightbackground=THEME["stroke_mid"], highlightcolor=THEME["accent"],
            padx=14, pady=8,
            command=self.add_task
        )
        self.add_button.pack(side=tk.LEFT, padx=(0, 8))
        _on_hover(self.add_button, THEME["btn_bg"], THEME["btn_bg_hover"])

        self.remove_button = tk.Button(
            self.buttons_frame, text="Remove a Task",
            bg=THEME["btn_bg"], fg=THEME["text"],
            activebackground=THEME["btn_bg_hover"], activeforeground=THEME["text"],
            font=("Arial", 10, "bold"),
            bd=0, highlightthickness=1,
            highlightbackground=THEME["stroke_mid"], highlightcolor=THEME["accent"],
            padx=14, pady=8,
            command=self.remove_task
        )
        self.remove_button.pack(side=tk.LEFT, padx=8)
        _on_hover(self.remove_button, THEME["btn_bg"], THEME["btn_bg_hover"])

        self.exit_button = tk.Button(
            self.buttons_frame, text="Exit",
            bg=THEME["btn_bg"], fg=THEME["text"],
            activebackground=THEME["btn_bg_hover"], activeforeground=THEME["text"],
            font=("Arial", 10, "bold"),
            bd=0, highlightthickness=1,
            highlightbackground=THEME["stroke_mid"], highlightcolor=THEME["accent"],
            padx=14, pady=8,
            command=self.exit_app
        )
        self.exit_button.pack(side=tk.RIGHT, padx=(8, 0))
        _on_hover(self.exit_button, THEME["btn_bg"], THEME["btn_bg_hover"])

        self.save_button = tk.Button(
            self.buttons_frame, text="Save",
            bg=THEME["btn_bg"], fg=THEME["text"],
            activebackground=THEME["btn_bg_hover"], activeforeground=THEME["text"],
            font=("Arial", 10, "bold"),
            bd=0, highlightthickness=1,
            highlightbackground=THEME["stroke_mid"], highlightcolor=THEME["accent"],
            padx=14, pady=8,
            command=self.save
        )
        self.save_button.pack(side=tk.RIGHT)
        _on_hover(self.save_button, THEME["btn_bg"], THEME["btn_bg_hover"])

        self.display_tasks()

    def display_tasks(self):
        # Clear existing widgets inside scrollable inner frame
        for widget in self.scroll.inner.winfo_children():
            widget.destroy()

        # Section label (kept in list area)
        section_title = tk.Label(
            self.scroll.inner,
            text="DAILY OBJECTIVES",
            fg=THEME["muted"],
            bg=THEME["panel_inner"],
            font=("Arial", 10, "bold")
        )
        section_title.pack(anchor="w", pady=(2, 8))

        if self.today not in self.tasks or not self.tasks[self.today]:
            tk.Label(
                self.scroll.inner,
                text="No tasks.",
                fg=THEME["text"],
                bg=THEME["panel_inner"],
                font=("Arial", 12)
            ).pack(pady=14)
            return

        for i, task in enumerate(self.tasks[self.today]):
            row_bg = THEME["row_bg"] if i % 2 == 0 else THEME["row_bg_alt"]

            task_frame = tk.Frame(
                self.scroll.inner,
                bg=row_bg,
                bd=0,
                highlightthickness=1,
                highlightbackground=THEME["stroke_mid"]
            )
            task_frame.pack(fill=tk.X, pady=4)

            # Always show a bracketed box, fill with ✓ / X when needed
            status = task.get("status", "pending")
            if status == "completed":
                box_text = "[✓]"
                box_color = THEME["ok"]
            elif status == "failed":
                box_text = "[X]"
                box_color = THEME["danger"]
            else:
                box_text = "[ ]"
                box_color = THEME["text"]

            # Big clickable box on the LEFT
            status_button = tk.Button(
                task_frame,
                text=box_text,
                fg=box_color,
                bg=row_bg,
                activebackground=row_bg,
                activeforeground=box_color,
                font=("Consolas", 16, "bold"),  # monospaced makes the box line up nicely
                bd=0,
                padx=12,
                pady=10,
                command=lambda idx=i: self.toggle_status(idx)
            )
            status_button.pack(side=tk.LEFT)

            # Task description to the right
            desc_label = tk.Label(
                task_frame,
                text=task["description"],
                fg=THEME["text"],
                bg=row_bg,
                font=("Arial", 12),
                anchor="w",
                padx=8,
                pady=10
            )
            desc_label.pack(side=tk.LEFT, fill=tk.X, expand=True)

    def toggle_status(self, index):
        if self.today in self.tasks and 0 <= index < len(self.tasks[self.today]):
            current_status = self.tasks[self.today][index]["status"]
            if current_status == "pending":
                self.tasks[self.today][index]["status"] = "completed"
            elif current_status == "completed":
                self.tasks[self.today][index]["status"] = "failed"
            else:
                self.tasks[self.today][index]["status"] = "pending"
            self.display_tasks()

    def add_task(self):
        desc = simpledialog.askstring("Add Task", "Enter task description:")
        if desc and desc.lower() != "cancel":
            if self.today not in self.tasks:
                self.tasks[self.today] = []
            self.tasks[self.today].append({"description": desc, "status": "pending"})
            self.display_tasks()

    def remove_task(self):
        if self.today not in self.tasks or not self.tasks[self.today]:
            messagebox.showinfo("No Tasks", "No tasks to remove.")
            return
        try:
            index = simpledialog.askinteger(
                "Remove Task",
                f"Enter task number to remove (1-{len(self.tasks[self.today])}):"
            )
            if index is not None and 1 <= index <= len(self.tasks[self.today]):
                removed_task = self.tasks[self.today].pop(index - 1)
                self.display_tasks()
                messagebox.showinfo("Removed", f"Task removed: {removed_task['description']}")
            else:
                messagebox.showerror("Invalid", "Invalid task number.")
        except:
            messagebox.showerror("Error", "Invalid input.")

    def save(self):
        save_tasks(self.tasks)

    def exit_app(self):
        self.root.quit()

    def save_and_exit(self):
        save_tasks(self.tasks)
        self.root.quit()
#----------------------------------------------------------------------------------------------
if __name__ == "__main__":
    root = tk.Tk()
    root.geometry("700x680")
    root.minsize(640, 620)
    app = TaskManagerApp(root)
    root.mainloop()