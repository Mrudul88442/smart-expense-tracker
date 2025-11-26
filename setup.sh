#!/usr/bin/env bash
set -e
python3 -m venv venv
source venv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt
cp .env.example .env || true
python3 expense_tracker_proj/manage.py migrate
echo "Setup complete. Run 'source venv/bin/activate' and then 'python expense_tracker_proj/manage.py runserver'"