# 🚀 TaskFlow Pro

A modern desktop task management application built with **Python**, **CustomTkinter**, and **SQLite**.

TaskFlow Pro provides a sleek dark-themed interface for creating, managing, searching, and deleting tasks while storing data locally using SQLite.

---

# 📸 Features

### ✅ Task Management

* Create new tasks
* Delete tasks instantly
* Assign priority levels

  * 🔴 High
  * 🟠 Medium
  * 🟢 Low

### ✅ Modern User Interface

* Built with CustomTkinter
* Dark Mode Design
* Responsive Layout
* Scrollable Task Timeline

### ✅ Local Database Storage

* SQLite Database Integration
* Automatic Database Creation
* Persistent Data Storage

### ✅ Search System

* Real-time task filtering
* Instant search updates

### ✅ Task Information

* Unique Task IDs
* Creation Timestamps
* Priority Indicators

---

# 🛠 Technologies Used

| Technology    | Purpose              |
| ------------- | -------------------- |
| Python        | Core Programming     |
| CustomTkinter | Modern GUI           |
| SQLite3       | Database Storage     |
| Datetime      | Timestamp Management |

---

# 📂 Project Structure

```text
TaskFlow-Pro/
│
├── taskflow.py
├── taskflow_pro.db
├── README.md
│
└── assets/
```

---

# ⚙️ Installation

## 1. Clone Repository

```bash
git clone https://github.com/your-username/taskflow-pro.git
```

## 2. Open Project Folder

```bash
cd taskflow-pro
```

## 3. Install Dependencies

```bash
pip install customtkinter
```

---

# ▶️ Run Application

```bash
python taskflow.py
```

---

# 🖥 User Interface

### Sidebar

* Create New Tasks
* Select Priority
* API Status Panel

### Main Area

* Search Tasks
* Active Timeline
* Scrollable Task Cards

---

# 💾 Database Schema

```sql
CREATE TABLE tasks (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    title TEXT NOT NULL,
    priority TEXT,
    status TEXT,
    api_sync_id TEXT,
    created_at TEXT
);
```

---

# 📋 Example Task

```text
Task Title : Complete AI Project
Priority   : High
Status     : Pending
Created At : 2026-06-03 15:30
```

---

# 🔥 Key Components

## DatabaseManager

Responsible for:

* Database Initialization
* Task Storage
* Task Retrieval
* Task Deletion

---

## TaskCard

Custom UI component displaying:

* Task Title
* Priority Marker
* Timestamp
* Delete Button

---

## TaskFlowApp

Main application engine handling:

* GUI Layout
* Search System
* Task Creation
* Task Rendering

---

# 🚀 Future Enhancements

* Task Editing
* Task Completion Tracking
* Due Dates
* Notifications
* Cloud Synchronization
* User Authentication
* Export Tasks to CSV
* Data Backup System
* Kanban Board View
* Analytics Dashboard

---

# 📊 Requirements

* Python 3.10+
* CustomTkinter
* SQLite3 (Built-in)

---

# 👨‍💻 Author

ANUJ

---
