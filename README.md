# Evently — Minimal Event Management App

**Stack:** Flask (Python), SQLite, SQLAlchemy, Flask-Login, Bootstrap 5

## Quick Start


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
