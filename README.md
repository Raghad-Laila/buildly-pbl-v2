# Buildly – Project-Based Programming Learning Platform

Buildly is an interactive educational platform designed to teach programming through real-world, project-based learning paths. It bridges the gap between theoretical knowledge and practical application by guiding learners through structured, hands-on projects.

## Project folder

After cloning, enter the nested app folder:

```bash
cd buildly---project-Based-learning-platform-master
```

All commands below are relative to that folder.

## Tech Stack

| Layer      | Technology              |
| ---------- | ----------------------- |
| Frontend   | React, Vite, CSS        |
| Backend    | Django (Python)         |
| Database   | SQLite (via Django ORM) |
| Versioning | Git & GitHub            |

## How to Run Locally

### 1. Docker (Python code runner)

```bash
cd docker\python-runner
docker build -t python-runner-image .
cd ..\..
```

### 2. Backend (Django)

```bash
cd backendPBL\projectBPL
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
copy .env.example .env
python manage.py migrate
python manage.py runserver
```

> `db.sqlite3` and `media/` are included in this repo so demo projects and images work after clone.
> Edit `.env` for email / Ollama / Gemini keys as needed.

**Optional AI (Ollama):**

```bash
ollama pull qwen2.5-coder:7b
```

Keep Ollama running while using Ask AI / Improve Code.

### 3. Frontend (React)

```bash
cd frontend
npm install
npm run dev
```

Open the URL shown by Vite (usually http://localhost:5173).

## Team Members

- Raghad Laila – Frontend Developer
- Malkeh Herhe – backend Developer
- Supervised by: Eng. Anas Abdelaziz

## License

This project is part of a graduation requirement at the Syrian Private University – Faculty of Artificial Intelligence Engineering. For academic use only.
