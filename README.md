# AI Personal Finance Advisor

A full-stack Flask personal finance management platform built from scratch for tracking income, expenses, budgets and savings, with dashboards, reporting and AI-powered financial insights.

## Features

- Secure registration, login, logout and protected routes
- Password hashing and CSRF protection
- Income tracking
- Expense tracking and categories
- Monthly budget planning
- Savings goals and progress
- Financial dashboard with Chart.js visualization
- Monthly reports and CSV export
- OpenAI and Gemini integration
- Rule-based AI fallback when no API key is configured
- SQLite by default and PostgreSQL-ready configuration
- Responsive web interface

## Tech Stack

Python, Flask, Flask-SQLAlchemy, Flask-Login, Flask-WTF, Jinja2, SQLite/PostgreSQL, Chart.js, OpenAI/Gemini APIs.

## Run locally

```bash
python -m venv .venv
```

Windows:

```bash
.venv\Scripts\activate
pip install -r requirements.txt
copy .env.example .env
python app.py
```

Linux/macOS:

```bash
source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
python app.py
```

Open `http://127.0.0.1:5000`.

## AI setup

Copy `.env.example` to `.env`. Add either an OpenAI API key or Gemini API key for live AI-generated recommendations. If neither is configured, the application automatically uses its local rule-based fallback.

Never commit `.env`, API keys, passwords, or database files.

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
tests/
requirements.txt
.env.example
```

## Scope

The project implements the major modules specified for an AI-powered personal finance and budgeting platform: authentication, financial tracking, budget management, AI recommendations, analytics/reporting, database processing, frontend/backend integration and testing.

For public deployment, configure a production secret, a production database, HTTPS and the required AI API credentials. Ngrok can be used for temporary demonstrations.
