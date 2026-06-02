import torch
from PIL import Image
from transformers import CLIPProcessor, CLIPModel

# Load model once
model = CLIPModel.from_pretrained("openai/clip-vit-base-patch32")
processor = CLIPProcessor.from_pretrained("openai/clip-vit-base-patch32")

# Waste categories (this is the KEY)
WASTE_LABELS = [
    "plastic bottle",
    "plastic cup",
    "metal can",
    "glass bottle",
    "paper",
    "cardboard box",
    "food waste",
    "organic waste",
    "trash"
]

def predict_waste_clip(image: Image.Image):

    inputs = processor(
        text=WASTE_LABELS,
        images=image,
        return_tensors="pt",
        padding=True
    )

    with torch.no_grad():
        outputs = model(**inputs)
        logits_per_image = outputs.logits_per_image
        probs = logits_per_image.softmax(dim=1)[0]

    # Get top prediction
    top_idx = torch.argmax(probs).item()

    top1 = {
        "label": WASTE_LABELS[top_idx],
        "score": probs[top_idx].item()
    }

    # Top 3
    top3 = []
    for i in torch.topk(probs, 3).indices:
        top3.append({
            "label": WASTE_LABELS[i],
            "score": probs[i].item()
        })

    return top1, top3
