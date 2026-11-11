
import tkinter as tk
from tkinter import ttk, messagebox
from task_manager import work, completed_tasks, save_tasks


# Main Window

root = tk.Tk()
root.title("TaskFlow | Smart Task Management")
root.geometry("1050x760")
root.minsize(850, 650)
root.configure(bg="#0F172A")

root.option_add("*Font", "Arial 10")

completed_window = None
completed_listbox = None
completed_counter = None

visible_tasks = []
editing_task = None


# Theme Colours

BG = "#0F172A"
CARD = "#1E293B"
CARD_LIGHT = "#273449"
BLUE = "#2563EB"
BLUE_HOVER = "#1D4ED8"
GREEN = "#16A34A"
GREEN_HOVER = "#15803D"
RED = "#DC2626"
RED_HOVER = "#B91C1C"
GREY = "#475569"
GREY_HOVER = "#334155"
WHITE = "#FFFFFF"
MUTED = "#94A3B8"
LIGHT_BLUE = "#60A5FA"


# Button Creation

def create_button(parent, text, color, hover_color, command, padx=15):
    button = tk.Button(
        parent,
        text=text,
        font=("Arial", 10, "bold"),
        bg=color,
        fg=WHITE,
        activebackground=hover_color,
        activeforeground=WHITE,
        relief="flat",
        bd=0,
        cursor="hand2",
        padx=padx,
        pady=9,
        command=command
    )

    button.bind(
        "<Enter>",
        lambda event: button.config(bg=hover_color)
    )

    button.bind(
        "<Leave>",
        lambda event: button.config(bg=color)
    )

    return button


# Statistics

def update_statistics():
    total = len(work) + len(completed_tasks)
    pending = len(work)
    completed = len(completed_tasks)

    total_label.config(text=total)
    pending_count_label.config(text=pending)
    completed_count_label.config(text=completed)

    if total > 0:
        percentage = (completed / total) * 100
    else:
        percentage = 0

    progress_bar["value"] = percentage

    progress_label.config(
        text=f"{percentage:.0f}% completed"
    )

    task_counter.config(
        text=f"{pending} pending task(s)"
    )


# Pending Task List

def refresh_task_list():
    global visible_tasks

    task_listbox.delete(0, tk.END)
    visible_tasks = []

    query = search_entry.get().strip().lower()

    for task in work:
        if query in task.lower():
            visible_tasks.append(task)

    if len(visible_tasks) == 0:
        if len(work) == 0:
            task_listbox.insert(tk.END, "No pending tasks!")
        else:
            task_listbox.insert(tk.END, "No matching tasks found!")

    else:
        for task in visible_tasks:
            task_listbox.insert(tk.END, task)

    selected_task_label.config(text="No task selected")

    update_statistics()


def get_selected_task():
    selected = task_listbox.curselection()

    if not selected:
        return None

    index = selected[0]

    if index >= len(visible_tasks):
        return None

    return visible_tasks[index]


def show_selected_task(event):
    task = get_selected_task()

    if task is not None:
        selected_task_label.config(
            text=f"Selected: {task}"
        )
    else:
        selected_task_label.config(
            text="No task selected"
        )


# Completed Task List

def refresh_completed_tasks():
    if completed_listbox is None:
        return

    if not completed_listbox.winfo_exists():
        return

    completed_listbox.delete(0, tk.END)

    if len(completed_tasks) == 0:
        completed_listbox.insert(
            tk.END,
            "No completed tasks yet!"
        )

    else:
        for task in completed_tasks:
            completed_listbox.insert(tk.END, task)

    completed_counter.config(
        text=f"{len(completed_tasks)} completed task(s)"
    )


def close_completed_window():
    global completed_window, completed_listbox

    if completed_window is not None:
        completed_window.destroy()

    completed_window = None
    completed_listbox = None


def open_completed_window():
    global completed_window, completed_listbox, completed_counter

    if completed_window is not None and completed_window.winfo_exists():
        completed_window.lift()
        return

    completed_window = tk.Toplevel(root)
    completed_window.title("TaskFlow | Completed Tasks")
    completed_window.geometry("750x550")
    completed_window.minsize(550, 400)
    completed_window.configure(bg=BG)

    heading = tk.Label(
        completed_window,
        text="Completed Tasks",
        font=("Arial", 24, "bold"),
        bg=BG,
        fg=WHITE
    )
    heading.pack(pady=(25, 5))

    subtitle = tk.Label(
        completed_window,
        text="Your finished work",
        font=("Arial", 11),
        bg=BG,
        fg=MUTED
    )
    subtitle.pack(pady=(0, 10))

    completed_counter = tk.Label(
        completed_window,
        text="0 completed task(s)",
        font=("Arial", 10, "bold"),
        bg=BG,
        fg=LIGHT_BLUE
    )
    completed_counter.pack(pady=(0, 15))

    list_frame = tk.Frame(
        completed_window,
        bg=CARD
    )
    list_frame.pack(
        fill="both",
        expand=True,
        padx=30,
        pady=(0, 15)
    )

    scrollbar = tk.Scrollbar(list_frame)
    scrollbar.pack(side="right", fill="y")

    completed_listbox = tk.Listbox(
        list_frame,
        font=("Arial", 12),
        bg=CARD,
        fg=WHITE,
        selectbackground=BLUE,
        selectforeground=WHITE,
        relief="flat",
        highlightthickness=0,
        yscrollcommand=scrollbar.set
    )
    completed_listbox.pack(
        side="left",
        fill="both",
        expand=True,
        padx=10,
        pady=10
    )

    scrollbar.config(command=completed_listbox.yview)

    action_frame = tk.Frame(
        completed_window,
        bg=BG
    )
    action_frame.pack(pady=(0, 20))

    restore_button = create_button(
        action_frame,
        "Restore Task",
        GREEN,
        GREEN_HOVER,
        restore_completed_task
    )
    restore_button.pack(side="left", padx=8)

    delete_completed_button = create_button(
        action_frame,
        "Delete Permanently",
        RED,
        RED_HOVER,
        delete_completed_task
    )
    delete_completed_button.pack(side="left", padx=8)

    refresh_completed_tasks()

    completed_window.protocol(
        "WM_DELETE_WINDOW",
        close_completed_window
    )


# Add Task

def add_task():
    task = task_entry.get().strip()

    if task == "":
        status_label.config(
            text="Task cannot be empty!",
            fg="#F87171"
        )

    elif task in work:
        status_label.config(
            text="Task already exists!",
            fg="#F87171"
        )

    elif task in completed_tasks:
        status_label.config(
            text="Task already completed!",
            fg="#F87171"
        )

    else:
        work.append(task)
        save_tasks()

        task_entry.delete(0, tk.END)

        refresh_task_list()

        status_label.config(
            text="Task added successfully!",
            fg="#4ADE80"
        )


# Edit Task

def start_edit_task():
    global editing_task

    task = get_selected_task()

    if task is None:
        status_label.config(
            text="Please select a task to edit!",
            fg="#F87171"
        )
        return

    editing_task = task

    task_entry.delete(0, tk.END)
    task_entry.insert(0, task)

    add_button.config(
        text="Save Changes",
        command=save_edited_task
    )

    cancel_edit_button.pack(
        side="right",
        padx=(8, 0)
    )

    status_label.config(
        text="Editing selected task...",
        fg=LIGHT_BLUE
    )


def save_edited_task():
    global editing_task

    new_task = task_entry.get().strip()

    if new_task == "":
        status_label.config(
            text="Task cannot be empty!",
            fg="#F87171"
        )
        return

    if new_task != editing_task:
        if new_task in work or new_task in completed_tasks:
            status_label.config(
                text="This task already exists!",
                fg="#F87171"
            )
            return

    index = work.index(editing_task)
    work[index] = new_task

    save_tasks()

    editing_task = None
    task_entry.delete(0, tk.END)

    add_button.config(
        text="Add Task",
        command=add_task
    )

    cancel_edit_button.pack_forget()

    refresh_task_list()

    status_label.config(
        text="Task updated successfully!",
        fg="#4ADE80"
    )


def cancel_edit():
    global editing_task

    editing_task = None

    task_entry.delete(0, tk.END)

    add_button.config(
        text="Add Task",
        command=add_task
    )

    cancel_edit_button.pack_forget()

    status_label.config(
        text="Editing cancelled!",
        fg=MUTED
    )


# Mark Task Completed

def mark_completed():
    task = get_selected_task()

    if task is None:
        status_label.config(
            text="Please select a task first!",
            fg="#F87171"
        )
        return

    work.remove(task)
    completed_tasks.append(task)

    save_tasks()

    if editing_task == task:
        cancel_edit()

    refresh_task_list()
    refresh_completed_tasks()

    status_label.config(
        text="Task completed successfully!",
        fg="#4ADE80"
    )


# Delete Pending Task

def delete_task():
    task = get_selected_task()

    if task is None:
        status_label.config(
            text="Please select a task first!",
            fg="#F87171"
        )
        return

    confirm = messagebox.askyesno(
        "Confirm Deletion",
        f"Are you sure you want to delete '{task}'?",
        parent=root
    )

    if confirm:
        work.remove(task)
        save_tasks()

        if editing_task == task:
            cancel_edit()

        refresh_task_list()

        status_label.config(
            text="Task deleted successfully!",
            fg="#4ADE80"
        )


# Restore Completed Task

def restore_completed_task():
    selected = completed_listbox.curselection()

    if not selected:
        messagebox.showwarning(
            "No Selection",
            "Please select a completed task first!",
            parent=completed_window
        )
        return

    task = completed_listbox.get(selected[0])

    if task == "No completed tasks yet!":
        return

    if task in work:
        messagebox.showwarning(
            "Task Exists",
            "This task already exists in pending tasks.",
            parent=completed_window
        )
        return

    completed_tasks.remove(task)
    work.append(task)

    save_tasks()

    refresh_task_list()
    refresh_completed_tasks()

    status_label.config(
        text="Task restored successfully!",
        fg="#4ADE80"
    )


# Delete Completed Task

def delete_completed_task():
    selected = completed_listbox.curselection()

    if not selected:
        messagebox.showwarning(
            "No Selection",
            "Please select a completed task first!",
            parent=completed_window
        )
        return

    task = completed_listbox.get(selected[0])

    if task == "No completed tasks yet!":
        return

    confirm = messagebox.askyesno(
        "Confirm Deletion",
        f"Permanently delete '{task}'?",
        parent=completed_window
    )

    if confirm:
        completed_tasks.remove(task)

        save_tasks()

        refresh_completed_tasks()
        update_statistics()

        status_label.config(
            text="Completed task deleted permanently!",
            fg="#4ADE80"
        )


# Search Tasks

def search_task():
    query = search_entry.get().strip()

    if query == "":
        status_label.config(
            text="Please enter a task to search!",
            fg="#F87171"
        )
        return

    refresh_task_list()

    if len(visible_tasks) > 0:
        status_label.config(
            text=f"Found {len(visible_tasks)} matching pending task(s)!",
            fg=LIGHT_BLUE
        )
    else:
        status_label.config(
            text="No matching pending tasks found!",
            fg="#F87171"
        )


def clear_search():
    search_entry.delete(0, tk.END)

    refresh_task_list()

    status_label.config(
        text="Search cleared!",
        fg=LIGHT_BLUE
    )


# Clear Task Input

def clear_task_input():
    if editing_task is not None:
        cancel_edit()
    else:
        task_entry.delete(0, tk.END)

        status_label.config(
            text="Task input cleared!",
            fg=LIGHT_BLUE
        )


# Window Closing

def close_application():
    save_tasks()
    root.destroy()


# Header Section

header_frame = tk.Frame(
    root,
    bg=BG
)
header_frame.pack(fill="x", pady=(22, 12))

heading = tk.Label(
    header_frame,
    text="TaskFlow",
    font=("Arial", 32, "bold"),
    bg=BG,
    fg=WHITE
)
heading.pack()

subtitle = tk.Label(
    header_frame,
    text="Smart Task Management System",
    font=("Arial", 12),
    bg=BG,
    fg=MUTED
)
subtitle.pack(pady=(5, 0))


# Statistics Cards

stats_frame = tk.Frame(
    root,
    bg=BG
)
stats_frame.pack(fill="x", padx=30, pady=12)


def create_stat_card(parent, title, value, accent):
    card = tk.Frame(
        parent,
        bg=CARD,
        padx=20,
        pady=15
    )
    card.pack(
        side="left",
        fill="both",
        expand=True,
        padx=8
    )

    title_label = tk.Label(
        card,
        text=title,
        font=("Arial", 11),
        bg=CARD,
        fg=MUTED
    )
    title_label.pack()

    value_label = tk.Label(
        card,
        text=value,
        font=("Arial", 25, "bold"),
        bg=CARD,
        fg=accent
    )
    value_label.pack(pady=(5, 0))

    return value_label


total_label = create_stat_card(
    stats_frame,
    "TOTAL TASKS",
    0,
    WHITE
)

pending_count_label = create_stat_card(
    stats_frame,
    "PENDING TASKS",
    0,
    LIGHT_BLUE
)

completed_count_label = create_stat_card(
    stats_frame,
    "COMPLETED TASKS",
    0,
    "#4ADE80"
)


# Progress Section

progress_frame = tk.Frame(
    root,
    bg=CARD,
    padx=20,
    pady=12
)
progress_frame.pack(fill="x", padx=38, pady=(5, 15))

progress_heading = tk.Label(
    progress_frame,
    text="Overall Progress",
    font=("Arial", 11, "bold"),
    bg=CARD,
    fg=WHITE
)
progress_heading.pack(anchor="w")

style = ttk.Style()
style.theme_use("clam")

style.configure(
    "TaskFlow.Horizontal.TProgressbar",
    troughcolor="#334155",
    background=BLUE,
    bordercolor=CARD,
    lightcolor=BLUE,
    darkcolor=BLUE
)

progress_bar = ttk.Progressbar(
    progress_frame,
    style="TaskFlow.Horizontal.TProgressbar",
    orient="horizontal",
    mode="determinate",
    maximum=100
)
progress_bar.pack(fill="x", pady=8)

progress_label = tk.Label(
    progress_frame,
    text="0% completed",
    font=("Arial", 9),
    bg=CARD,
    fg=MUTED
)
progress_label.pack(anchor="e")


# Task Input Section

input_heading = tk.Label(
    root,
    text="Create a New Task",
    font=("Arial", 14, "bold"),
    bg=BG,
    fg=WHITE
)
input_heading.pack(anchor="w", padx=40, pady=(8, 7))

input_frame = tk.Frame(
    root,
    bg=BG
)
input_frame.pack(fill="x", padx=40, pady=(0, 15))

task_entry = tk.Entry(
    input_frame,
    font=("Arial", 12),
    bg=CARD,
    fg=WHITE,
    insertbackground=WHITE,
    relief="flat",
    bd=0
)
task_entry.pack(
    side="left",
    fill="x",
    expand=True,
    ipady=11,
    padx=(0, 10)
)

add_button = create_button(
    input_frame,
    "Add Task",
    BLUE,
    BLUE_HOVER,
    add_task,
    18
)
add_button.pack(side="left", padx=(0, 8))

cancel_edit_button = create_button(
    input_frame,
    "Cancel",
    GREY,
    GREY_HOVER,
    cancel_edit
)


clear_input_button = create_button(
    input_frame,
    "Clear",
    GREY,
    GREY_HOVER,
    clear_task_input,
    12
)
clear_input_button.pack(side="right")


# Search Section

search_heading = tk.Label(
    root,
    text="Find Your Tasks",
    font=("Arial", 12, "bold"),
    bg=BG,
    fg="#CBD5E1"
)
search_heading.pack(anchor="w", padx=40, pady=(0, 6))

search_frame = tk.Frame(
    root,
    bg=BG
)
search_frame.pack(fill="x", padx=40, pady=(0, 15))

search_entry = tk.Entry(
    search_frame,
    font=("Arial", 11),
    bg=CARD,
    fg=WHITE,
    insertbackground=WHITE,
    relief="flat",
    bd=0
)
search_entry.pack(
    side="left",
    fill="x",
    expand=True,
    ipady=10,
    padx=(0, 10)
)

search_button = create_button(
    search_frame,
    "Search",
    GREY,
    GREY_HOVER,
    search_task,
    18
)
search_button.pack(side="left", padx=(0, 8))

clear_search_button = create_button(
    search_frame,
    "Clear",
    GREY,
    GREY_HOVER,
    clear_search,
    12
)
clear_search_button.pack(side="right")


# Pending Tasks Heading

task_header_frame = tk.Frame(
    root,
    bg=BG
)
task_header_frame.pack(
    fill="x",
    padx=42,
    pady=(0, 8)
)

list_heading = tk.Label(
    task_header_frame,
    text="Your Pending Tasks",
    font=("Arial", 15, "bold"),
    bg=BG,
    fg=WHITE
)
list_heading.pack(side="left")

task_counter = tk.Label(
    task_header_frame,
    text="0 pending task(s)",
    font=("Arial", 10, "bold"),
    bg=BG,
    fg=LIGHT_BLUE
)
task_counter.pack(side="right")


# Pending Tasks List

list_frame = tk.Frame(
    root,
    bg=CARD
)
list_frame.pack(
    fill="both",
    expand=True,
    padx=38,
    pady=(0, 8)
)

scrollbar = tk.Scrollbar(list_frame)
scrollbar.pack(side="right", fill="y")

task_listbox = tk.Listbox(
    list_frame,
    font=("Arial", 12),
    bg=CARD,
    fg=WHITE,
    selectbackground=BLUE,
    selectforeground=WHITE,
    relief="flat",
    highlightthickness=0,
    yscrollcommand=scrollbar.set,
    activestyle="none"
)
task_listbox.pack(
    side="left",
    fill="both",
    expand=True,
    padx=10,
    pady=10
)

scrollbar.config(command=task_listbox.yview)

task_listbox.bind(
    "<<ListboxSelect>>",
    show_selected_task
)


# Selected Task Information

selected_task_label = tk.Label(
    root,
    text="No task selected",
    font=("Arial", 10),
    bg=BG,
    fg=MUTED
)
selected_task_label.pack(
    anchor="w",
    padx=42,
    pady=(3, 5)
)


# Task Action Buttons

button_frame = tk.Frame(
    root,
    bg=BG
)
button_frame.pack(pady=10)

edit_button = create_button(
    button_frame,
    "Edit Task",
    GREY,
    GREY_HOVER,
    start_edit_task
)
edit_button.pack(side="left", padx=6)

complete_button = create_button(
    button_frame,
    "Mark Completed",
    GREEN,
    GREEN_HOVER,
    mark_completed
)
complete_button.pack(side="left", padx=6)

delete_button = create_button(
    button_frame,
    "Delete Task",
    RED,
    RED_HOVER,
    delete_task
)
delete_button.pack(side="left", padx=6)

completed_button = create_button(
    button_frame,
    "View Completed",
    BLUE,
    BLUE_HOVER,
    open_completed_window
)
completed_button.pack(side="left", padx=6)


# Status Message

status_label = tk.Label(
    root,
    text="Welcome to TaskFlow!",
    font=("Arial", 10),
    bg=BG,
    fg=MUTED
)
status_label.pack(pady=(5, 15))


# Keyboard Shortcuts

task_entry.bind(
    "<Return>",
    lambda event: (
        save_edited_task()
        if editing_task is not None
        else add_task()
    )
)

search_entry.bind(
    "<Return>",
    lambda event: search_task()
)

task_listbox.bind(
    "<Double-Button-1>",
    lambda event: start_edit_task()
)


# Initial Data Loading

refresh_task_list()
update_statistics()


# Close Application

root.protocol(
    "WM_DELETE_WINDOW",
    close_application
)


# Run Application

root.mainloop()
