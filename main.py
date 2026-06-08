import sqlite3
import json
from bambooapi import Bamboo, Response

DB_PATH = "/home/axiomapi/notes.db"

def get_db():
    db = sqlite3.connect(DB_PATH, timeout=5.0)
    db.row_factory = sqlite3.Row
    return db

def init_db():
    db = get_db()
    db.execute("""
        CREATE TABLE IF NOT EXISTS notes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            data TEXT NOT NULL
        )
    """)
    db.commit()
    db.close()

init_db()

app = Bamboo(title="Notes API", version="0.1.2")


@app.middleware
async def timer(request, next):
    """Log method, path, and response time for every request."""
    import time
    t0 = time.monotonic()
    response = await next(request)
    ms = round((time.monotonic() - t0) * 1000, 1)
    print(f"[bamboo] {request.method} {request.path} {ms}ms")
    return response


@app.get("/", responses={200: "Welcome message"})
async def home(request):
    """Welcome message."""
    return {"message": "Hello from Bamboo"}


@app.get("/health", responses={200: "Service is healthy"})
async def health(request):
    """Health check for the service."""
    return {"status": "ok"}


@app.get("/notes", responses={200: "List of all notes"}, query={"limit": "integer", "offset": "integer"})
async def list_notes(request):
    """List all notes."""
    try:
        limit = int(request.query_params.get("limit", 100))
        offset = int(request.query_params.get("offset", 0))
    except ValueError:
        return Response({"error": "limit and offset must be integers"}, status=400)
    db = get_db()
    rows = db.execute("SELECT id, data FROM notes ORDER BY id LIMIT ? OFFSET ?", (limit, offset)).fetchall()
    db.close()
    notes = {str(row["id"]): json.loads(row["data"]) for row in rows}
    return {"notes": notes, "limit": limit, "offset": offset}


@app.post("/notes", responses={201: "Note created", 400: "Invalid or missing JSON body"})
async def create_note(request):
    """Create a new note from a JSON body."""
    data = await request.json()
    if data is None:
        return Response({"error": "expected a JSON body"}, status=400)
    db = get_db()
    cursor = db.execute("INSERT INTO notes (data) VALUES (?)", (json.dumps(data),))
    db.commit()
    note_id = cursor.lastrowid
    db.close()
    return Response({"id": note_id, "note": data}, status=201)


@app.get("/notes/{note_id}", responses={200: "Note found", 404: "Note not found"})
async def get_note(request, note_id):
    """Fetch a single note by its id."""
    db = get_db()
    row = db.execute("SELECT id, data FROM notes WHERE id = ?", (note_id,)).fetchone()
    db.close()
    if row is None:
        return Response({"error": "note not found"}, status=404)
    return {"id": row["id"], "note": json.loads(row["data"])}


@app.put("/notes/{note_id}", responses={200: "Note updated", 400: "Invalid or missing JSON body", 404: "Note not found"})
async def update_note(request, note_id):
    """Replace a note entirely with a new JSON body."""
    db = get_db()
    row = db.execute("SELECT id FROM notes WHERE id = ?", (note_id,)).fetchone()
    if row is None:
        db.close()
        return Response({"error": "note not found"}, status=404)
    data = await request.json()
    if data is None:
        db.close()
        return Response({"error": "expected a JSON body"}, status=400)
    db.execute("UPDATE notes SET data = ? WHERE id = ?", (json.dumps(data), note_id))
    db.commit()
    db.close()
    return {"id": note_id, "note": data}


@app.delete("/notes/{note_id}", responses={200: "Note deleted", 404: "Note not found"})
async def delete_note(request, note_id):
    """Delete a note by its id."""
    db = get_db()
    row = db.execute("SELECT id FROM notes WHERE id = ?", (note_id,)).fetchone()
    if row is None:
        db.close()
        return Response({"error": "note not found"}, status=404)
    db.execute("DELETE FROM notes WHERE id = ?", (note_id,))
    db.commit()
    db.close()
    return Response({"deleted": True, "id": note_id}, status=200)
