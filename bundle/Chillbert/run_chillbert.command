#!/bin/bash

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
