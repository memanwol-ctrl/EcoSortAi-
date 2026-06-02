def map_waste(label: str):
    label = label.lower()

    if any(x in label for x in ["bottle", "plastic", "bag", "container"]):
        return "Plastic Waste ♻️"

    elif "glass" in label:
        return "Glass Waste ♻️"

    elif any(x in label for x in ["paper", "book", "cardboard"]):
        return "Paper Waste ♻️"

    elif any(x in label for x in ["food", "banana", "fruit", "vegetable"]):
        return "Organic Waste 🌱"

    else:
        return "General Waste ❓"


def get_advice(category):
    if category == "Plastic Waste ♻️":
        return "Clean it, remove liquid, and put in plastic recycling bin."
    elif category == "Glass Waste ♻️":
        return "Do not break it. Send to glass recycling center."
    elif category == "Paper Waste ♻️":
        return "Keep dry and recycle with paper waste."
    elif category == "Organic Waste 🌱":
        return "Compost it if possible."
    else:
        return "Check local waste management guidelines."
