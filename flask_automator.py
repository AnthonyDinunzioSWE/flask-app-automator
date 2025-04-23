import os
import subprocess
import customtkinter as ctk
from tkinter import filedialog, messagebox
import time
import webbrowser
import threading
from PIL import Image, ImageTk

# Constants
DEPENDENCIES = [
    "flask", "flask-sqlalchemy", "flask-migrate",
    "flask-login", "python-dotenv", "gunicorn", "flask-cors"
]

FOLDER_STRUCTURE = {
    "backend/models": [],
    "backend/routes": [],
    "backend/utils": [],
    "backend/instances.py": "instances_py",
    "backend/__init__.py": "init_py",
    "backend/routes/main.py": "main_routes",
    "frontend/templates/base.html": "html_base",
    "frontend/templates/main/index.html": "index_html",
    "frontend/templates/auth/login.html": "",
    "frontend/templates/auth/register.html": "",
    "frontend/static/css/styles.css": "",
    "frontend/static/js/script.js": "",
    "frontend/static/uploads": [],
    "requirements.txt": "",
    "README.md": "# Project README\n",
    ".env": "SECRET_KEY=your_secret_key\n",
    "run.py": "from backend import app\n\nif __name__ == '__main__':\n    app.run(debug=True)"
}

TEMPLATES = {
    "html_base": """<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<title>{% block title %}My App{% endblock %}</title>
<link href="https://cdn.jsdelivr.net/npm/tailwindcss/dist/tailwind.min.css" rel="stylesheet">
</head>
<body>
{% block content %}{% endblock %}
</body>
</html>""",
    "instances_py": """from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
# Singleton instances
db = SQLAlchemy()
migrate = Migrate()
login_manager = LoginManager()
""",
    "init_py": """from flask import Flask
from flask_cors import CORS
from .instances import db, migrate, login_manager
import os
app = Flask(__name__,
static_folder='../frontend/static',
template_folder='../frontend/templates')
# Load config
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'default-dev-key')
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
# Initialize extensions
db.init_app(app)
migrate.init_app(app, db)
login_manager.init_app(app)
login_manager.login_view = 'auth.login'
@login_manager.user_loader
def load_user(user_id):
    try:
        return None
        #return User.query.get(user_id)
    except Exception:
        return None
# Enable CORS
CORS(app)
# Register blueprints
from .routes.main import main_bp
app.register_blueprint(main_bp)
""",
    "main_routes": """from flask import Blueprint, render_template
main_bp = Blueprint('main', __name__)
@main_bp.route('/')
def index():
    return render_template('main/index.html')
""",
    "index_html": """{% extends "base.html" %}
{% block title %}Welcome{% endblock %}
{% block content %}
<div class="container mx-auto px-4 py-8">
    <div class="text-center">
        <h1 class="text-4xl font-bold text-blue-600 mb-4">Welcome to Your Flask App</h1>
        <p class="text-xl text-gray-700 mb-8">Your application is running successfully!</p>
        <div class="bg-gray-100 p-6 rounded-lg shadow-md inline-block">
            <p class="text-left text-gray-800">
                <span class="font-semibold">Project structure created:</span><br>
                ✅ SQLAlchemy database integration<br>
                ✅ Flask-Migrate for database migrations<br>
                ✅ Flask-Login for user authentication<br>
                ✅ Tailwind CSS for styling<br>
                ✅ Environment variables configuration
            </p>
        </div>
    </div>
</div>
{% endblock %}
"""
}

def browse_folder(entry):
    """Open folder browser dialog and update the entry field with selected path."""
    path = filedialog.askdirectory()
    if path:
        entry.delete(0, ctk.END)
        entry.insert(0, path)

def start_creation(project_name, base_path, progress_bar, status_label, create_btn, app):
    """Start project creation in a separate thread to keep UI responsive."""
    if not project_name or not base_path:
        status_label.configure(text="⚠️ Please provide project name and location", text_color="orange")
        return
    
    # Show progress bar and update UI
    progress_bar.pack(fill="x", pady=10)
    status_label.configure(text="⏳ Initializing project creation...", text_color="grey")
    create_btn.configure(state="disabled", text="Creating Project...")
    progress_bar.set(0)  # Reset progress bar
    
    # Start the creation in a separate thread to avoid UI freezing
    thread = threading.Thread(
        target=create_project,
        args=(project_name, base_path, progress_bar, status_label, create_btn, app)
    )
    thread.daemon = True
    thread.start()

def create_project(project_name, base_path, progress_bar, status_label, create_btn, app):
    """Create a Flask project with the specified structure and settings."""
    project_path = os.path.join(base_path, project_name)
    
    # Helper function to update progress bar and status
    def update_status(percent, message, color="grey"):
        app.after(0, lambda p=percent/100, m=message, c=color: (
            progress_bar.set(p),
            status_label.configure(text=m, text_color=c)
        ))
        app.update_idletasks()
        time.sleep(0.1)  # Small delay for visual effect
    
    # Helper function to show error dialog
    def show_error(title, message):
        app.after(0, lambda t=title, m=message: messagebox.showerror(t, m))
    
    # Helper function to show warning dialog
    def show_warning(title, message):
        app.after(0, lambda t=title, m=message: messagebox.showwarning(t, m))
    
    # Helper function to show info dialog
    def show_info(title, message):
        app.after(0, lambda t=title, m=message: messagebox.showinfo(t, m))
    
    try:
        # Initialize project directory
        update_status(5, "📁 Creating project directory...", "grey")
        os.makedirs(project_path, exist_ok=True)
        
        # Step 1: Create folder structure (0-15%)
        file_count = len(FOLDER_STRUCTURE)
        for idx, (path, content) in enumerate(FOLDER_STRUCTURE.items()):
            # Calculate progress percentage (0-15% range for this step)
            percent = 5 + (idx / file_count * 10)
            update_status(percent, f"📁 Creating project structure ({idx+1}/{file_count})...")
            
            full_path = os.path.join(project_path, path)
            if isinstance(content, list):
                os.makedirs(full_path, exist_ok=True)
            else:
                os.makedirs(os.path.dirname(full_path), exist_ok=True)
                with open(full_path, 'w', encoding='utf-8') as f:
                    f.write(TEMPLATES.get(content, content))
        
        # Step 2: Initialize Git (15-20%)
        update_status(15, "🔄 Initializing Git repository...")
        try:
            subprocess.call(["git", "init"], cwd=project_path)
            update_status(20, "🔄 Git repository initialized!")
        except Exception as e:
            # Continue even if git fails
            error_msg = str(e)
            update_status(20, f"⚠️ Git initialization skipped: {error_msg}", "orange")
            time.sleep(1)  # Show warning briefly
        
        # Step 3: Create virtual environment (20-35%)
        update_status(25, "🔧 Creating virtual environment...")
        try:
            subprocess.call(["python", "-m", "venv", "venv"], cwd=project_path)
            update_status(35, "🔧 Virtual environment created!")
        except Exception as e:
            error_msg = str(e)
            show_error("Error", f"Failed to create virtual environment: {error_msg}")
            update_status(35, f"❌ Error creating virtual environment", "red")
            app.after(0, lambda: create_btn.configure(state="normal", text="Create Project"))
            return
        
        # Ensure the virtual environment paths work for Windows and Linux
        venv_path = os.path.join(project_path, "venv")
        pip_path = os.path.join(venv_path, "Scripts", "pip.exe") if os.name == 'nt' else os.path.join(venv_path, "bin", "pip")
        python_path = os.path.join(venv_path, "Scripts", "python.exe") if os.name == 'nt' else os.path.join(venv_path, "bin", "python")
        
        # Step 4: Install dependencies (35-85%)
        update_status(35, "📦 Installing dependencies...")
        try:
            # Check if pip exists
            if not os.path.exists(pip_path):
                error_msg = f"Pip not found at: {pip_path}"
                raise FileNotFoundError(error_msg)
            
            # Upgrade pip first
            update_status(40, "📦 Upgrading pip...")
            subprocess.call([pip_path, "install", "--upgrade", "pip"])
            
            # Install each dependency with feedback
            dep_progress_base = 45
            dep_progress_step = 35 / len(DEPENDENCIES)  # 35% of progress bar for dependencies
            
            for idx, dep in enumerate(DEPENDENCIES):
                current_progress = dep_progress_base + (idx * dep_progress_step)
                update_status(
                    current_progress, 
                    f"📦 Installing {dep}... ({idx+1}/{len(DEPENDENCIES)})"
                )
                subprocess.call([pip_path, "install", dep])
                
                # Update progress after each dependency is installed
                update_status(
                    current_progress + dep_progress_step/2,  # Halfway through this dependency's allocation
                    f"📦 Installed {dep}!"
                )
        except Exception as e:
            error_msg = str(e)
            show_error("Error", f"Failed to install dependencies: {error_msg}")
            update_status(80, f"❌ Error installing dependencies", "red")
            app.after(0, lambda: create_btn.configure(state="normal", text="Create Project"))
            return
        
        # Step 5: Write requirements.txt (85-90%)
        update_status(85, "📄 Generating requirements.txt...")
        try:
            result = subprocess.run([pip_path, "freeze"], capture_output=True, text=True)
            with open(os.path.join(project_path, "requirements.txt"), "w") as req_file:
                req_file.write(result.stdout)
            update_status(90, "📄 Requirements.txt generated!")
        except Exception as e:
            error_msg = str(e)
            show_warning("Warning", f"Could not generate requirements.txt: {error_msg}")
            update_status(90, f"⚠️ Could not generate requirements.txt", "orange")
        
        # Step 6: Launch Flask App (90-95%)
        update_status(90, "✅ Setup complete! Launching Flask App...", "green")
        
        # Step 7: Final steps (95-100%)
        try:
            if os.name == 'nt':
                flask_process = subprocess.Popen(
                    [python_path, "run.py"],
                    cwd=project_path,
                    creationflags=subprocess.CREATE_NEW_CONSOLE
                )
            else:
                # For non-Windows platforms
                flask_process = subprocess.Popen(
                    [python_path, "run.py"],
                    cwd=project_path
                )
            
            update_status(95, "🚀 Starting Flask app...", "green")
            
            # Wait for server to start before opening browser
            time.sleep(4)  # Adjust as needed based on your server startup time
            
            if flask_process.poll() is None:
                update_status(100, "🎉 Project created successfully! App is running", "green")
                webbrowser.open('http://127.0.0.1:5000/')
                show_info(
                    "Success", 
                    f"🚀 Flask app for '{project_name}' is now running!\n\nURL: http://127.0.0.1:5000/"
                )
                
                # Launch VSCode if available
                try:
                    subprocess.Popen(["code.cmd", project_path])
                    update_status(100, "🎉 Project created successfully! Opening in VSCode...", "green")
                except:
                    update_status(100, "🎉 Project created successfully! (VSCode not found)", "green")
            else:
                show_error("Error", "Failed to start Flask app")
                update_status(100, "❌ Error starting Flask app", "red")
        except Exception as e:
            error_msg = str(e)
            show_error("Error", f"Failed to start Flask app:\n{error_msg}")
            update_status(100, f"❌ Error: {error_msg}", "red")
        
        # Hide progress bar after 3 seconds of showing completion
        app.after(3000, lambda: progress_bar.pack_forget())
        
        # Re-enable the create button
        app.after(0, lambda: create_btn.configure(state="normal", text="Create Project"))
            
    except Exception as e:
        error_msg = str(e)
        show_error("Error", f"Project creation failed:\n{error_msg}")
        app.after(0, lambda: status_label.configure(text=f"❌ Error: {error_msg}", text_color="red"))
        app.after(0, lambda: create_btn.configure(state="normal", text="Create Project"))
        app.after(3000, lambda: progress_bar.pack_forget())

def run_gui():
    """Initialize and run the GUI application."""
    # Set appearance mode and default color theme
    ctk.set_appearance_mode("System")  # or "Light" or "Dark"
    ctk.set_default_color_theme("blue")  # blue, green, dark-blue
    
    app = ctk.CTk()
    app.title("Flask Project Automator")
    app.geometry("850x650")
    app.minsize(750, 600)  # Set minimum window size
    
    # Try to load icon
    icon_path = "icon.ico"
    icon_image = None
    try:
        app.iconbitmap(icon_path)
        # Also load the icon for display in the UI
        if os.path.exists(icon_path):
            try:
                # For PIL/Pillow versions that support .ico directly
                icon_image = Image.open(icon_path)
            except:
                # Fallback icon if we can't load the .ico
                icon_image = None
    except:
        print("Icon not found, using default")
    
    # Create a consistent padding and style
    padding = {"padx": 20, "pady": 10}
    
    # Main container frame
    container = ctk.CTkFrame(app, fg_color="transparent")
    container.pack(fill="both", expand=True, padx=10, pady=10)
    
    # Header frame with app icon and title
    header_frame = ctk.CTkFrame(container, corner_radius=10, height=100)
    header_frame.pack(fill="x", pady=(0, 15))
    
    # Logo/icon and title in a horizontal layout
    logo_frame = ctk.CTkFrame(header_frame, fg_color="transparent")
    logo_frame.pack(fill="x", padx=20, pady=15)
    
    # Add app icon if available
    if icon_image:
        # Resize icon for display
        icon_size = (64, 64)
        icon_image = icon_image.resize(icon_size, Image.LANCZOS)
        icon_photo = ImageTk.PhotoImage(icon_image)
        
        icon_label = ctk.CTkLabel(logo_frame, text="", image=icon_photo)
        icon_label.image = icon_photo  # Keep a reference to prevent garbage collection
        icon_label.pack(side="left", padx=(0, 15))
    
    # Title and subtitle
    title_frame = ctk.CTkFrame(logo_frame, fg_color="transparent")
    title_frame.pack(side="left", fill="y", expand=True)
    
    title_label = ctk.CTkLabel(
        title_frame,
        text="Flask Project Automator",
        font=ctk.CTkFont(size=28, weight="bold")
    )
    title_label.pack(anchor="w")
    
    subtitle_label = ctk.CTkLabel(
        title_frame,
        text="Generate professional Flask projects with ease",
        font=ctk.CTkFont(size=14)
    )
    subtitle_label.pack(anchor="w")
    
    # Main content frame
    content_frame = ctk.CTkFrame(container, corner_radius=10)
    content_frame.pack(fill="both", expand=True)
    
    # Instructions
    instruction_frame = ctk.CTkFrame(content_frame, fg_color="transparent")
    instruction_frame.pack(fill="x", padx=20, pady=(20, 10))
    
    instruction_text = """
    This tool will create a complete Flask project structure with:
    • Flask application setup with Database Migrations and ORM, and User Authentication
    • Frontend templates with Tailwind CSS
    • Virtual environment with all dependencies
    • Git repository initialization
    """
    
    instruction_label = ctk.CTkLabel(
        instruction_frame,
        text=instruction_text,
        font=ctk.CTkFont(size=13),
        justify="left",
        wraplength=750
    )
    instruction_label.pack(anchor="w")
    
    # Separator
    separator = ctk.CTkFrame(content_frame, height=1, fg_color="gray75")
    separator.pack(fill="x", padx=20, pady=10)
    
    # Project details section title
    details_title = ctk.CTkLabel(
        content_frame,
        text="Project Details",
        font=ctk.CTkFont(size=16, weight="bold")
    )
    details_title.pack(anchor="w", padx=25, pady=(10, 5))
    
    # Input fields with better layout
    input_frame = ctk.CTkFrame(content_frame, fg_color="transparent")
    input_frame.pack(fill="x", padx=20, pady=10)
    
    # Project name
    project_label = ctk.CTkLabel(
        input_frame, 
        text="Project Name:",
        font=ctk.CTkFont(size=13)
    )
    project_label.grid(row=0, column=0, sticky="w", pady=10)
    
    project_entry = ctk.CTkEntry(
        input_frame, 
        width=300, 
        placeholder_text="Enter project name (e.g., my_flask_app)"
    )
    project_entry.grid(row=0, column=1, sticky="ew", pady=10, padx=(10, 0))
    
    # Directory selection
    dir_label = ctk.CTkLabel(
        input_frame, 
        text="Project Location:",
        font=ctk.CTkFont(size=13)
    )
    dir_label.grid(row=1, column=0, sticky="w", pady=10)
    
    dir_frame = ctk.CTkFrame(input_frame, fg_color="transparent")
    dir_frame.grid(row=1, column=1, sticky="ew", pady=10, padx=(10, 0))
    
    dir_entry = ctk.CTkEntry(
        dir_frame, 
        placeholder_text="Select a directory for your project"
    )
    dir_entry.pack(side="left", fill="x", expand=True)
    
    browse_btn = ctk.CTkButton(
        dir_frame,
        text="Browse",
        command=lambda: browse_folder(dir_entry),
        width=100,
        height=30,
        font=ctk.CTkFont(size=13)
    )
    browse_btn.pack(side="right", padx=(10, 0))
    
    # Add grid configuration to make resizing work properly
    input_frame.columnconfigure(1, weight=1)
    
    # Separator
    separator2 = ctk.CTkFrame(content_frame, height=1, fg_color="gray75")
    separator2.pack(fill="x", padx=20, pady=10)
    
    # Progress section
    progress_frame = ctk.CTkFrame(content_frame, fg_color="transparent")
    progress_frame.pack(fill="x", padx=20, pady=10)
    
    status_label = ctk.CTkLabel(
        progress_frame, 
        text="Ready to create project",
        font=ctk.CTkFont(size=13),
        text_color="grey"
    )
    status_label.pack(pady=(0, 5))
    
    # Create the progress bar but don't pack it yet - it will be shown during project creation
    progress_bar = ctk.CTkProgressBar(progress_frame)
    progress_bar.set(0)
    
    # Create button
    button_frame = ctk.CTkFrame(content_frame, fg_color="transparent")
    button_frame.pack(fill="x", padx=20, pady=(10, 20))
    
    create_btn = ctk.CTkButton(
        button_frame,
        text="Create Project",
        font=ctk.CTkFont(size=15, weight="bold"),
        height=40,
        command=lambda: start_creation(
            project_entry.get(), 
            dir_entry.get(), 
            progress_bar,
            status_label, 
            create_btn, 
            app
        )
    )
    create_btn.pack(pady=10)
    
    # Footer with version and copyright
    footer_frame = ctk.CTkFrame(container, fg_color="transparent", height=30)
    footer_frame.pack(fill="x", pady=(10, 0))
    
    footer_text = ctk.CTkLabel(
        footer_frame,
        text="Flask Project Automator v2.0.0 | 2025 | Anthony Dinunzio",
        font=ctk.CTkFont(size=11),
        text_color="gray"
    )
    footer_text.pack(side="right", padx=10)
    
    # Mode switch (light/dark)
    def change_appearance_mode():
        current_mode = ctk.get_appearance_mode()
        new_mode = "Dark" if current_mode == "Light" else "Light"
        ctk.set_appearance_mode(new_mode)
        mode_switch.configure(text=f"{'🌙' if new_mode == 'Dark' else '☀️'} {new_mode} Mode")
    
    mode_switch = ctk.CTkButton(
        footer_frame,
        text=f"{'🌙' if ctk.get_appearance_mode() == 'Dark' else '☀️'} {ctk.get_appearance_mode()} Mode",
        font=ctk.CTkFont(size=11),
        width=100,
        height=25,
        command=change_appearance_mode
    )
    mode_switch.pack(side="left", padx=10)
    
    app.mainloop()

if __name__ == "__main__":
    run_gui()