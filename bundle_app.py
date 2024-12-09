# bundle_app.py
import os
import shutil
import stat
import logging
from pathlib import Path
import subprocess

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class ApplicationBundler:
    """
    Creates a self-contained application bundle that can be distributed and run
    without requiring PyInstaller or dealing with conda conflicts.
    """
    def __init__(self):
        self.app_name = "Chillbert"
        self.bundle_dir = Path("bundle")
        self.app_dir = self.bundle_dir / self.app_name
        self.requirements_file = "requirements.txt"

    def create_directory_structure(self):
        """Creates the necessary directory structure for the bundle."""
        logger.info("Creating directory structure...")
        
        # Clean existing bundle if it exists
        if self.bundle_dir.exists():
            shutil.rmtree(self.bundle_dir)
        
        # Create new directory structure
        self.app_dir.mkdir(parents=True)
        (self.app_dir / "src").mkdir()
        (self.app_dir / "assets").mkdir()
        (self.app_dir / "venv").mkdir()
        (self.app_dir / "pages").mkdir()
        (self.app_dir / "logs").mkdir()

    def create_requirements(self):
        """Creates a requirements.txt file with essential dependencies."""
        requirements = [
            "streamlit",
            "pyaudio",
            "python-dotenv"
        ]
        
        with open(self.requirements_file, "w") as f:
            f.write("\n".join(requirements))

    def copy_application_files(self):
        """Copies all necessary application files to the bundle."""
        logger.info("Copying application files...")
        
        # Copy main application files
        shutil.copy2("app.py", self.app_dir)
        shutil.copy2("requirements.txt", self.app_dir)
        shutil.copy2(".env", self.app_dir)
        shutil.copy2("chillbert.gif", self.app_dir / "assets")
        shutil.copy2("ChillbertLogo-removebg-preview.png", self.app_dir)
        shutil.copy2("ChillbertLogo-removebg-preview.png", self.app_dir / "assets")
        #shutil.copytree("pages", self.app_dir)
        for file_name in os.listdir("pages"):
            full_file_name = os.path.join("pages", file_name)
            if os.path.isfile(full_file_name):  # Check if it's a file
                shutil.copy2(full_file_name, self.app_dir / "pages")
        
        
        # Copy source files
        for src_file in ["authenticator.py", "connection.py","analyse_chat.py","chatbot.py","fileprocessing.py","messanger.py"]:
            shutil.copy2(f"src/{src_file}", self.app_dir / "src")

    def create_launcher(self):
        """Creates a launcher script that sets up the environment and runs the application."""
        launcher_path = self.app_dir / "run_chillbert.command"
        
        launcher_content = """#!/bin/bash

# Get the directory where this script is located
DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"

# Function to log messages
log_message() {
    echo "[$(date '+%Y-%m-%d %H:%M:%S')] $1"
}

# Function to check Python installation
check_python() {
    if ! command -v python3 &> /dev/null; then
        log_message "Python 3 is required but not installed. Please install Python 3 and try again."
        exit 1
    fi
}

# Function to create virtual environment
setup_environment() {
    if [ ! -d "$DIR/venv" ]; then
        log_message "Setting up virtual environment..."
        python3 -m venv "$DIR/venv"
    fi
    
    # Activate virtual environment
    source "$DIR/venv/bin/activate"
    
    # Install requirements if needed
    if [ ! -f "$DIR/venv/requirements_installed" ]; then
        log_message "Installing required packages..."
        pip install streamlit pyaudio python-dotenv
        touch "$DIR/venv/requirements_installed"
    fi
}

# Function to run the application
run_app() {
    log_message "Starting Chillbert..."
    export PYTHONPATH="$DIR:$PYTHONPATH"
    cd "$DIR"
    streamlit run app.py
}

# Main execution
log_message "Initializing Chillbert..."
check_python
setup_environment
run_app
"""
        
        with open(launcher_path, "w") as f:
            f.write(launcher_content)
        
        # Make the launcher executable
        launcher_path.chmod(launcher_path.stat().st_mode | stat.S_IEXEC)

    def create_bundle(self):
        """Creates the complete application bundle."""
        try:
            logger.info("Starting bundle creation...")
            
            self.create_directory_structure()
            self.create_requirements()
            self.copy_application_files()
            self.create_launcher()
            
            # Create a zip archive of the bundle
            shutil.make_archive(
                base_name=self.app_name,
                format="zip",
                root_dir=self.bundle_dir,
                base_dir=self.app_name
            )
            
            logger.info(f"Bundle created successfully: {self.app_name}.zip")
            return True
            
        except Exception as e:
            logger.error(f"Failed to create bundle: {str(e)}")
            return False

if __name__ == "__main__":
    bundler = ApplicationBundler()
    bundler.create_bundle()