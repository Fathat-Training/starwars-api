#!/bin/bash

set -e

# Add /app to Python path for import statements find the scripts inside /app.
export PYTHONPATH=/app:$PYTHONPATH

echo "Setting up database"
python database/mysql/setup.py

echo "Running server"
python main.py
