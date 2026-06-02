from transformers import pipeline

classifier = pipeline(
    "image-classification",
    model="google/vit-base-patch16-224"
)

def predict_image(image):
    results = classifier(image)
    top = results[0]

    return top["label"], float(top["score"])
