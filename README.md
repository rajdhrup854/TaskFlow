
# TaskFlow – Smart Task Management System

TaskFlow is a Python-based task management application designed to help users organise their daily activities efficiently. It provides both a command-line interface and a graphical user interface for managing tasks.

## Features

- Add new tasks
- View all pending tasks
- Edit existing tasks
- Delete pending tasks
- Mark tasks as completed
- View completed tasks
- Restore completed tasks
- Permanently delete completed tasks
- Search for pending tasks
- View task statistics
- Track overall task completion progress
- Automatically save tasks using JSON storage
- User-friendly graphical interface
- Keyboard shortcuts and confirmation dialogs

## Technologies Used

- Python
- Tkinter
- JSON
- Git and GitHub

## Project Structure

    TaskFlow/
    │
    ├── main.py
    ├── task_manager.py
    ├── gui.py
    ├── README.md
    └── .gitignore

Note: `tasks.json` is generated automatically when task data is saved. It is excluded from GitHub.

## Requirements

- Python 3.x
- Tkinter (usually included with standard Python installations)

No additional third-party Python packages are required.

## How to Run

### 1. Clone the Repository

    git clone YOUR_GITHUB_REPOSITORY_URL

### 2. Open the Project Folder

    cd TaskFlow

### 3. Run the GUI Application

    python gui.py

### 4. Run the Terminal Application

    python main.py

## Data Storage

TaskFlow uses a JSON file named `tasks.json` to store pending and completed tasks.

The data is automatically loaded when the application starts and saved whenever task information changes.

## Future Improvements

- Task priorities
- Due dates and reminders
- Task categories
- Improved dashboard
- Additional productivity features

## Author

Developed as a Python project by **Dhrup Raj**.

---

If you find this project useful, consider giving the repository a star!
