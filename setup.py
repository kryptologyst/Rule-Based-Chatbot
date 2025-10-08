#!/usr/bin/env python3
"""
Setup script for Modern Rule-Based Chatbot
"""
import os
import sys
import subprocess
import sqlite3
from pathlib import Path

def check_python_version():
    """Check if Python version is compatible"""
    if sys.version_info < (3, 7):
        print("Error: Python 3.7 or higher is required")
        sys.exit(1)
    print(f"✓ Python {sys.version_info.major}.{sys.version_info.minor} detected")

def install_dependencies():
    """Install required dependencies"""
    print("Installing dependencies...")
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"])
        print("✓ Dependencies installed successfully")
    except subprocess.CalledProcessError:
        print("Error: Failed to install dependencies")
        sys.exit(1)

def create_directories():
    """Create necessary directories"""
    directories = ["logs", "data", "static"]
    for directory in directories:
        Path(directory).mkdir(exist_ok=True)
        print(f"✓ Created directory: {directory}")

def initialize_database():
    """Initialize the SQLite database"""
    print("Initializing database...")
    try:
        from chatbot import ModernRuleBasedChatbot
        chatbot = ModernRuleBasedChatbot("chatbot.db")
        print("✓ Database initialized successfully")
    except Exception as e:
        print(f"Error: Failed to initialize database: {e}")
        sys.exit(1)

def create_env_file():
    """Create .env file with default configuration"""
    env_content = """# Modern Rule-Based Chatbot Configuration
# Copy this file and modify as needed

# Database settings
DATABASE_PATH=chatbot.db

# Flask settings
SECRET_KEY=your-secret-key-here
DEBUG=True
HOST=0.0.0.0
PORT=5000

# Chatbot settings
MAX_CONVERSATION_HISTORY=10
CONFIDENCE_THRESHOLD=0.6

# Logging settings
LOG_LEVEL=INFO
LOG_FILE=chatbot.log
"""
    
    if not os.path.exists(".env"):
        with open(".env", "w") as f:
            f.write(env_content)
        print("✓ Created .env file")
    else:
        print("✓ .env file already exists")

def run_tests():
    """Run the test suite"""
    print("Running tests...")
    try:
        subprocess.check_call([sys.executable, "-m", "pytest", "tests/", "-v"])
        print("✓ All tests passed")
    except subprocess.CalledProcessError:
        print("Warning: Some tests failed")
    except FileNotFoundError:
        print("Warning: pytest not found, skipping tests")

def main():
    """Main setup function"""
    print("Setting up Modern Rule-Based Chatbot...")
    print("=" * 50)
    
    # Check Python version
    check_python_version()
    
    # Install dependencies
    install_dependencies()
    
    # Create directories
    create_directories()
    
    # Initialize database
    initialize_database()
    
    # Create environment file
    create_env_file()
    
    # Run tests
    run_tests()
    
    print("=" * 50)
    print("Setup completed successfully!")
    print("\nTo run the chatbot:")
    print("  Console mode: python chatbot.py")
    print("  Web interface: python app.py")
    print("\nTo run tests:")
    print("  python -m pytest tests/")
    print("\nTo view the web interface:")
    print("  Open http://localhost:5000 in your browser")

if __name__ == "__main__":
    main()
