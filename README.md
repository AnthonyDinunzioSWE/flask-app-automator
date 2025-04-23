🖥️ Flask Project Generator - Windows Desktop App
=================================================

A modern, interactive, and user-friendly Python-based desktop GUI application built with **CustomTkinter** that automates the creation of a full-stack Flask project with proper file structure, template files, environment setup, and Git initialization.

* * * * *

📌 Features
-----------

-   ✅ Cross-platform CustomTkinter-based interface

-   ✅ Auto-generates a Flask project with:

    -   Backend folder setup

    -   Frontend templates and static assets

    -   Virtual environment

    -   Predefined dependencies (Flask, SQLAlchemy, etc.)

-   ✅ Git repository auto-initialization

-   ✅ Tailwind CSS integration

-   ✅ Environment variable setup (.env)

-   ✅ Progress updates and detailed status feedback

* * * * *

⚙️ Tech Stack
-------------

| Component | Details |
| GUI | [CustomTkinter](https://github.com/TomSchimansky/CustomTkinter) |
| Web Backend | Flask (with blueprints and auth support) |
| ORM | SQLAlchemy + Flask-Migrate |
| Authentication | Flask-Login |
| Styling | Tailwind CSS |
| Virtual Environments | Python `venv` |
| Version Control | Git |

* * * * *

🧱 Project Structure (Auto-Generated)
-------------------------------------

```
project_name/
├── backend/
│   ├── __init__.py
│   ├── instances.py
│   ├── models/
│   ├── routes/
│   │   └── main.py
│   └── utils/
├── frontend/
│   ├── static/
│   │   ├── css/styles.css
│   │   ├── js/script.js
│   │   └── uploads/
│   └── templates/
│       ├── base.html
│       ├── main/index.html
│       └── auth/
│           ├── login.html
│           └── register.html
├── .env
├── run.py
├── requirements.txt
├── README.md
└── venv/ (auto-created)
```

* * * * *

🚀 How It Works
---------------

1.  Launch the desktop app.

2.  Enter a project name and choose a folder.

3.  Click **"Create Project"**.

4.  Watch as the app:

    -   Generates directories and files

    -   Creates and activates a virtual environment

    -   Installs all required dependencies

    -   Initializes a Git repository

    -   Outputs real-time progress

* * * * *

📦 Preinstalled Dependencies
----------------------------

The app auto-installs the following into your virtual environment:

```
flask
flask-sqlalchemy
flask-migrate
flask-login
python-dotenv
gunicorn
flask-cors
```

You can also customize `requirements.txt` after project creation.

* * * * *

🔐 Environment Variables
------------------------

`.env` file created automatically:

```
SECRET_KEY=your_secret_key
```

Make sure to update this before deploying!

* * * * *

🖼️ GUI Preview
---------------

[Screenshot 2025-04-22 231641](https://github.com/user-attachments/assets/b28a1eab-f7f0-4001-b8bd-f9aea5fdc9e6)

