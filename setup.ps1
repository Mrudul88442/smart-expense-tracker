#!/usr/bin/env pwsh
Write-Host "Creating virtual environment (venv)..."
python -m venv venv
Write-Host "Activating venv..."
.\venv\Scripts\Activate.ps1
Write-Host "Upgrading pip and installing dependencies from requirements.txt..."
pip install --upgrade pip
pip install -r requirements.txt
Write-Host "Requirements installed."
Write-Host "If you want to configure environment variables, copy .env.example to .env and edit it."
if (-not (Test-Path -Path .env)) {
    Copy-Item -Path .env.example -Destination .env
    Write-Host "Created .env from .env.example. Edit .env to add your real secrets (e.g. DJANGO_SECRET_KEY)."
}
Write-Host "Applying database migrations..."
.
\venv\Scripts\Activate.ps1
python .\expense_tracker_proj\manage.py migrate
Write-Host "Done. You can run the server using 'run_dev.ps1' or 'python manage.py runserver'."