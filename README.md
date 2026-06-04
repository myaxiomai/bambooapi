# Bamboo

A lightweight, readable Python API framework. Simple by design.

Bamboo is an ASGI micro-framework you can read in one sitting and fully understand.
No magic. No hidden complexity. Just clean, honest Python.

## Install

```bash
pip install bambooapi
```

## Quickstart

```python
from bambooapi import Bamboo, Response

app = Bamboo()

@app.get("/")
async def home(request):
    """Welcome message."""
    return {"message": "Hello from Bamboo"}

@app.post("/notes")
async def create_note(request):
    """Create a note."""
    data = await request.json()
    return Response({"note": data}, status=201)
```

Run it:

```bash
uvicorn myapp:app
```

Then visit `http://localhost:8000/docs` for the interactive API docs.

## Features

- GET, POST, PUT, DELETE routing
- Path parameters: `/notes/{note_id}`
- Async request body and JSON parsing
- Auto-generated OpenAPI spec at `/openapi.json`
- Interactive docs page at `/docs`
- Zero dependencies beyond an ASGI server

## Philosophy

The entire framework fits in one file you can read in an afternoon.
If you can read it, you can understand it. If you can understand it, you can trust it.

## License

MIT
