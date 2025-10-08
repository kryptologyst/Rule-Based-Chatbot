#!/usr/bin/env python3
"""
Deployment script for Modern Rule-Based Chatbot
"""
import os
import sys
import subprocess
import shutil
from pathlib import Path

def check_requirements():
    """Check if all requirements are met"""
    print("Checking requirements...")
    
    # Check Python version
    if sys.version_info < (3, 7):
        print("❌ Python 3.7 or higher is required")
        return False
    
    print(f"✅ Python {sys.version_info.major}.{sys.version_info.minor} detected")
    
    # Check if required files exist
    required_files = [
        "chatbot.py",
        "app.py",
        "requirements.txt",
        "templates/index.html",
        "config.py"
    ]
    
    for file in required_files:
        if not os.path.exists(file):
            print(f"❌ Required file missing: {file}")
            return False
        print(f"✅ Found: {file}")
    
    return True

def install_dependencies():
    """Install production dependencies"""
    print("\nInstalling dependencies...")
    try:
        subprocess.check_call([
            sys.executable, "-m", "pip", "install", 
            "-r", "requirements.txt", "--upgrade"
        ])
        print("✅ Dependencies installed successfully")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Failed to install dependencies: {e}")
        return False

def setup_environment():
    """Setup production environment"""
    print("\nSetting up environment...")
    
    # Create production .env file
    env_content = """# Production Configuration
SECRET_KEY=your-production-secret-key-here
DEBUG=False
HOST=0.0.0.0
PORT=5000
DATABASE_PATH=chatbot.db
LOG_LEVEL=WARNING
LOG_FILE=chatbot.log
"""
    
    if not os.path.exists(".env.production"):
        with open(".env.production", "w") as f:
            f.write(env_content)
        print("✅ Created production environment file")
    
    # Create logs directory
    Path("logs").mkdir(exist_ok=True)
    print("✅ Created logs directory")
    
    return True

def run_tests():
    """Run test suite"""
    print("\nRunning tests...")
    try:
        result = subprocess.run([
            sys.executable, "-m", "pytest", "tests/", "-v", "--tb=short"
        ], capture_output=True, text=True)
        
        if result.returncode == 0:
            print("✅ All tests passed")
            return True
        else:
            print("❌ Some tests failed:")
            print(result.stdout)
            print(result.stderr)
            return False
    except FileNotFoundError:
        print("⚠️  pytest not found, skipping tests")
        return True

def create_startup_scripts():
    """Create startup scripts for different platforms"""
    print("\nCreating startup scripts...")
    
    # Linux/Mac startup script
    startup_script = """#!/bin/bash
# Modern Rule-Based Chatbot Startup Script

# Activate virtual environment if it exists
if [ -d "venv" ]; then
    source venv/bin/activate
fi

# Set environment variables
export FLASK_ENV=production
export FLASK_APP=app.py

# Start the application
echo "Starting Modern Rule-Based Chatbot..."
python app.py
"""
    
    with open("start.sh", "w") as f:
        f.write(startup_script)
    os.chmod("start.sh", 0o755)
    print("✅ Created start.sh")
    
    # Windows startup script
    windows_script = """@echo off
REM Modern Rule-Based Chatbot Startup Script

REM Activate virtual environment if it exists
if exist venv\\Scripts\\activate.bat (
    call venv\\Scripts\\activate.bat
)

REM Set environment variables
set FLASK_ENV=production
set FLASK_APP=app.py

REM Start the application
echo Starting Modern Rule-Based Chatbot...
python app.py
pause
"""
    
    with open("start.bat", "w") as f:
        f.write(windows_script)
    print("✅ Created start.bat")
    
    return True

def create_docker_files():
    """Create Docker configuration files"""
    print("\nCreating Docker files...")
    
    # Dockerfile
    dockerfile_content = """FROM python:3.9-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \\
    gcc \\
    && rm -rf /var/lib/apt/lists/*

# Copy requirements and install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . .

# Create non-root user
RUN useradd -m -u 1000 chatbot && chown -R chatbot:chatbot /app
USER chatbot

# Expose port
EXPOSE 5000

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \\
    CMD curl -f http://localhost:5000/health || exit 1

# Start application
CMD ["python", "app.py"]
"""
    
    with open("Dockerfile", "w") as f:
        f.write(dockerfile_content)
    print("✅ Created Dockerfile")
    
    # Docker Compose file
    compose_content = """version: '3.8'

services:
  chatbot:
    build: .
    ports:
      - "5000:5000"
    environment:
      - FLASK_ENV=production
      - SECRET_KEY=your-production-secret-key
    volumes:
      - ./data:/app/data
      - ./logs:/app/logs
    restart: unless-stopped
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost:5000/health"]
      interval: 30s
      timeout: 10s
      retries: 3
"""
    
    with open("docker-compose.yml", "w") as f:
        f.write(compose_content)
    print("✅ Created docker-compose.yml")
    
    return True

def create_systemd_service():
    """Create systemd service file for Linux systems"""
    print("\nCreating systemd service...")
    
    service_content = """[Unit]
Description=Modern Rule-Based Chatbot
After=network.target

[Service]
Type=simple
User=chatbot
WorkingDirectory=/opt/chatbot
Environment=FLASK_ENV=production
Environment=SECRET_KEY=your-production-secret-key
ExecStart=/usr/bin/python3 app.py
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
"""
    
    with open("chatbot.service", "w") as f:
        f.write(service_content)
    print("✅ Created chatbot.service")
    
    return True

def main():
    """Main deployment function"""
    print("🚀 Modern Rule-Based Chatbot Deployment")
    print("=" * 50)
    
    # Check requirements
    if not check_requirements():
        print("\n❌ Requirements check failed")
        sys.exit(1)
    
    # Install dependencies
    if not install_dependencies():
        print("\n❌ Dependency installation failed")
        sys.exit(1)
    
    # Setup environment
    if not setup_environment():
        print("\n❌ Environment setup failed")
        sys.exit(1)
    
    # Run tests
    if not run_tests():
        print("\n⚠️  Tests failed, but continuing with deployment")
    
    # Create startup scripts
    create_startup_scripts()
    
    # Create Docker files
    create_docker_files()
    
    # Create systemd service
    create_systemd_service()
    
    print("\n" + "=" * 50)
    print("✅ Deployment completed successfully!")
    print("\nTo start the chatbot:")
    print("  Linux/Mac: ./start.sh")
    print("  Windows: start.bat")
    print("  Docker: docker-compose up -d")
    print("\nTo install as systemd service:")
    print("  sudo cp chatbot.service /etc/systemd/system/")
    print("  sudo systemctl enable chatbot")
    print("  sudo systemctl start chatbot")
    print("\nThe chatbot will be available at: http://localhost:5000")

if __name__ == "__main__":
    main()
