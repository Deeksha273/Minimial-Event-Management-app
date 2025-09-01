# Evently — Minimal Event Management App

**Stack:** Flask (Python), SQLite, SQLAlchemy, Flask-Login, Bootstrap 5

## execution steps
1. Create Virtual Environment (only once per project)
python -m venv venv
- This creates a venv folder where all your project’s packages will be stored.
(You do this only once unless you delete the folder.)

2. Activate Virtual Environment (every time you start working)
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope Process
.\venv\Scripts\Activate.ps1
- This tells VS Code/terminal to use the Python interpreter inside your project’s venv.
- You must activate the venv each time you open a new terminal/session.

3. Install Required Packages (only once, unless new ones are needed)
pip install -r requirements.txt
- Once installed inside your venv, they remain there until you delete venv.
- No need to reinstall every time.

4. Run Your Project
python app.py

- When you run python app.py
  - you’ll usually see output like this:
 * Running on http://127.0.0.1:5000
 * Press CTRL+C to quit
 - That means your Flask app is now running on port 5000 of your local machine.

## Features
- Register/Login (secure password hashing)
- Create, Read, Update, Delete events (ownership enforced)
- Public event list (title, date/time, city)
- REST API:
  - POST /auth/register
  - POST /auth/login
  - GET /events
  - GET /events/:id
  - POST /events (auth)
  - PUT /events/:id (owner)
  - DELETE /events/:id (owner)
- Frontend: server-rendered pages + Bootstrap 5
- Basic tests with pytest

## Notes
- Uses session cookie for auth (spec allows session or JWT).
- Input validation on server; HTML constraints on forms.
- You can switch DB by editing `DATABASE_URL` in `.env`.
