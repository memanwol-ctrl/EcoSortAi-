def get_advice(label, confidence=None):

    label = label.lower()

    # ---------------- HIGH CONFIDENCE CHECK ----------------
    if confidence is not None and confidence < 0.5:
        return (
            "⚠️ Uncertain detection. Please re-scan with better lighting and a clearer background."
        )

    # ---------------- PLASTIC ----------------
    if any(x in label for x in ["plastic bottle", "pet bottle", "water bottle"]):
        return (
            "♻️ Rinse thoroughly, remove cap, and recycle in PET (1) bin. "
            "Do not mix with food waste. Flatten only if required locally."
        )

    if "plastic cup" in label:
        return (
            "⚠️ Most plastic cups are not recyclable unless labeled PP5. "
            "Check bottom recycling symbol before disposal."
        )

    if "plastic" in label:
        return (
            "♻️ Plastic detected. Identify resin code (1–7). "
            "PET and HDPE are recyclable, others often require special handling."
        )

    # ---------------- GLASS ----------------
    if any(x in label for x in ["glass bottle", "glass jar"]):
        return (
            "🍾 Rinse, remove lids, and recycle in glass bin. "
            "Separate by color if possible (clear, green, brown)."
        )

    if "glass" in label:
        return (
            "⚠️ Glass waste. Handle carefully and avoid mixing with ceramics or mirrors."
        )

    # ---------------- PAPER ----------------
    if "cardboard" in label:
        return (
            "📦 Flatten cardboard boxes. Keep dry and clean. "
            "Remove plastic tape before recycling."
        )

    if "paper" in label:
        return (
            "📄 Recycle clean paper only. Avoid wet, oily, or laminated paper."
        )

    # ---------------- ORGANIC ----------------
    if any(x in label for x in ["food", "fruit", "organic"]):
        return (
            "🌱 Compost this waste. If dumped, it produces methane gas in landfills."
        )

    # ---------------- METAL ----------------
    if any(x in label for x in ["can", "aluminum", "metal"]):
        return (
            "🥫 Rinse and crush lightly. Metal is highly recyclable and energy-efficient."
        )

    # ---------------- UNKNOWN / FALLBACK ----------------
    return (
        f"🔍 Detected: {label}. "
        "Separate into dry waste category. Avoid mixing with wet/organic waste. "
        "If unsure, follow local municipal recycling rules."
    )
