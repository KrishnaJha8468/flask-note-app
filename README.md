# Flask Note App 📝

A simple, secure note-taking web app built with Flask.

## Features
- User registration and login
- Secure password storage (hashing)
- Create and view personal notes
- Logout functionality

## Setup Instructions

```bash
# Clone the repo
git clone https://github.com/KrishnaJha8468/flask-note-app.git

# Navigate to the project
cd flask-note-app

# Create virtual environment
python -m venv venv
venv\Scripts\activate  # On Windows

# Install dependencies
pip install flask

# Initialize database
python init_db.py

# Run the app
python app.py
