# Setup Guide

Quick guide to get the Plant Care Card Generator running.

---

## Option 1: Docker (Recommended)

### Requirements
- Docker Desktop installed and running
- OpenAI API key
- Tavily API key

### Steps

1. **Install Docker Desktop**
   - Download: https://www.docker.com/products/docker-desktop/
   - Start Docker Desktop and wait for it to fully load before proceeding

2. **Configure API Keys**

   Create `.env` file in project root:
   ```env
   OPENAI_API_KEY=your_openai_key_here
   TAVILY_API_KEY=your_tavily_key_here
   ```

3. **Add Model Checkpoint**

   Download `best-vgg11-model-v3.ckpt` and place it at:
   ```
   models/checkpoints/best-vgg11-model-v3.ckpt
   ```
   See [Model Checkpoint](README.md#model-checkpoint) in the main README for download instructions.

4. **Run**
   ```bash
   docker-compose up --build
   ```

5. **Access**
   - Web UI: http://localhost:8501
   - API: http://localhost:8000/docs

6. **Stop**
   ```bash
   Ctrl+C
   docker-compose down
   ```

---

## Option 2: Local Development

### Requirements
- Python 3.10 or 3.11
- pip

### Steps

1. **Create Virtual Environment**
   ```bash
   python -m venv venv

   # Activate:
   venv\Scripts\activate          # Windows
   source venv/bin/activate       # Mac/Linux
   ```

2. **Install Dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Configure API Keys**

   Create `.env` file in project root:
   ```env
   OPENAI_API_KEY=your_key_here
   TAVILY_API_KEY=your_key_here
   ```

4. **Add Model Checkpoint**

   Download `best-vgg11-model-v3.ckpt` and place it at:
   ```
   models/checkpoints/best-vgg11-model-v3.ckpt
   ```

5. **Build Vector Store** (first time only)
   ```bash
   python scripts/build_vector_store.py
   ```
   Takes 2-3 minutes. Fetches content from curated URLs and builds the LanceDB vector store.

6. **Run Services**

   Terminal 1 - API:
   ```bash
   python main.py
   ```

   Terminal 2 - Frontend:
   ```bash
   streamlit run frontend/streamlit_app.py
   ```

7. **Access**
   - Web UI: http://localhost:8501
   - API: http://localhost:8000/docs

---

## Getting API Keys

### OpenAI
1. Go to https://platform.openai.com/api-keys
2. Create account / Sign in
3. Click "Create new secret key"
4. Copy and paste into `.env`

Cost: ~$0.003-0.005 per request (uses gpt-4o-mini + ada-002 embeddings)

### Tavily
1. Go to https://tavily.com/
2. Sign up
3. Get API key from dashboard
4. Add to `.env`

Required for web search fallback. Without it, only the 7 plants in the RAG database will return full care cards; the remaining 23 classified plants will have no information source to draw from.

---

## Supported Plants

**Plants with RAG database** (curated info, ~10-15s response):
- aloevera, banana, mango, cucumber, ginger, spinach, watermelon

**Remaining 23 plants use Tavily web search fallback** (~20s response):
- bilimbi, cantaloupe, cassava, coconut, corn, curcuma, eggplant, galangal, guava, kale, longbeans, melon, orange, paddy, papaya, peper chili, pineapple, pomelo, shallot, soybeans, sweet potatoes, tobacco, waterapple, watermelon

---

## Common Issues

**"Module not found"**
- Make sure virtual environment is activated
- Check you see `(venv)` in terminal prompt

**"OPENAI_API_KEY not found"**
- Create `.env` file with your API key in the project root

**"Model checkpoint not found"**
- Download the checkpoint and place it at `models/checkpoints/best-vgg11-model-v3.ckpt`

**"Port already in use"**
- Another service is using port 8000 or 8501
- Stop other services or change ports in `docker-compose.yml`

**Docker won't start**
- Make sure Docker Desktop is running before running `docker-compose`
- Check logs: `docker-compose logs`

---

## Testing

Test the RAG system:
```bash
python scripts/test_rag.py
```

Test the API:
```bash
curl http://localhost:8000/health
```

---

## Next Steps

- Upload plant images at http://localhost:8501
- Explore API docs at http://localhost:8000/docs
- Read [Docker Guide](README_DOCKER.md) for deployment details
