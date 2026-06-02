def get_advice(label):

    label = label.lower()

    if "plastic" in label or "bottle" in label:
        return "♻️ Clean before recycling. Remove caps if possible."

    elif "glass" in label:
        return "⚠️ Handle carefully. Send to glass recycling."

    elif "paper" in label:
        return "📄 Keep dry. Recycle with paper waste."

    elif "food" in label or "fruit" in label:
        return "🌱 Compost organic waste."

    else:
        return "❓ Check local recycling guidelines."


def local_guide():
    return """
♻️ Local Waste Tips (Pakistan):

- Do not mix wet and dry waste
- Plastic burning is harmful
- Separate glass and metal
- Compost organic waste if possible
"""
