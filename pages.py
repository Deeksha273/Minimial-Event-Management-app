from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user
from models import db, Event

pages_bp = Blueprint("pages", __name__)

@pages_bp.get("/")
def home():
    events = db.session.query(Event).order_by(Event.start_time.asc()).all()
    return render_template("index.html", events=events)

@pages_bp.get("/login")
def login():
    return render_template("login.html")

@pages_bp.get("/register")
def register():
    return render_template("register.html")

@pages_bp.get("/events/new")
@login_required
def new_event():
    return render_template("create_event.html")

@pages_bp.get("/events/<int:event_id>")
def view_event(event_id):
    ev = db.session.get(Event, event_id)
    if not ev:
        return render_template("404.html"), 404
    return render_template("detail.html", ev=ev)

@pages_bp.get("/events/<int:event_id>/edit")
@login_required
def edit_event(event_id):
    ev = db.session.get(Event, event_id)
    if not ev:
        return render_template("404.html"), 404
    if ev.created_by != current_user.id:
        flash("You can only edit your own events.", "danger")
        return redirect(url_for("pages.home"))
    return render_template("edit_event.html", ev=ev)
