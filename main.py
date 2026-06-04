from bambooapi import Bamboo, Response

app = Bamboo(title="Notes API", version="0.1.1")

notes = {}
next_id = {"value": 1}


@app.get("/")
async def home(request):
    """Welcome message."""
    return {"message": "Hello from Bamboo"}


@app.get("/health")
async def health(request):
    """Health check for the service."""
    return {"status": "ok"}


@app.get("/notes")
async def list_notes(request):
    """List all notes."""
    return {"notes": notes}


@app.post("/notes")
async def create_note(request):
    """Create a new note from a JSON body."""
    data = await request.json()
    if data is None:
        return Response({"error": "expected a JSON body"}, status=400)
    note_id = next_id["value"]
    next_id["value"] += 1
    notes[str(note_id)] = data
    return Response({"id": note_id, "note": data}, status=201)


@app.get("/notes/{note_id}")
async def get_note(request, note_id):
    """Fetch a single note by its id."""
    note = notes.get(note_id)
    if note is None:
        return Response({"error": "note not found"}, status=404)
    return {"id": note_id, "note": note}


@app.put("/notes/{note_id}")
async def update_note(request, note_id):
    """Replace a note entirely with a new JSON body."""
    if note_id not in notes:
        return Response({"error": "note not found"}, status=404)
    data = await request.json()
    if data is None:
        return Response({"error": "expected a JSON body"}, status=400)
    notes[note_id] = data
    return {"id": note_id, "note": data}


@app.delete("/notes/{note_id}")
async def delete_note(request, note_id):
    """Delete a note by its id."""
    if note_id not in notes:
        return Response({"error": "note not found"}, status=404)
    del notes[note_id]
    return Response({"deleted": True, "id": note_id}, status=200)
