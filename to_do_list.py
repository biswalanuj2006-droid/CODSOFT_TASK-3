import customtkinter as ctk
import sqlite3
import os
from dotenv import load_dotenv
from tkinter import messagebox
from datetime import datetime

# ==================================================
# LOAD SECRET API KEY
# ==================================================
load_dotenv()

API_KEY = os.getenv("API_KEY")

if not API_KEY:
    raise ValueError(
        "API_KEY not found! Create a .env file and add:\n"
        "API_KEY=YOUR_SECRET_API_KEY"
    )

APP_VERSION = "3.0 Secure Edition"

# ==================================================
# CUSTOMTKINTER CONFIG
# ==================================================
ctk.set_appearance_mode("Dark")
ctk.set_default_color_theme("blue")


# ==================================================
# DATABASE MANAGER
# ==================================================
class DatabaseManager:
    def __init__(self):
        self.db_name = "taskflow_pro.db"
        self.create_database()

    def create_database(self):
        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()

        cursor.execute("""
        CREATE TABLE IF NOT EXISTS tasks(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            priority TEXT,
            status TEXT,
            created_at TEXT
        )
        """)

        conn.commit()
        conn.close()

    def add_task(self, title, priority):
        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()

        cursor.execute(
            """
            INSERT INTO tasks(title, priority, status, created_at)
            VALUES(?,?,?,?)
            """,
            (
                title,
                priority,
                "Pending",
                datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            )
        )

        conn.commit()
        conn.close()

    def get_tasks(self, search=""):
        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()

        if search:
            cursor.execute(
                "SELECT * FROM tasks WHERE title LIKE ? ORDER BY id DESC",
                (f"%{search}%",)
            )
        else:
            cursor.execute(
                "SELECT * FROM tasks ORDER BY id DESC"
            )

        tasks = cursor.fetchall()

        conn.close()
        return tasks

    def delete_task(self, task_id):
        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()

        cursor.execute(
            "DELETE FROM tasks WHERE id=?",
            (task_id,)
        )

        conn.commit()
        conn.close()


# ==================================================
# TASK CARD
# ==================================================
class TaskCard(ctk.CTkFrame):

    def __init__(self, parent, task, delete_function):
        super().__init__(parent)

        self.configure(
            corner_radius=12,
            height=80
        )

        task_id = task[0]
        title = task[1]
        priority = task[2]
        status = task[3]
        created = task[4]

        colors = {
            "High": "#ff4d4d",
            "Medium": "#ffaa00",
            "Low": "#22c55e"
        }

        indicator = ctk.CTkFrame(
            self,
            width=8,
            fg_color=colors.get(priority, "gray")
        )

        indicator.pack(
            side="left",
            fill="y",
            padx=(0, 10)
        )

        content = ctk.CTkFrame(
            self,
            fg_color="transparent"
        )

        content.pack(
            side="left",
            fill="both",
            expand=True,
            padx=10,
            pady=10
        )

        ctk.CTkLabel(
            content,
            text=title,
            font=ctk.CTkFont(
                size=16,
                weight="bold"
            )
        ).pack(anchor="w")

        ctk.CTkLabel(
            content,
            text=f"Priority: {priority} | Status: {status}",
            text_color="gray"
        ).pack(anchor="w")

        ctk.CTkLabel(
            content,
            text=created,
            text_color="gray"
        ).pack(anchor="w")

        ctk.CTkButton(
            self,
            text="Delete",
            width=80,
            fg_color="#cc0000",
            hover_color="#880000",
            command=lambda: delete_function(task_id)
        ).pack(
            side="right",
            padx=15
        )


# ==================================================
# MAIN APP
# ==================================================
class TaskFlowApp(ctk.CTk):

    def __init__(self):
        super().__init__()

        self.db = DatabaseManager()

        self.title(f"TaskFlow Pro • {APP_VERSION}")
        self.geometry("1100x700")

        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)

        self.create_sidebar()
        self.create_main_area()

        self.refresh_tasks()

    # ---------------------------------------------
    def create_sidebar(self):

        self.sidebar = ctk.CTkFrame(
            self,
            width=300,
            corner_radius=0
        )

        self.sidebar.grid(
            row=0,
            column=0,
            sticky="ns"
        )

        ctk.CTkLabel(
            self.sidebar,
            text="TASKFLOW PRO",
            font=ctk.CTkFont(
                size=26,
                weight="bold"
            )
        ).pack(pady=25)

        self.task_entry = ctk.CTkEntry(
            self.sidebar,
            placeholder_text="Enter Task..."
        )

        self.task_entry.pack(
            padx=20,
            fill="x",
            pady=10
        )

        self.priority = ctk.CTkOptionMenu(
            self.sidebar,
            values=[
                "High",
                "Medium",
                "Low"
            ]
        )

        self.priority.pack(
            padx=20,
            fill="x"
        )

        self.priority.set("Medium")

        ctk.CTkButton(
            self.sidebar,
            text="Create Task",
            command=self.add_task
        ).pack(
            padx=20,
            pady=20,
            fill="x"
        )

        api_frame = ctk.CTkFrame(self.sidebar)

        api_frame.pack(
            padx=20,
            pady=20,
            fill="x"
        )

        ctk.CTkLabel(
            api_frame,
            text="SECURE API STATUS"
        ).pack(pady=10)

        masked = API_KEY[:4] + "*" * 12

        ctk.CTkLabel(
            api_frame,
            text=masked
        ).pack()

        ctk.CTkLabel(
            api_frame,
            text="● ACTIVE",
            text_color="green"
        ).pack(pady=10)

    # ---------------------------------------------
    def create_main_area(self):

        container = ctk.CTkFrame(
            self,
            fg_color="transparent"
        )

        container.grid(
            row=0,
            column=1,
            sticky="nsew",
            padx=20,
            pady=20
        )

        container.grid_rowconfigure(1, weight=1)
        container.grid_columnconfigure(0, weight=1)

        self.search_box = ctk.CTkEntry(
            container,
            placeholder_text="Search Tasks..."
        )

        self.search_box.grid(
            row=0,
            column=0,
            sticky="ew",
            pady=(0, 10)
        )

        self.search_box.bind(
            "<KeyRelease>",
            lambda e: self.refresh_tasks()
        )

        self.scroll = ctk.CTkScrollableFrame(
            container,
            label_text="Task Timeline"
        )

        self.scroll.grid(
            row=1,
            column=0,
            sticky="nsew"
        )

    # ---------------------------------------------
    def add_task(self):

        title = self.task_entry.get().strip()

        if not title:
            messagebox.showwarning(
                "Warning",
                "Task title cannot be empty."
            )
            return

        self.db.add_task(
            title,
            self.priority.get()
        )

        self.task_entry.delete(0, "end")

        self.refresh_tasks()

    # ---------------------------------------------
    def delete_task(self, task_id):

        if messagebox.askyesno(
            "Confirm",
            "Delete this task?"
        ):
            self.db.delete_task(task_id)
            self.refresh_tasks()

    # ---------------------------------------------
    def refresh_tasks(self):

        for widget in self.scroll.winfo_children():
            widget.destroy()

        tasks = self.db.get_tasks(
            self.search_box.get()
        )

        for task in tasks:
            card = TaskCard(
                self.scroll,
                task,
                self.delete_task
            )

            card.pack(
                fill="x",
                padx=10,
                pady=8
            )


# ==================================================
# START APPLICATION
# ==================================================
if __name__ == "__main__":
    app = TaskFlowApp()
    app.mainloop()