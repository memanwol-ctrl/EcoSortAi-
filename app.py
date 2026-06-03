import streamlit as st
from PIL import Image
import pandas as pd
import matplotlib.pyplot as plt

from utils.clip_model import predict_waste_clip
from utils.recycling import get_advice, local_guide
from utils.climate import get_carbon_impact
from utils.report import generate_pdf_report

# ---------------- PAGE SETUP ----------------
st.set_page_config(page_title="EcoSort AI Dashboard", layout="wide")

st.title("🌍 EcoSort AI — Eco Analytics Dashboard")
st.write("Track waste, CO₂ impact, and environmental behavior over time.")

st.divider()

# ---------------- SESSION STATE ----------------
if "scan_count" not in st.session_state:
    st.session_state.scan_count = 0

if "total_co2" not in st.session_state:
    st.session_state.total_co2 = 0

if "history" not in st.session_state:
    st.session_state.history = []

if "waste_breakdown" not in st.session_state:
    st.session_state.waste_breakdown = {
        "plastic": 0,
        "glass": 0,
        "metal": 0,
        "paper": 0,
        "organic": 0
    }

# ---------------- SIDEBAR ----------------
with st.sidebar:
    st.header("🌍 Eco Mission")

    st.metric("Total Scans", st.session_state.scan_count)
    st.metric("Total CO₂ (kg)", round(st.session_state.total_co2, 2))

    st.progress(min(st.session_state.scan_count / 20, 1.0))

    st.write("🎯 Goal: 20 scans unlocks Eco Report")

# ---------------- INPUT ----------------
st.subheader("♻️ Add Waste")

entry_mode = st.radio(
    "Choose Method",
    [
        "📸 Scan Waste",
        "✍️ Manual Entry"
    ]
)
if entry_mode == "✍️ Manual Entry":

    waste_type = st.selectbox(
        "Waste Type",
        [
            "Plastic",
            "Metal",
            "Glass",
            "Paper",
            "Organic"
        ]
    )

    quantity = st.number_input(
        "Quantity",
        min_value=1,
        value=1
    )

    if st.button("Add Waste Entry"):

        category = waste_type.lower()

        carbon_values = {
            "plastic": 6,
            "metal": 4,
            "glass": 2,
            "paper": 1,
            "organic": 0.5
        }

        carbon = carbon_values[category] * quantity

        st.session_state.scan_count += quantity
        st.session_state.total_co2 += carbon
        st.session_state.waste_breakdown[category] += quantity

        for _ in range(quantity):
            st.session_state.history.append({
                "label": waste_type,
                "category": category,
                "co2": carbon_values[category]
            })

        st.success(f"✅ Added {quantity} {waste_type} item(s)")
    elif entry_mode == "📸 Scan Waste":

      scan_method = st.radio(
        "Scan Method",
        [
            "📁 Upload Image",
            "📷 Camera"
        ]
    )

   elif entry_mode == "📸 Scan Waste":

    scan_method = st.radio(
        "Scan Method",
        ["📁 Upload Image", "📷 Camera"]
    )

    image = None

    if scan_method == "📁 Upload Image":

        uploaded_file = st.file_uploader(
            "Upload image",
            type=["jpg", "png", "jpeg"]
        )

        if uploaded_file:
            image = Image.open(uploaded_file)

    elif scan_method == "📷 Camera":

        camera_file = st.camera_input("Take picture")

        if camera_file:
            image = Image.open(camera_file)

st.divider()

# ---------------- MAIN PROCESSING ----------------
if image:

    st.image(image, use_container_width=True)

    st.subheader("🤖 AI Analysis")

    top1, top3 = predict_waste_clip(image)

    label = top1["label"]
    confidence = top1["score"]

    # ---------------- CATEGORY ----------------
    if "plastic" in label:
        category = "plastic"
        impact_score = 8
    elif "metal" in label:
        category = "metal"
        impact_score = 5
    elif "glass" in label:
        category = "glass"
        impact_score = 4
    elif "paper" in label:
        category = "paper"
        impact_score = 2
    else:
        category = "organic"
        impact_score = 6

    carbon = get_carbon_impact(label)

    # ---------------- UPDATE STATE ----------------
    st.session_state.scan_count += 1
    st.session_state.total_co2 += carbon
    st.session_state.waste_breakdown[category] += 1

    st.session_state.history.append({
        "label": label,
        "category": category,
        "co2": carbon
    })

    # ---------------- RESULT ----------------
    st.success(f"Detected: {label}")
    st.metric("Confidence", f"{confidence:.2f}")

    st.divider()

    # ---------------- IMPACT ----------------
    st.subheader("🌍 Impact Score")
    st.progress(impact_score / 10)

    if impact_score <= 3:
        st.success("Low impact 🌱")
    elif impact_score <= 6:
        st.warning("Medium impact ⚠️")
    else:
        st.error("High impact 🔥")

    st.divider()

    # ---------------- RECYCLING ----------------
    st.subheader("♻️ Recycling Advice")
    st.info(get_advice(label, confidence))

    st.divider()

    # ---------------- CO2 ----------------
    st.subheader("🌍 CO₂ Impact")
    st.metric("CO₂ (kg)", round(carbon, 2))

    st.divider()

    # ---------------- HISTORY PREVIEW ----------------
    st.subheader("📊 Recent Activity")

    st.write(pd.DataFrame(st.session_state.history[-5:]))

    st.divider()

else:
    st.info("Upload or capture an image to start analysis")

# =====================================================
# 📊 ANALYTICS DASHBOARD
# =====================================================

st.divider()
st.header("📊 Waste Analytics Dashboard")

if st.session_state.history:

    df = pd.DataFrame(st.session_state.history)

    # ---------------- PIE CHART ----------------
    st.subheader("🥧 Waste Type Distribution")

    fig1, ax1 = plt.subplots()
    df["category"].value_counts().plot(kind="pie", autopct="%1.1f%%", ax=ax1)
    ax1.set_ylabel("")
    st.pyplot(fig1)

    # ---------------- CO2 TREND ----------------
    st.subheader("📈 CO₂ Trend Over Time")

    fig2, ax2 = plt.subplots()
    df["co2"].cumsum().plot(ax=ax2, marker="o")
    ax2.set_title("Cumulative CO₂ Impact")
    ax2.set_xlabel("Scan Number")
    ax2.set_ylabel("CO₂ (kg)")
    st.pyplot(fig2)

else:
    st.info("No data yet. Start scanning to generate analytics.")

# =====================================================
# 📄 ECO REPORT SECTION
# =====================================================

st.divider()
st.header("📄 Eco Report System")

eco_score = max(0, 100 - st.session_state.total_co2 * 2)

st.metric("Eco Score", round(eco_score, 2))

if st.session_state.scan_count >= 10:

    if st.button("Generate Eco Report PDF"):

        data = {
            "scans": st.session_state.scan_count,
            "co2": round(st.session_state.total_co2, 2),
            "eco_score": round(eco_score, 2),
            "breakdown": st.session_state.waste_breakdown,
            "suggestions": "Reduce plastic usage, recycle more, and avoid single-use materials.",
            "history": st.session_state.history
        }

        file = generate_pdf_report(data)

        with open(file, "rb") as f:
            st.download_button(
                "Download Eco Report",
                f,
                file_name="eco_report.pdf"
            )

else:
    st.info("Do 10 scans to unlock Eco Report 📄")
