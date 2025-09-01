from flask import Blueprint, request, jsonify, abort
from flask_login import login_required, current_user
from sqlalchemy import or_
from models import db, Event
from utils import validate_event_payload, parse_iso_datetime

events_bp = Blueprint("events", __name__, url_prefix="/events")

@events_bp.get("")
def list_events():
    q = (request.args.get("q") or "").strip()
    city = (request.args.get("city") or "").strip()
    query = db.session.query(Event)
    if q:
        ilike = f"%{q}%"
        query = query.filter(or_(Event.title.ilike(ilike), Event.description.ilike(ilike)))
    if city:
        query = query.filter(Event.city.ilike(city))
    events = query.order_by(Event.start_time.asc()).all()
    return jsonify([serialize_event(e) for e in events]), 200

@events_bp.get("/<int:event_id>")
def get_event(event_id):
    e = db.session.get(Event, event_id)
    if not e:
        abort(404, description="Event not found")
    return jsonify(serialize_event(e)), 200

@events_bp.post("")
@login_required
def create_event():
    data = request.get_json(silent=True) or request.form.to_dict()
    errors = validate_event_payload(data)
    if errors:
        return jsonify({"ok": False, "errors": errors}), 400

    start_dt, _ = parse_iso_datetime(data["start_time"])
    ev = Event(
        title=data["title"].strip(),
        description=(data.get("description") or "").strip(),
        city=data["city"].strip(),
        start_time=start_dt,
        organizer_name=data["organizer_name"].strip(),
        created_by=current_user.id
    )
    db.session.add(ev)
    db.session.commit()
    return jsonify({"ok": True, "event": serialize_event(ev)}), 201

@events_bp.put("/<int:event_id>")
@login_required
def update_event(event_id):
    ev = db.session.get(Event, event_id)
    if not ev:
        abort(404, description="Event not found")
    if ev.created_by != current_user.id:
        abort(403, description="You can only edit your own events")

    data = request.get_json(silent=True) or request.form.to_dict()
    errors = validate_event_payload(data)
    if errors:
        return jsonify({"ok": False, "errors": errors}), 400

    start_dt, _ = parse_iso_datetime(data["start_time"])
    ev.title = data["title"].strip()
    ev.description = (data.get("description") or "").strip()
    ev.city = data["city"].strip()
    ev.start_time = start_dt
    ev.organizer_name = data["organizer_name"].strip()
    db.session.commit()
    return jsonify({"ok": True, "event": serialize_event(ev)}), 200

@events_bp.delete("/<int:event_id>")
@login_required
def delete_event(event_id):
    ev = db.session.get(Event, event_id)
    if not ev:
        abort(404, description="Event not found")
    if ev.created_by != current_user.id:
        abort(403, description="You can only delete your own events")
    db.session.delete(ev)
    db.session.commit()
    return jsonify({"ok": True, "message": "Event deleted."}), 200

def serialize_event(e: Event):
    return {
        "id": e.id,
        "title": e.title,
        "description": e.description,
        "city": e.city,
        "start_time": e.start_time.isoformat(),
        "organizer_name": e.organizer_name,
        "created_by": e.created_by,
        "created_at": e.created_at.isoformat(),
    }
