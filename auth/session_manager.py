import json
from datetime import datetime, timedelta
from config import SESSION_FILE, SESSION_MAX_AGE_HOURS


def save_session(cookies: list):
    data = {
        "saved_at": datetime.now().isoformat(),
        "cookies": cookies,
    }
    SESSION_FILE.write_text(json.dumps(data, indent=2))
    print(f"Session saved to {SESSION_FILE}")


def load_session() -> list | None:
    if not SESSION_FILE.exists():
        return None
    try:
        data = json.loads(SESSION_FILE.read_text())
        saved_at = datetime.fromisoformat(data["saved_at"])
        age = datetime.now() - saved_at
        if age > timedelta(hours=SESSION_MAX_AGE_HOURS):
            print(f"Saved session is {int(age.total_seconds() / 3600)}h old (limit: {SESSION_MAX_AGE_HOURS}h). Need to re-login.")
            return None
        print(f"Loaded session from {SESSION_FILE} (saved {int(age.total_seconds() / 60)}m ago)")
        return data["cookies"]
    except Exception as e:
        print(f"Could not load session: {e}")
        return None


def clear_session():
    if SESSION_FILE.exists():
        SESSION_FILE.unlink()
        print(f"Session cleared: {SESSION_FILE}")
