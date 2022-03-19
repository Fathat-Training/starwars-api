#!/bin/bash

set -e

export PYTHONPATH=/app:$PYTHONPATH

cd /app/

echo "Setting up database"
python database/mysql/setup.py

echo "Running server"
python main.py
