#!/bin/bash

# Create virtual environment
echo "Creating virtual environment 'fifa-env'..."
python3 -m venv fifa-env

# Activate the environment
echo "Activating environment..."
source fifa-env/bin/activate

# Upgrade pip
echo "Upgrading pip..."
pip install --upgrade pip

# Install packages from requirements.txt
if [ -f requirements.txt ]; then
    echo "Installing dependencies from requirements.txt..."
    pip install -r requirements.txt
else
    echo "Error: requirements.txt not found."
    exit 1
fi

# Register Jupyter kernel
echo "Registering Jupyter kernel 'Python (FIFA)'..."
python -m ipykernel install --user --name=fifa-env --display-name "Python (FIFA)"

echo "Setup complete."
echo "To activate the environment later, run: source fifa-env/bin/activate"
