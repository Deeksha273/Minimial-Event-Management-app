import os
from flask import Flask, jsonify
from flask_login import current_user
from dotenv import load_dotenv
from config import Config
from models import db
from auth import auth_bp, login_manager
from events import events_bp
from pages import pages_bp

def create_app():
    load_dotenv()
    app = Flask(__name__, static_folder="static", template_folder="templates")
    app.config.from_object(Config)

    db.init_app(app)
    login_manager.init_app(app)

    app.register_blueprint(auth_bp)
    app.register_blueprint(events_bp)
    app.register_blueprint(pages_bp)

    @app.errorhandler(400)
    @app.errorhandler(401)
    @app.errorhandler(403)
    @app.errorhandler(404)
    def handle_error(err):
        message = getattr(err, "description", str(err))
        return jsonify({"ok": False, "error": message}), err.code

    @app.get("/whoami")
    def whoami():
        if current_user.is_authenticated:
            return {"ok": True, "user": {"id": current_user.id, "email": current_user.email, "name": current_user.name}}
        return {"ok": True, "user": None}

    with app.app_context():
        db.create_all()

    return app

if __name__ == "__main__":
    app = create_app()
    app.run(host="0.0.0.0", port=5000, debug=True)
