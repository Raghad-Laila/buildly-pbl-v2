# Buildly – Project-Based Programming Learning Platform

Buildly is an interactive educational platform designed to teach programming through real-world, project-based learning paths. It bridges the gap between theoretical knowledge and practical application by guiding learners through structured, hands-on projects.

## 🚀 Project Overview

Traditional programming education often lacks practical depth. Buildly addresses this by offering:

- Progressive learning paths: From beginner to expert, organized by topic (e.g., Web Development, AI).
- Real-world projects: Each project includes clear objectives, requirements, and estimated completion time.
- Integrated code editor: Learners can write and run code directly within the platform.
- Smart feedback: Instant evaluation and guidance to improve coding skills.
- User roles: Separate interfaces and permissions for learners and instructors.

## 🚀 Tech Stack

| Layer      | Technology              |
| ---------- | ----------------------- |
| Frontend   | React, Vite, CSS        |
| Backend    | Django (Python)         |
| Database   | SQLite (via Django ORM) |
| Versioning | Git & GitHub            |

## 🚀 How to Run Locally

### 1. Docker build

- cd docker\python-runner
- docker build -t python-runner-image .

### 2. Run Backend (Django)

- cd backendPBL\projectBPL
- python -m venv venv
- source venv/bin/activate # or venv\Scripts\activate on Windows
- pip install -r requirements.txt
- python manage.py migrate

**Windows (recommended):** use the helper script so only one server runs on port 8000:

```powershell
.\scripts\start-server.ps1
```

To stop all servers on port 8000:

```powershell
.\scripts\stop-server.ps1
```

**Manual start:**

```bash
python manage.py runserver
```

> Avoid running multiple `runserver` instances at the same time, and do not use `--noreload` during development.

### 3. Run Frontend (React)

- cd frontend
- npm install
- npm run dev

## 👥 Team Members

- Raghad Laila – Frontend Developer
- Malkeh Herhe – backend Developer
- Supervised by: Eng. Anas Abdelaziz

## 📄 License

This project is part of a graduation requirement at the Syrian Private University – Faculty of Artificial Intelligence Engineering. For academic use only.

`

--- 
