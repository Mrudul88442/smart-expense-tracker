#!/usr/bin/env pwsh
if (-not (Test-Path -Path .\venv\Scripts\Activate.ps1)) {
    Write-Host "Virtual environment not found. Run './setup.ps1' first or create a venv." -ForegroundColor Red
    exit 1
}
.\venv\Scripts\Activate.ps1
Write-Host "Activating virtual env and running Django dev server"
Write-Host "Make sure you have set environment variables (e.g., .env file)."
# You can run the server directly; this will use the environment variables loaded by python-dotenv in settings.py
python .\expense_tracker_proj\manage.py runserver