def get_advice(label, confidence=None):

    label = label.lower()

    # LOW CONFIDENCE SAFETY CHECK
    if confidence is not None and confidence < 0.5:
        return "⚠️ Low confidence detection. Please retake a clearer image."

    # ---------------- PLASTIC ----------------
    if "plastic bottle" in label:
        return "♻️ Rinse bottle, remove cap, recycle in PET bin."

    if "plastic cup" in label:
        return "⚠️ Plastic cups often NOT recyclable (check PP5 symbol)."

    if "plastic" in label:
        return "♻️ Identify resin code (1–7). PET & HDPE are recyclable."

    # ---------------- GLASS ----------------
    if "glass bottle" in label or "glass jar" in label:
        return "🍾 Rinse and recycle in glass bin. Separate by color if possible."

    if "glass" in label:
        return "⚠️ Handle carefully. Do not mix with ceramics."

    # ---------------- PAPER ----------------
    if "paper" in label or "cardboard" in label:
        return "📦 Keep dry. Remove tape/plastic before recycling."

    # ---------------- ORGANIC ----------------
    if "food" in label or "fruit" in label:
        return "🌱 Compost organic waste. Avoid landfill disposal."

    # ---------------- METAL ----------------
    if "can" in label or "metal" in label:
        return "🥫 Rinse and recycle. Metal is highly reusable."

    # ---------------- DEFAULT ----------------
    return f"🔍 Detected: {label}. Sort into dry waste if unsure."
