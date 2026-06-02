# Simple estimated carbon footprint per item (kg CO2 approx)

CARBON_DATA = {
    "plastic": 0.08,
    "bottle": 0.08,
    "glass": 0.30,
    "paper": 0.05,
    "cardboard": 0.04,
    "food": 0.02,
    "fruit": 0.02,
    "organic": 0.02
}

def get_carbon_impact(label: str):
    label = label.lower()

    for key, value in CARBON_DATA.items():
        if key in label:
            return value

    return 0.10  # default fallback
