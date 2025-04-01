#!/bin/bash

# Activate virtual environment if it exists
if [ -d "venv" ]; then
    source venv/bin/activate
fi

# Set PYTHONPATH to include the parent directory of the visual_curses package
export PYTHONPATH=$(dirname "$(pwd)")

# Run the Python program
python3 -m visual_curses.main
