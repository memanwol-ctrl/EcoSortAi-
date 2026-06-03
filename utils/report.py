from reportlab.platypus import (
SimpleDocTemplate,
Paragraph,
Spacer,
Table,
TableStyle,
Image
)

from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.pagesizes import A4

from datetime import datetime

import matplotlib.pyplot as plt
import pandas as pd

def generate_pdf_report(data, filename="eco_report.pdf"):

```
styles = getSampleStyleSheet()

# ----------------------------
# Create Pie Chart
# ----------------------------

breakdown = data["breakdown"]

pie_file = "waste_pie_chart.png"

plt.figure(figsize=(5, 5))
plt.pie(
    breakdown.values(),
    labels=breakdown.keys(),
    autopct="%1.1f%%"
)
plt.title("Waste Distribution")
plt.savefig(pie_file, bbox_inches="tight")
plt.close()

# ----------------------------
# Create CO2 Trend Graph
# ----------------------------

trend_file = "co2_trend.png"

history = pd.DataFrame(data["history"])

if not history.empty:

    plt.figure(figsize=(6, 4))

    history["co2"].cumsum().plot(
        marker="o"
    )

    plt.title("Cumulative CO₂ Impact")
    plt.xlabel("Scan Number")
    plt.ylabel("CO₂ (kg)")

    plt.savefig(
        trend_file,
        bbox_inches="tight"
    )

    plt.close()

# ----------------------------
# Build PDF
# ----------------------------

doc = SimpleDocTemplate(
    filename,
    pagesize=A4
)

elements = []

# Title

elements.append(
    Paragraph(
        "EcoSort AI - Environmental Impact Report",
        styles["Title"]
    )
)

elements.append(Spacer(1, 12))

elements.append(
    Paragraph(
        f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M')}",
        styles["Normal"]
    )
)

elements.append(Spacer(1, 20))

# ----------------------------
# Summary Table
# ----------------------------

summary_data = [
    ["Metric", "Value"],
    ["Total Scans", str(data["scans"])],
    ["Total CO₂ Impact", f"{data['co2']} kg"],
    ["Eco Score", f"{data['eco_score']}/100"],
    ["Most Common Waste", data["most_common"]]
]

summary_table = Table(summary_data)

summary_table.setStyle(
    TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), colors.lightgreen),
        ("GRID", (0, 0), (-1, -1), 1, colors.black)
    ])
)

elements.append(
    Paragraph(
        "Summary",
        styles["Heading2"]
    )
)

elements.append(summary_table)

elements.append(Spacer(1, 20))

# ----------------------------
# Waste Breakdown Table
# ----------------------------

waste_table_data = [
    ["Waste Type", "Count"]
]

for waste, count in breakdown.items():
    waste_table_data.append(
        [waste.capitalize(), str(count)]
    )

waste_table = Table(waste_table_data)

waste_table.setStyle(
    TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), colors.lightblue),
        ("GRID", (0, 0), (-1, -1), 1, colors.black)
    ])
)

elements.append(
    Paragraph(
        "Waste Breakdown",
        styles["Heading2"]
    )
)

elements.append(waste_table)

elements.append(Spacer(1, 20))

# ----------------------------
# Pie Chart
# ----------------------------

elements.append(
    Paragraph(
        "Waste Distribution",
        styles["Heading2"]
    )
)

elements.append(
    Image(
        pie_file,
        width=300,
        height=300
    )
)

elements.append(Spacer(1, 20))

# ----------------------------
# CO2 Trend
# ----------------------------

if not history.empty:

    elements.append(
        Paragraph(
            "CO₂ Impact Trend",
            styles["Heading2"]
        )
    )

    elements.append(
        Image(
            trend_file,
            width=400,
            height=250
        )
    )

    elements.append(Spacer(1, 20))

# ----------------------------
# Recommendations
# ----------------------------

recommendations = f"""
Most of your waste is {data['most_common']}.

Recommendations:

• Reduce single-use plastics where possible.
• Separate recyclable materials before disposal.
• Compost organic waste.
• Reuse containers and packaging.
• Increase recycling participation.
"""

elements.append(
    Paragraph(
        "Recommendations",
        styles["Heading2"]
    )
)

elements.append(
    Paragraph(
        recommendations,
        styles["BodyText"]
    )
)

doc.build(elements)

return filename
```
