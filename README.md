Flask Project Automator
  

A professional desktop application that automates the creation of robust Flask project structures with a single click.



🚀 Features
Complete Flask Structure: Generates a fully structured Flask project using best practices
Pre-configured Components: Sets up SQLAlchemy, Flask-Migrate, Flask-Login, and more
Modern Frontend: Includes Tailwind CSS for styling
Environment Setup: Automatically creates a virtual environment with all dependencies
Git Integration: Initializes a Git repository
Instant Launch: Directly runs your Flask app and opens it in the browser
IDE Integration: Opens project in VSCode (if installed)
User-Friendly Interface: Clean, modern UI with real-time progress tracking
📋 Prerequisites
Python 3.8 or higher
Git (optional, but recommended)
Visual Studio Code (optional)
Windows, macOS, or Linux operating system
🔧 Installation
Clone this repository or download the latest release:
git clone https://github.com/yourusername/flask-project-automator.git
cd flask-project-automator
Create a virtual environment (recommended):
python -m venv venv
venv\Scripts\activate  # On Windows
source venv/bin/activate  # On macOS/Linux
Install required dependencies:
pip install -r requirements.txt
💻 Usage
Run the application:
python flask_automator.py
Fill in your project details:

Project Name: Name of your Flask application
Project Location: Directory where your project will be created
Click Create Project and watch as the application:

Creates the project structure
Sets up a virtual environment
Installs all dependencies
Initializes Git repository
Launches your Flask application
Opens the project in VSCode (if available)
🏗️ Generated Project Structure
your_project_name/
├── backend/
│   ├── models/
│   ├── routes/
│   │   └── main.py
│   ├── utils/
│   ├── __init__.py
│   └── instances.py
├── frontend/
│   ├── static/
│   │   ├── css/
│   │   │   └── styles.css
│   │   ├── js/
│   │   │   └── script.js
│   │   └── uploads/
│   └── templates/
│       ├── auth/
│       │   ├── login.html
│       │   └── register.html
│       ├── main/
│       │   └── index.html
│       └── base.html
├── venv/
├── .env
├── .git/
├── README.md
├── requirements.txt
└── run.py
✨ Technologies Included
| Category | Components | |----------|------------| | Backend | Flask, Flask-SQLAlchemy, Flask-Migrate, Flask-Login, Flask-CORS | | Database | SQLAlchemy ORM, SQLite (default) | | Frontend | Tailwind CSS, HTML templates, JavaScript | | Development | Python dotenv, Git integration, VSCode integration | | Deployment | Gunicorn pre-configured |

🛠️ Customization
The Flask Project Automator can be customized by modifying:

DEPENDENCIES list in 
flask_automator.py
 to add or remove Python packages
FOLDER_STRUCTURE dictionary to change the generated file structure
TEMPLATES dictionary to modify the content of generated files
🔍 How It Works
Project Structure Creation: Generates directories and files based on the defined structure
Git Initialization: Sets up a Git repository in the project folder
Virtual Environment: Creates and activates a Python virtual environment
Dependency Installation: Installs all required packages using pip
Requirements Generation: Creates a requirements.txt file with exact package versions
Application Launch: Starts the Flask development server
IDE Integration: Opens the project in Visual Studio Code
🤝 Contributing
Contributions are welcome! Here's how you can contribute:

Fork the repository
Create a feature branch: git checkout -b feature/amazing-feature
Commit your changes: git commit -m 'Add some amazing feature'
Push to the branch: git push origin feature/amazing-feature
Open a Pull Request
