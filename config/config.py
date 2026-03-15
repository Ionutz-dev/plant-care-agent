import os
from pathlib import Path
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Project paths
PROJECT_ROOT = Path(__file__).parent.parent
MODEL_DIR = PROJECT_ROOT / "models" / "checkpoints"
DATA_DIR = PROJECT_ROOT / "data"

# Model settings
MODEL_CHECKPOINT = MODEL_DIR / "best-vgg11-model-v3.ckpt"
NUM_CLASSES = 30
IMAGE_SIZE = 224

# API keys
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
TAVILY_API_KEY = os.getenv("TAVILY_API_KEY")

# Agent settings
LLM_MODEL = "gpt-4o-mini"
LLM_TEMPERATURE = 0.7

# API settings
API_HOST = "0.0.0.0"
API_PORT = 8000

# Device
DEVICE = "cuda" if os.getenv("FORCE_CPU") != "1" else "cpu"