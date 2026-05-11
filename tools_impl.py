import json, os, uuid
from datetime import datetime

NOTES_FILE = "notes.json"

def _load() -> list[dict]:
    if not os.path.exists(NOTES_FILE):
        return []
    with open(NOTES_FILE, "r", encoding="utf-8") as f:
        return json.load(f)

def _save(notes: list[dict]) -> None:
    with open(NOTES_FILE, "w", encoding="utf-8") as f:
        json.dump(notes, f, ensure_ascii=False, indent=2)

def save_note(content: str) -> dict:
    notes = _load()
    note = {
        "id": "n_" + uuid.uuid4().hex[:8],
        "content": content,
        "created_at": datetime.now().isoformat(timespec="seconds"),
    }
    notes.append(note)
    _save(notes)
    return {"ok": True, "id": note["id"]}

def list_notes() -> dict:
    notes = sorted(_load(), key=lambda n: n["created_at"], reverse=True)
    return {"ok": True, "count": len(notes), "notes": notes}