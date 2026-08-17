# AI Orbit Data Ingestion Pipeline

A production-grade, API-first bulk data ingestion pipeline built in Python to fetch, sanitize, resolve, and link AI ecosystem data across multiple entities.

## Architecture & Project Structure

```text
ai-orbit-ingestion/
│
├── data/                  # Output directory (entities.json, relationships.json)
├── src/
│   ├── discovery/         # Multi-source API/RSS ingestion modules
│   ├── processing/        # Data sanitization, URL normalization, entity resolution
│   ├── mapping/           # Graph relationship mapping engine
│   └── utils/             # Pydantic schemas and metadata models
└── run.py                 # Core pipeline orchestrator