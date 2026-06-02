def get_advice(label, confidence=None):

    label = label.lower()

    if confidence is not None and confidence < 0.5:
        return "⚠️ Low confidence. Please retake image."

    if "plastic bottle" in label:
        return "♻️ Rinse and recycle in PET bin."

    if "glass bottle" in label:
        return "🍾 Rinse and recycle as glass waste."

    if "paper" in label or "cardboard" in label:
        return "📦 Keep dry and recycle."

    if "food" in label or "organic" in label:
        return "🌱 Compost organic waste."

    return f"🔍 Detected: {label}. Sort into dry waste."


def local_guide():
    return """
🌍 Local Recycling Guide:

- Separate wet and dry waste
- Do not burn plastic
- Recycle bottles and cans properly
- Compost organic waste when possible
"""
