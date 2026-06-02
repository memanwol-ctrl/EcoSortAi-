from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.pagesizes import A4
from datetime import datetime


def generate_pdf_report(data, filename="eco_report.pdf"):

    doc = SimpleDocTemplate(filename, pagesize=A4)
    styles = getSampleStyleSheet()
    content = []

    content.append(Paragraph("🌍 EcoSort AI - Eco Impact Report", styles["Title"]))
    content.append(Spacer(1, 12))

    content.append(Paragraph(f"Date: {datetime.now()}", styles["Normal"]))
    content.append(Spacer(1, 12))

    content.append(Paragraph(f"Total Scans: {data['scans']}", styles["Normal"]))
    content.append(Spacer(1, 8))

    content.append(Paragraph(f"Total CO₂ Impact: {data['co2']} kg", styles["Normal"]))
    content.append(Spacer(1, 8))

    content.append(Paragraph(f"Eco Score: {data['eco_score']}/100", styles["Normal"]))
    content.append(Spacer(1, 12))

    content.append(Paragraph("Waste Breakdown:", styles["Heading2"]))
    content.append(Paragraph(str(data["breakdown"]), styles["Normal"]))
    content.append(Spacer(1, 12))

    content.append(Paragraph("Suggestions:", styles["Heading2"]))
    content.append(Paragraph(data["suggestions"], styles["Normal"]))

    doc.build(content)

    return filename
