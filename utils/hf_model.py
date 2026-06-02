from transformers import pipeline
from utils.cache import load_model

classifier = load_model()

def predict_image(image):
    results = classifier(image)

    top1 = results[0]
    top3 = results[:3]

    return top1, top3
