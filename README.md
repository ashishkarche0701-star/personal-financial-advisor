# FinAI — Personal Financial Advisor

A full-stack Flask personal finance management application for tracking income, expenses, budgets, and savings goals, with a financial dashboard, reporting, and AI-assisted financial insights.

## Features

- User registration, login, logout, and protected routes
- Password hashing and CSRF protection
- Income tracking
- Expense tracking and categories
- Monthly budget planning
- Savings goals and progress tracking
- Financial dashboard with Chart.js visualizations
- Monthly reports and CSV export
- OpenAI and Gemini integration
- Local rule-based AI fallback when no AI API key is configured
- SQLite by default with PostgreSQL-ready configuration
- Responsive web interface

## Tech Stack

- Python
- Flask
- Flask-SQLAlchemy
- Flask-Login
- Flask-WTF
- Jinja2
- SQLite / PostgreSQL
- Chart.js
- OpenAI / Gemini APIs

## Run locally

### 1. Create a virtual environment

```bash
python -m venv .venv
```

### 2. Install dependencies

Windows PowerShell (works even when PowerShell script activation is restricted):

```powershell
.venv\Scripts\python.exe -m pip install -r requirements.txt
```

Windows Command Prompt:

```bat
.venv\Scripts\activate.bat
pip install -r requirements.txt
```

Linux/macOS:

```bash
source .venv/bin/activate
pip install -r requirements.txt
```

### 3. Configure environment variables

Copy `.env.example` to `.env` and set a secure secret key. AI API keys are optional because the application has a local rule-based fallback.

### 4. Start the application

```bash
.venv\Scripts\python.exe app.py
```

Or, if the virtual environment is activated:

```bash
python app.py
```

Then open:

`http://127.0.0.1:5000`

## AI setup

For live AI-generated recommendations, add either an OpenAI API key or Gemini API key to your local `.env` file. If neither is configured, FinAI uses its local rule-based fallback.

**Never commit `.env`, API keys, passwords, or local database files to GitHub.**

## Project structure

```text
app.py
config.py
extensions.py
models.py
routes/
  auth.py
  main.py
  api.py
services/
  finance_service.py
  ai_service.py
templates/
static/
requirements.txt
.env.example
README.md
```

## Project scope

FinAI brings together authentication, financial tracking, budgeting, savings goals, analytics/reporting, AI-assisted recommendations, database processing, and frontend/backend integration in one Flask application.

## Submission

This repository contains the source code for the FinAI Personal Financial Advisor project. Clone the repository, install the dependencies, configure `.env` locally, and run the Flask application using the instructions above.

For public deployment, use a production secret, production database, HTTPS, and the required AI credentials. The included configuration is intended for local development and academic demonstration.
