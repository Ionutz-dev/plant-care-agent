# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

Plant Care Card Generator — an AI pipeline that classifies a plant from an uploaded image, then generates a structured 18-field care card using a LangChain agent backed by a RAG database and optional web search.

## Commands

### Local Development
```bash
pip install -r requirements.txt

# First-time setup: build the LanceDB vector store
python scripts/build_vector_store.py

# Test the RAG system
python scripts/test_rag.py

# Start the API server (port 8000)
python main.py
# or with hot-reload
uvicorn api.app:app --reload

# Start the Streamlit frontend (port 8501)
streamlit run frontend/streamlit_app.py
```

### Docker
```bash
docker-compose up --build   # first time
docker-compose up           # subsequent runs
docker-compose down
docker-compose logs -f
```

### No automated test suite exists. Testing is done via `scripts/test_rag.py` and the API's `/health` endpoint.

## Architecture

### Request Pipeline
```
Image upload (Streamlit UI)
  → POST /predict (FastAPI)
  → VGG11 classifier → plant name + confidence
  → LangChain agent:
      1. query_plant_care_database (LanceDB RAG, 7 plants)
      2. search_plant_info (Tavily web search, fallback)
  → GPT-4o-mini → PlantCareCard (Pydantic, 18 fields)
  → JSON response rendered in Streamlit
```

### Key Components

**`api/app.py`** — FastAPI app with three endpoints (`/`, `/health`, `/predict`). The VGG11 model is loaded once at startup as a global. File uploads are validated as images before processing.

**`models/classifier.py`** — PyTorch Lightning VGG11 module. Features are frozen; only the custom classifier head (FC→ReLU→Dropout×2→FC(30)) is trained. Requires checkpoint at `models/checkpoints/best-vgg11-model-v3.ckpt` (~500 MB, not in repo).

**`agents/plant_care_agent.py`** — `generate_care_card(plant_name)` orchestrates the LangChain tool-calling agent. After the agent gathers information, a second LLM call with a structured output prompt produces the final `PlantCareCard`.

**`agents/tools.py`** — Two LangChain tools: `query_plant_care_database` (LanceDB similarity search with metadata filter on `plant_name`) and `search_plant_info` (Tavily API). LanceDB connection is a singleton.

**`schemas/plant_care_card.py`** — Pydantic `PlantCareCard` with 18 fields (latin_name, watering_schedule, toxicity, common_pests, etc.).

**`prompts/plant_care_prompts.py`** — Three prompts: system (botanist persona + tool priority), user (per-request template), and structured output (converts agent output → PlantCareCard fields).

**`config/config.py`** — All settings in one place: API keys from `.env`, model path, `NUM_CLASSES=30`, `LLM_MODEL="gpt-4o-mini"`, device auto-detection (CUDA/CPU).

**`utils/preprocessing.py`** — Image transforms: resize to 224×224 with padding to preserve aspect ratio, normalization with ImageNet stats.

### RAG Database

LanceDB (`lancedb/`) stores ~48 chunks for 7 plants: aloevera, banana, mango, cucumber, ginger, spinach, watermelon. Content is fetched from curated URLs (2 per plant) using LangChain's `WebBaseLoader`, chunked at 1000 chars with 200 overlap, and embedded with OpenAI ada-002. The remaining 23 classified plant species fall back to Tavily web search.

### Environment Variables

Required in `.env`:
```
OPENAI_API_KEY=...
TAVILY_API_KEY=...
```

### Python Version

Python 3.10 or 3.11 required (Docker uses 3.11-slim).
