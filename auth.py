from flask import Blueprint, request, jsonify
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
from models import db, User

auth_bp = Blueprint("auth", __name__, url_prefix="/auth")

login_manager = LoginManager()
login_manager.login_view = "pages.login"

@login_manager.user_loader
def load_user(user_id):
    return db.session.get(User, int(user_id))

@auth_bp.post("/register")
def register():
    data = request.get_json(silent=True) or request.form.to_dict()
    name = (data.get("name") or "").strip()
    email = (data.get("email") or "").strip().lower()
    password = data.get("password") or ""

    errors = {}
    if not name:
        errors["name"] = "Name is required."
    if not email:
        errors["email"] = "Email is required."
    if not password or len(password) < 6:
        errors["password"] = "Password must be at least 6 characters."

    if errors:
        return jsonify({"ok": False, "errors": errors}), 400

    if db.session.query(User).filter_by(email=email).first():
        return jsonify({"ok": False, "errors": {"email": "Email already registered."}}), 409

    user = User(name=name, email=email, password_hash=generate_password_hash(password))
    db.session.add(user)
    db.session.commit()
    login_user(user)
    return jsonify({"ok": True, "message": "Registered and logged in.", "user": {"id": user.id, "name": user.name, "email": user.email}}), 201

@auth_bp.post("/login")
def login():
    data = request.get_json(silent=True) or request.form.to_dict()
    email = (data.get("email") or "").strip().lower()
    password = data.get("password") or ""

    user = db.session.query(User).filter_by(email=email).first()
    if not user or not check_password_hash(user.password_hash, password):
        return jsonify({"ok": False, "errors": {"general": "Invalid email or password."}}), 401

    login_user(user)
    return jsonify({"ok": True, "message": "Logged in.", "user": {"id": user.id, "name": user.name, "email": user.email}}), 200

@auth_bp.post("/logout")
@login_required
def logout():
    logout_user()
    return jsonify({"ok": True, "message": "Logged out."}), 200
