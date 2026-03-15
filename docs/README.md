# Plant Care Card Generator

AI-powered plant classification and care card generation system using deep learning, RAG (Retrieval Augmented Generation), and LangChain agents.

---

## Overview

This project combines:
- **VGG11 Deep Learning Model** for plant classification (30 species)
- **RAG System** with vector database for curated plant care information
- **LangChain AI Agent** for intelligent information retrieval and generation
- **FastAPI Backend** for REST API
- **Streamlit Frontend** for user-friendly interface

Upload a plant image → Get classification + comprehensive care card!

---

## Features

✅ **Image Classification**: VGG11 model trained on 30 agricultural plants
✅ **RAG Database**: 7 plants with curated care guides from trusted sources
✅ **Web Search Fallback**: Tavily API for plants not in the RAG database
✅ **Structured Output**: Pydantic schemas with 18 care card fields
✅ **Dual Interface**: Web UI (Streamlit) + REST API (FastAPI)
✅ **Docker Deployment**: One-command deployment with Docker Compose

---

## Quick Start

### Using Docker (Recommended)
```bash
# 1. Configure API keys
# Create .env in project root:
# OPENAI_API_KEY=your_key_here
# TAVILY_API_KEY=your_key_here

# 2. Run
docker-compose up --build

# 3. Access
# Web UI: http://localhost:8501
# API: http://localhost:8000/docs
```

### Local Development
```bash
# 1. Install dependencies
python -m venv venv
source venv/bin/activate  # or venv\Scripts\activate on Windows
pip install -r requirements.txt

# 2. Configure
# Create .env in project root with OPENAI_API_KEY and TAVILY_API_KEY

# 3. Build vector store (first time only)
python scripts/build_vector_store.py

# 4. Run services
python main.py                              # Terminal 1
streamlit run frontend/streamlit_app.py     # Terminal 2

# 5. Access
# Web UI: http://localhost:8501
# API: http://localhost:8000/docs
```

See [Setup Guide](README_SETUP.md) for detailed instructions.

---

## Model Checkpoint

The trained VGG11 model checkpoint (`models/checkpoints/best-vgg11-model-v3.ckpt`, ~500MB) is **not included** in this repository due to file size.

To obtain it:
- Download it from [Google Drive](#) *(add your link here)*
- Or retrain the model using the notebook in `notebooks/Assignment_10.ipynb`

Place the checkpoint at: `models/checkpoints/best-vgg11-model-v3.ckpt`

---

## Project Structure
```
plant-care-agent/
│
├── api/                      # FastAPI REST API
│   ├── __init__.py
│   └── app.py               # Endpoints: /, /health, /predict
│
├── agents/                   # LangChain AI agents
│   ├── __init__.py
│   ├── plant_care_agent.py  # Main agent logic
│   └── tools.py             # RAG query + web search tools
│
├── config/                   # Configuration
│   └── config.py            # Settings, paths, API keys
│
├── frontend/                 # Streamlit web interface
│   └── streamlit_app.py     # UI for uploading images
│
├── models/                   # VGG11 classifier
│   ├── __init__.py
│   ├── classifier.py        # Model architecture
│   └── checkpoints/
│       └── best-vgg11-model-v3.ckpt  # Trained weights (not included, see above)
│
├── prompts/                  # Prompt templates
│   ├── __init__.py
│   └── plant_care_prompts.py  # Agent system prompts
│
├── schemas/                  # Pydantic models
│   ├── __init__.py
│   └── plant_care_card.py   # PlantCareCard with 18 fields
│
├── scripts/                  # Utility scripts
│   ├── build_vector_store.py  # Build RAG database
│   └── test_rag.py           # Test RAG system
│
├── utils/                    # Helper functions
│   ├── __init__.py
│   └── preprocessing.py     # Image transforms
│
├── lancedb/                  # Vector database
│   └── plant_care_guides.lance
│
├── docs/                     # Documentation
│   ├── README_SETUP.md      # Setup guide
│   └── README_DOCKER.md     # Docker guide
│
├── notebooks/                # Training notebooks
│   └── Assignment_10.ipynb
│
├── .env                     # API keys (not committed)
├── .gitignore               # Git ignore rules
├── .dockerignore            # Docker ignore rules
├── requirements.txt         # Python dependencies
├── Dockerfile               # Docker image definition
├── docker-compose.yml       # Multi-service orchestration
└── main.py                  # FastAPI entry point
```

---

## Technology Stack

### Machine Learning
- **PyTorch** - Deep learning framework
- **PyTorch Lightning** - Training framework
- **TorchVision** - Pre-trained models and transforms
- **VGG11** - CNN architecture for classification

### LLM & RAG
- **OpenAI GPT-4o-mini** - Language model
- **LangChain** - Agent framework
- **LanceDB** - Vector database
- **OpenAI Embeddings** - Text embeddings (ada-002)

### Backend
- **FastAPI** - REST API framework
- **Uvicorn** - ASGI server
- **Pydantic** - Data validation

### Frontend
- **Streamlit** - Web interface

### Tools
- **Docker** - Containerization
- **Docker Compose** - Multi-container orchestration
- **Tavily** - Web search API

---

## How It Works

### 1. Image Classification
```
User uploads image
    ↓
Preprocessing (resize to 224×224, normalize with ImageNet stats)
    ↓
VGG11 Model (frozen feature extractor + custom classifier head)
    ↓
Plant class prediction (e.g., "cucumber") + confidence score
```

### 2. RAG Information Retrieval
```
Plant name
    ↓
Agent queries vector store with metadata filter on plant_name
    ↓
Retrieve top 4 relevant chunks (fallback: unfiltered search)
    ↓
If no results: Tavily web search fallback
```

### 3. Care Card Generation
```
Plant name + retrieved information
    ↓
LangChain Agent (GPT-4o-mini)
    ↓
Structured output prompt → Pydantic validation
    ↓
PlantCareCard with 18 fields
```

### Complete Pipeline
```
Image → VGG11 → Plant Name → Agent → RAG/Web Search → LLM → Care Card → UI
```

---

## Dataset

**Source**: [Kaggle - Plants Type Dataset](https://www.kaggle.com/datasets/yudhaislamisulistya/plants-type-datasets)

**30 Agricultural Plants**:
aloevera, banana, bilimbi, cantaloupe, cassava, coconut, corn, cucumber, curcuma, eggplant, galangal, ginger, guava, kale, longbeans, mango, melon, orange, paddy, papaya, peper chili, pineapple, pomelo, shallot, soybeans, spinach, sweet potatoes, tobacco, waterapple, watermelon

**RAG Database (7 plants)**:
- aloevera, banana, mango, cucumber, ginger, spinach, watermelon
- 2 curated URLs per plant from: almanac.com, gardeningknowhow.com, epicgardening.com
- ~48 document chunks total

**Remaining 23 plants** use Tavily web search fallback.

---

## API Endpoints

### GET /
Returns API information and status.

### GET /health
Health check endpoint — returns model load status and device info.

### POST /predict
Upload a plant image, returns classification + care card.

**Request:**
```bash
curl -X POST "http://localhost:8000/predict" \
  -H "Content-Type: multipart/form-data" \
  -F "file=@cucumber.jpg"
```

**Response:**
```json
{
  "predicted_plant": "cucumber",
  "confidence": "95.3%",
  "care_card": {
    "latin_name": "Cucumis sativus",
    "common_names": ["Cucumber", "Garden cucumber"],
    "plant_family": "Cucurbitaceae",
    "lighting_conditions": "Full sun, 6-8 hours daily",
    "watering_schedule": "Water deeply 1-2 times per week",
    ...
  }
}
```

Interactive docs: http://localhost:8000/docs

---

## Configuration

### Environment Variables (.env)
```env
# Required
OPENAI_API_KEY=sk-...
TAVILY_API_KEY=tvly-...

# Optional
FORCE_CPU=1    # Force CPU inference even if CUDA is available
```

### Hardcoded Settings (config/config.py)
```python
NUM_CLASSES = 30
IMAGE_SIZE = 224
LLM_MODEL = "gpt-4o-mini"
LLM_TEMPERATURE = 0.7
API_HOST = "0.0.0.0"
API_PORT = 8000
MODEL_CHECKPOINT = "models/checkpoints/best-vgg11-model-v3.ckpt"
```

---

## PlantCareCard Schema

18 fields of comprehensive plant information:

1. **latin_name** - Scientific name
2. **common_names** - List of common names
3. **plant_family** - Botanical family
4. **native_region** - Origin
5. **outdoors** - Can grow outdoors?
6. **indoor_suitable** - Can grow indoors?
7. **lighting_conditions** - Light requirements
8. **temperature_range** - Ideal temperature
9. **humidity_requirements** - Humidity needs
10. **watering_schedule** - How often to water
11. **soil_type** - Soil requirements
12. **fertilization** - Fertilizing schedule
13. **pruning_needs** - Pruning requirements
14. **growth_rate** - How fast it grows
15. **mature_size** - Full-grown size
16. **toxicity** - Pet/human safety
17. **common_pests** - Pest issues
18. **special_care_notes** - Additional tips

---

## Testing

### Test RAG System
```bash
python scripts/test_rag.py
```

### Test API
```bash
# Health check
curl http://localhost:8000/health

# Predict
curl -X POST "http://localhost:8000/predict" \
  -F "file=@test_image.jpg"
```

### Test with Docker
```bash
docker-compose up --build
# Open http://localhost:8501
# Upload a plant image
```

---

## Development

### Adding New Plants to RAG

1. Edit `scripts/build_vector_store.py`
2. Add URLs to `CARE_GUIDE_URLS` dictionary:
```python
CARE_GUIDE_URLS = {
    "newplant": [
        "https://example.com/newplant-care-1",
        "https://example.com/newplant-care-2"
    ],
    ...
}
```
3. Rebuild vector store:
```bash
python scripts/build_vector_store.py
```

### Modifying Prompts

Edit `prompts/plant_care_prompts.py` to change the system prompt, user input template, or structured output prompt used for care card generation.

### Hot Reload

**FastAPI:**
```bash
uvicorn api.app:app --reload
```

**Streamlit:**
- Auto-reloads on file changes

---

## Docker

See [Docker Guide](README_DOCKER.md) for full details.

```bash
docker-compose up --build   # First time
docker-compose up           # Subsequent runs
docker-compose down         # Stop
docker-compose logs -f      # View logs
docker-compose down -v && docker system prune -a  # Clean everything
```

---

## Performance

- **Classification Time**: ~200ms
- **RAG Query**: ~5s
- **LLM Generation**: ~5-10s
- **Total Response Time**: ~10-15s (with RAG) vs ~20s (web search only)

---

## Future Improvements

- [ ] Add more plants to RAG database (23 remaining)
- [ ] Implement user feedback system
- [ ] Add image upload history
- [ ] Multi-language support
- [ ] Mobile app
- [ ] Plant disease detection

---

## Troubleshooting

**"Module not found"**
- Activate virtual environment: `source venv/bin/activate`

**"API key not found"**
- Create `.env` file with `OPENAI_API_KEY` and `TAVILY_API_KEY`

**"Port already in use"**
- Change ports in `docker-compose.yml` or stop other services

**"Model checkpoint not found"**
- Download checkpoint and place at `models/checkpoints/best-vgg11-model-v3.ckpt`

**Docker build fails**
- Make sure Docker Desktop is running
- Clear cache: `docker system prune -a`
- Rebuild: `docker-compose up --build`

---

## Documentation

- [Setup Guide](README_SETUP.md) - Installation and configuration
- [Docker Guide](README_DOCKER.md) - Docker usage and deployment
