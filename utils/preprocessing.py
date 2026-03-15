import torch
from torchvision import transforms
from PIL import Image
import io


class PadToSquare:
    """Pad image to square shape."""

    def __call__(self, img):
        width, height = img.size
        max_dim = max(width, height)

        left = (max_dim - width) // 2
        top = (max_dim - height) // 2
        right = max_dim - width - left
        bottom = max_dim - height - top

        padding = (left, top, right, bottom)
        return transforms.functional.pad(img, padding, fill=0, padding_mode='constant')


def get_inference_transform(image_size=224):
    """Get preprocessing transforms for inference."""
    return transforms.Compose([
        PadToSquare(),
        transforms.Resize((image_size, image_size)),
        transforms.ToTensor(),
        transforms.Normalize(
            mean=[0.485, 0.456, 0.406],
            std=[0.229, 0.224, 0.225]
        )
    ])


def preprocess_image(image_data, image_size=224):
    """
    Preprocess image for model inference.

    Args:
        image_data: PIL Image or bytes
        image_size: Target image size

    Returns:
        torch.Tensor: Preprocessed image tensor
    """
    if isinstance(image_data, bytes):
        image = Image.open(io.BytesIO(image_data)).convert('RGB')
    else:
        image = image_data.convert('RGB')

    transform = get_inference_transform(image_size)
    image_tensor = transform(image)

    return image_tensor.unsqueeze(0)  # Add batch dimension