# Docker Guide

Guide to using Docker with this project.

---

## What is Docker?

Docker packages the entire application into **containers** — everything needed to run:
- Python 3.11 + all packages
- Your code
- Vector database (lancedb/)

The model checkpoint is **not** baked into the image; it is mounted as a volume from `./models/checkpoints` on the host.

**Benefits:**
- Works the same on any computer
- No complex local setup
- One command to run

---

## Prerequisites

Before running any Docker commands, make sure:
- **Docker Desktop is installed and running** (look for the whale icon in your taskbar)
- Your `.env` file is configured with `OPENAI_API_KEY` and `TAVILY_API_KEY`
- The model checkpoint is placed at `models/checkpoints/best-vgg11-model-v3.ckpt`

---

## Basic Commands

### Start Application (first time)
```bash
docker-compose up --build
```

### Start (after first time)
```bash
docker-compose up
```

### Stop
```bash
Ctrl+C
docker-compose down
```

### View Logs
```bash
docker-compose logs -f

# Logs for a specific service
docker-compose logs api
docker-compose logs streamlit
```

### Clean Everything
```bash
docker-compose down -v
docker system prune -a
```

---

## How It Works

### Two Services Run:

**1. API service (port 8000)** — `plant-care-api`
- Loads the VGG11 model at startup
- Classifies plant images
- Generates care cards via LangChain agent
- Has a health check: `curl http://localhost:8000/health` every 30s
- Access: http://localhost:8000/docs

**2. Streamlit service (port 8501)** — `plant-care-streamlit`
- Web interface for uploading images and viewing results
- Starts after the API service
- Connects to API at `http://api:8000` over the internal Docker network
- Access: http://localhost:8501

### They Talk to Each Other:
```
Streamlit → API (internal network: http://api:8000) → Returns care card → Streamlit displays it
```

---

## Files Explained

### Dockerfile
Single image used by both services:
- Base: `python:3.11-slim`
- Installs system deps (`build-essential`, `curl`) and all Python packages
- Copies all project code and the lancedb vector store
- Copies `.env` directly into the image
- `models/checkpoints/` is created but left empty (filled by volume mount)
- Exposes ports 8000 and 8501
- Default command: `python main.py` (overridden per-service in docker-compose.yml)

### docker-compose.yml
- **api** service: runs `python main.py`, mounts `./models/checkpoints` as a volume, has health check
- **streamlit** service: runs `streamlit run frontend/streamlit_app.py --server.address=0.0.0.0`, depends on api
- Both services share `plant-care-network` (bridge) for internal communication

### .dockerignore
Excludes `venv/`, `__pycache__/`, and `.git/` from the Docker build context.

---

## Common Docker Commands
```bash
# See running containers
docker ps

# See all images
docker images

# Remove unused images
docker image prune

# View resource usage
docker stats

# Access container shell
docker exec -it plant-care-api bash
```

---

## Troubleshooting

### Docker Desktop Not Running
```
Error: "The system cannot find the file specified"
Fix: Open Docker Desktop and wait for it to fully load, then retry
```

### Port Already in Use
```bash
# Stop all containers
docker-compose down

# Or change the host ports in docker-compose.yml (left side of the mapping)
# e.g., "8001:8000" to use port 8001 on the host
```

### Out of Disk Space
```bash
docker system prune -a
```

### Build Fails
```bash
# Clear cache and rebuild
docker-compose down -v
docker system prune -a
docker-compose up --build
```

### Can't Connect to API
```bash
# Check if both containers are running
docker ps

# Check API logs
docker-compose logs api
```

---

## Docker vs Local

| Aspect | Docker | Local |
|--------|--------|-------|
| Setup Time | ~5 min | ~30 min |
| Works Everywhere | Yes | Depends on OS |
| Easy Deployment | Yes | No |
| Debugging | Harder | Easier |
| Hot Reload | Requires rebuild | Built-in |

---

## Workflow

### First Time
```bash
docker-compose up --build    # 5-10 minutes
```

### After Code Changes
```bash
docker-compose up --build    # 2-3 minutes
```

### Normal Run
```bash
docker-compose up            # ~30 seconds
```

---

## What Gets Packaged

Your Docker image includes:
- ✅ Python 3.11
- ✅ All packages from requirements.txt
- ✅ All project code
- ✅ LanceDB vector store (~10MB)
- ✅ Environment variables from .env (copied into image)
- ⚠️ Model checkpoint (~500MB) — mounted as a volume, not baked in

**Total image size:** ~2.5GB

---

## Summary

**To use Docker:**
1. Start Docker Desktop
2. Place model checkpoint at `models/checkpoints/best-vgg11-model-v3.ckpt`
3. Create `.env` with your API keys
4. Run `docker-compose up --build`
5. Access http://localhost:8501

**To stop:**
- Press `Ctrl+C`
- Run `docker-compose down`
