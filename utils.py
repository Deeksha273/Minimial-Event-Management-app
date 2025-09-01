from datetime import datetime

def parse_iso_datetime(value: str):
    try:
        dt = datetime.fromisoformat(value)
        return dt, None
    except Exception:
        return None, "start_time must be a valid ISO 8601 datetime (e.g., 2025-08-27T18:30:00)"
    
def validate_event_payload(data: dict):
    errors = {}

    title = (data.get("title") or "").strip()
    if not (5 <= len(title) <= 100):
        errors["title"] = "Title must be between 5 and 100 characters."

    description = (data.get("description") or "").strip()
    if len(description) > 2000:
        errors["description"] = "Description must be at most 2000 characters."

    city = (data.get("city") or "").strip()
    if not city:
        errors["city"] = "City is required."

    organizer_name = (data.get("organizer_name") or "").strip()
    if not organizer_name:
        errors["organizer_name"] = "Organizer name is required."

    start_time_str = (data.get("start_time") or "").strip()
    dt, err = parse_iso_datetime(start_time_str)
    if err:
        errors["start_time"] = err

    return errors
