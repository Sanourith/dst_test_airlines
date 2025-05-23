#!/bin/bash
# This script is used to begin work on Python over venv-infra profile
# (which is a lite version)

set -e

script_dir=$(dirname "$(readlink -f "$0")")
bin_dir="$script_dir/../bin"

echo "*****"
echo "Checking python installation..."
if ! command -v python3 &> /dev/null; then
    echo "Python3 needs to be installed. Launching..."
    sudo apt update && sudo apt install -y python3 python3-venv
else
    echo "Python3 is already installed."
fi
echo "*****"

echo ""

echo "*****"
echo "Checking utils & ssl-dev installation..."
if ! command -v apache2-utils &> /dev/null || ! dpkg -s libssl-dev &> /dev/null; then
    echo "Installing utilities..."
    sudo apt install -y apache2-utils libssl-dev
else
    echo "Utilities are already installed."
fi
echo "*****"

echo ""

VENV_DIR="$script_dir/venv-data"

if [ ! -d "$VENV_DIR" ]; then
    echo "Creating virtual environment in $VENV_DIR..."
    python3 -m venv "$VENV_DIR"
else
    echo "Using existing virtual environment in $VENV_DIR..."
fi

echo "*****"
source "$VENV_DIR/bin/activate"
echo "Virtual environment activated."

REQ_FILE="$script_dir/requirements.txt"

if [[ -f "$REQ_FILE" ]]; then
    echo "Checking dependencies installations..."
    pip install --upgrade pip -y
    pip install -r "$REQ_FILE"
    requirements="1"
else
    echo "No requirements.txt found at $REQ_FILE."
    requirements="0"
fi

echo ""
echo "*****"
echo "Preparing CLI interface..."
mkdir -p "$bin_dir"
for script in "$bin_dir"/*.py; do
    if [[ -f "$script" ]]; then
        script_name=$(basename "$script" .py)
        echo "Enabling script: $script"
        chmod +x "$script"
    fi
done

if ! grep -q "keepass" ~/.bashrc; then
    echo "Adding keepass alias into bashrc. 'keepass'"
    echo "alias keepass='$bin_dir/keepass_cli.py'" >> ~/.bashrc
else
    echo "'keepass' CLI has already got an alias."
fi

echo ""
echo "Reset bashrc file..."
if [ -f ~/.bashrc ]; then
    source ~/.bashrc
else
    echo "No ~/.bashrc file found."
fi

echo ""
echo "* * * * *"

echo "Installation complete."
echo "To activate, use 'source devops-venv/bin/activate'"

if [[ "$requirements" == "1" ]]; then
    echo "Everything turned well. Go on!"
else
    echo "Requirements are not installed yet [not found]"
    echo "Try launching 'pip install -r path/to/requirements.txt'"
fi
