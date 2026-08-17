import json
from pathlib import Path
from fastapi import FastAPI
from fastapi.responses import HTMLResponse, JSONResponse

app = FastAPI(title="AI Orbit Data Ingestion API")

BASE_DIR = Path(__file__).resolve().parent
ENTITIES_PATH = BASE_DIR / "data" / "entities.json"
RELATIONSHIPS_PATH = BASE_DIR / "data" / "relationships.json"

def load_json(path: Path):
    if not path.exists():
        return []
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)

@app.get("/", response_class=HTMLResponse)
def dashboard():
    entities = load_json(ENTITIES_PATH)
    relationships = load_json(RELATIONSHIPS_PATH)
    return f"""
    <!DOCTYPE html>
    <html>
    <head>
        <meta charset="utf-8">
        <title>AI Orbit Data Pipeline Viewer</title>
    </head>
    <body style="font-family: sans-serif; background: #0d1117; color: #c9d1d9; padding: 40px;">
        <h1 style="color: #58a6ff;">AI Orbit Ingestion Dashboard</h1>
        <p>Total Entities: <strong>{len(entities)}</strong> | Relationships: <strong>{len(relationships)}</strong></p>
        <p>
            <a href="/api/entities" style="color: #58a6ff;" target="_blank">/api/entities</a> | 
            <a href="/api/relationships" style="color: #58a6ff;" target="_blank">/api/relationships</a> | 
            <a href="/docs" style="color: #3fb950;" target="_blank">Interactive Swagger Docs</a>
        </p>
    </body>
    </html>
    """

@app.get("/api/entities")
def get_entities():
    return JSONResponse(content=load_json(ENTITIES_PATH))

@app.get("/api/relationships")
def get_relationships():
    return JSONResponse(content=load_json(RELATIONSHIPS_PATH))
