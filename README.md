<img width="940" height="529" alt="image" src="https://github.com/user-attachments/assets/5e890ea6-ab01-4391-9085-60c6ca4f0b83" />
<img width="940" height="529" alt="image" src="https://github.com/user-attachments/assets/34d33497-9b8a-4b27-9e6d-105961755d08" />
<img width="940" height="529" alt="image" src="https://github.com/user-attachments/assets/effff466-5ce3-4199-8662-f5b799508674" />
<img width="940" height="529" alt="image" src="https://github.com/user-attachments/assets/e81c0501-cf93-452d-9000-71ddc5f78813" />
<img width="940" height="529" alt="image" src="https://github.com/user-attachments/assets/bfcb021c-e32d-48ce-be4f-3569596dca1c" />
<img width="940" height="529" alt="image" src="https://github.com/user-attachments/assets/fa142d42-3cce-4e71-8780-366160873da2" />
<img width="940" height="529" alt="image" src="https://github.com/user-attachments/assets/598daccd-7fe5-4bb5-867e-c629ebec2626" />







# smart Expense Tracker

A Django-based personal expense tracking application with support for multiple financial features including expenses, income, savings, investment goals, mutual funds, and an AI financial advisor.
# smart Expense Tracker

A Django-based personal expense tracking application with support for multiple financial features including expenses, income, savings, investment goals, mutual funds, and an AI financial advisor.

## Features

- **Expense Tracking**: Log and categorize daily expenses
- **Income Management**: Track multiple income sources
- **Savings Goals**: Set and monitor savings targets
- **Investment Targets**: Track financial targets with status monitoring
- **Mutual Funds**: Search and manage mutual fund investments
- **AI Financial Advisor**: Get AI-powered financial insights (requires Google Gemini API)
- **User Authentication**: Secure login and registration
- **Dashboard**: Comprehensive financial overview

## Tech Stack

- **Backend**: Django 5.2.7
- **Database**: SQLite
- **Frontend**: HTML, CSS, JavaScript
- **API Integration**: Mutual Funds API (api.mfapi.in)
- **AI**: Google Gemini (optional)

## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/expense_tracker.git
   cd expense_tracker
   ```

2. Create and activate virtual environment:
   ```bash
   python -m venv venv
   .\venv\Scripts\Activate.ps1  # On Windows
   source venv/bin/activate      # On macOS/Linux
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Apply database migrations:
   ```bash
   cd expense_tracker_proj
   python manage.py migrate
   ```

5. Create a superuser:
   ```bash
   python manage.py createsuperuser
   ```

6. Run the development server:
   ```bash
   python manage.py runserver
   ```

7. Open your browser and visit: `http://127.0.0.1:8000/`

## Environment Variables

For AI features, set the following environment variable:

```powershell
# On Windows PowerShell
$env:FINANCIAL_AI_API_KEY = "your_google_gemini_api_key"

# Or permanently (Windows)
setx FINANCIAL_AI_API_KEY "your_google_gemini_api_key"
```

## Project Structure

```
expense_tracker/
├── expense_tracker_proj/      # Django project root
│   ├── manage.py
│   ├── settings.py            # Project settings
│   ├── urls.py                # URL routing
│   ├── wsgi.py
2. Create and activate virtual environment (or use the included `setup.ps1` script for Windows):
│   ├── home/                  # Home/dashboard app
   # On Windows you can run the provided script:
   .\setup.ps1

   # Or do it manually:
   python -m venv venv
   .\venv\Scripts\Activate.ps1  # On Windows
   source venv/bin/activate      # On macOS/Linux
│   ├── accounts/              # User authentication
│   ├── todos/                 # Todo/reminders app
│   ├── mutualfunds/           # Mutual funds app
│   ├── financial_ai/          # AI advisor app
│   ├── templates/             # HTML templates
│   ├── static/                # CSS, JS, images
│   └── db.sqlite3             # SQLite database
├── venv/                      # Virtual environment (excluded from git)
├── .gitignore
├── README.md
└── requirements.txt
```

## Usage

### Add an Expense
1. Navigate to Expenses
2. Click "Add Expense"
3. Enter amount, category, and date
4. Submit

### Track Savings
1. Go to Savings section
2. Add savings goal with target amount and date
3. Monitor progress on dashboard

### View Investment Portfolio
For AI features and secure configuration, you should set environment variables. We provide a `.env.example` that you can copy to `.env`.

Example values to set (in `.env` file):
```
DJANGO_SECRET_KEY=your-secret-key-here
DJANGO_DEBUG=True
DJANGO_ALLOWED_HOSTS=127.0.0.1,localhost
FINANCIAL_AI_API_KEY=your_google_gemini_api_key
```

On Windows PowerShell you can set the environment variable for a single session:

```powershell
$env:FINANCIAL_AI_API_KEY = "your_google_gemini_api_key"
```

Or permanently using `setx`:

```powershell
setx FINANCIAL_AI_API_KEY "your_google_gemini_api_key"
```
2. Search for funds
3. Add funds to portfolio
4. Monitor current NAV and profit/loss

### Use AI Advisor
1. Set `FINANCIAL_AI_API_KEY` environment variable
2. Install Google Gemini SDK: `pip install google-genai`
3. Chat with AI for financial insights

## API Integration

### Mutual Funds API
- Endpoint: `https://api.mfapi.in/mf`
- No authentication required
- Provides real-time mutual fund data and NAV

The app includes resilient request handling with:
- 5-second request timeout
- Automatic retries on failure
- Graceful fallback when API is unavailable

## Development

### Running Tests
```bash
python manage.py test
```

### Creating Migrations
```bash
python manage.py makemigrations
python manage.py migrate
```

### Collecting Static Files
```bash
python manage.py collectstatic
```

## Known Issues & Limitations

- Mutual Funds API may timeout during high traffic
- AI features require valid Google Gemini API key
- Some fund metadata uses placeholder values

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is licensed under the MIT License - see LICENSE file for details.

## Support

For issues or questions, please open an issue on GitHub.

## Author

Created with Django and ❤️
