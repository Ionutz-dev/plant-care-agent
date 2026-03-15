import torch
from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.responses import JSONResponse
from PIL import Image
import io
import uvicorn

from config import config
from models import VGG11Classifier
from utils import preprocess_image
from agents import generate_care_card

# Plant class names (30 agricultural plants from the dataset)
PLANT_CLASSES = [
    'aloevera', 'banana', 'bilimbi', 'cantaloupe', 'cassava',
    'coconut', 'corn', 'cucumber', 'curcuma', 'eggplant',
    'galangal', 'ginger', 'guava', 'kale', 'longbeans',
    'mango', 'melon', 'orange', 'paddy', 'papaya',
    'peper chili', 'pineapple', 'pomelo', 'shallot', 'soybeans',
    'spinach', 'sweet potatoes', 'tobacco', 'waterapple', 'watermelon'
]

# Initialize FastAPI app
app = FastAPI(
    title="Plant Care Card Generator",
    description="Upload a plant image to get classification and care instructions",
    version="1.0.0"
)

# Load model at startup
model = None
device = None


@app.on_event("startup")
async def load_model():
    """Load the VGG11 model on startup."""
    global model, device

    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    print(f"Using device: {device}")

    try:
        model = VGG11Classifier.load_from_checkpoint(
            str(config.MODEL_CHECKPOINT),
            num_classes=config.NUM_CLASSES
        )
        model.to(device)
        model.eval()
        print("Model loaded successfully!")
    except Exception as e:
        print(f"Error loading model: {e}")
        raise


@app.get("/")
async def root():
    """API information endpoint."""
    return {
        "message": "Plant Care Card Generator API",
        "endpoints": {
            "/predict": "POST - Upload plant image for classification and care card",
            "/health": "GET - Check API health"
        }
    }


@app.get("/health")
async def health_check():
    """Health check endpoint."""
    return {
        "status": "healthy",
        "model_loaded": model is not None,
        "device": str(device)
    }


@app.post("/predict")
async def predict_and_generate_care_card(file: UploadFile = File(...)):
    """
    Upload a plant image to get classification and care card.

    Returns:
        JSON with predicted plant class and detailed care card
    """
    if model is None:
        raise HTTPException(status_code=503, detail="Model not loaded")

    # Validate file type
    if not file.content_type.startswith('image/'):
        raise HTTPException(status_code=400, detail="File must be an image")

    try:
        # Read and preprocess image
        print(f"Processing image: {file.filename}")
        image_data = await file.read()
        image = Image.open(io.BytesIO(image_data)).convert('RGB')

        # Preprocess
        image_tensor = preprocess_image(image, config.IMAGE_SIZE).to(device)

        # Predict
        with torch.no_grad():
            outputs = model(image_tensor)
            probabilities = torch.nn.functional.softmax(outputs, dim=1)
            confidence, predicted_idx = torch.max(probabilities, 1)

        # Get plant name
        plant_name = PLANT_CLASSES[predicted_idx.item()]
        confidence_score = confidence.item()

        print(f"Predicted: {plant_name} (confidence: {confidence_score:.2%})")

        # Generate care card
        print("Generating care card...")
        care_card = generate_care_card(plant_name)
        print("Care card generated!")

        return JSONResponse(content={
            "predicted_plant": plant_name,
            "confidence": f"{confidence_score:.2%}",
            "care_card": care_card
        })

    except Exception as e:
        print(f"Error: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Processing error: {str(e)}")


if __name__ == "__main__":

    uvicorn.run(app, host=config.API_HOST, port=config.API_PORT)