import streamlit as st
from PIL import Image

from utils.clip_model import predict_waste_clip
from utils.recycling import get_advice, local_guide
from utils.climate import get_carbon_impact
from utils.report import generate_pdf_report

# ---------------- PAGE SETUP ----------------
st.set_page_config(page_title="EcoSort AI", layout="wide")

st.title("🌍 EcoSort AI — Impact Tracker System")
st.write("Track waste, CO₂ impact, and your environmental progress.")

st.divider()

# ---------------- SESSION STATE ----------------
if "scan_count" not in st.session_state:
    st.session_state.scan_count = 0

if "total_co2" not in st.session_state:
    st.session_state.total_co2 = 0

if "waste_breakdown" not in st.session_state:
    st.session_state.waste_breakdown = {
        "plastic": 0,
        "glass": 0,
        "metal": 0,
        "paper": 0,
        "organic": 0
    }

if "last_image" not in st.session_state:
    st.session_state.last_image = None

# ---------------- SIDEBAR DASHBOARD ----------------
with st.sidebar:
    st.header("🌍 Eco Mission")

    st.metric("Total Scans", st.session_state.scan_count)
    st.metric("Total CO₂ (kg)", round(st.session_state.total_co2, 2))

    progress = min(st.session_state.scan_count / 20, 1.0)
    st.progress(progress)

    if progress < 1:
        st.info("Goal: 20 scans → Unlock Eco Report")
    else:
        st.success("🎉 Eco Report Unlocked")

# ---------------- INPUT ----------------
st.subheader("📸 Upload or Capture Waste Image")

mode = st.radio("Input mode:", ["Upload", "Camera"])

image = None

if mode == "Upload":
    file = st.file_uploader("Upload image", type=["jpg", "png", "jpeg"])
    if file:
        image = Image.open(file)

elif mode == "Camera":
    cam = st.camera_input("Take picture")
    if cam:
        image = Image.open(cam)

st.divider()

# ---------------- MAIN LOGIC ----------------
if image:

    st.image(image, use_container_width=True)

    st.subheader("🤖 AI Analysis")

    top1, top3 = predict_waste_clip(image)

    label = top1["label"]
    confidence = top1["score"]

    # ---------------- IMPACT SCORE ----------------
    if "plastic" in label:
        impact_score = 8
        category = "plastic"
    elif "metal" in label:
        impact_score = 5
        category = "metal"
    elif "glass" in label:
        impact_score = 4
        category = "glass"
    elif "paper" in label:
        impact_score = 2
        category = "paper"
    else:
        impact_score = 6
        category = "organic"

    carbon = get_carbon_impact(label)

    # ---------------- UPDATE STATS ----------------
    st.session_state.scan_count += 1
    st.session_state.total_co2 += carbon
    st.session_state.waste_breakdown[category] += 1

    # ---------------- RESULT ----------------
    st.markdown("## 🔍 Result")

    col1, col2 = st.columns(2)

    with col1:
        st.success(label)

    with col2:
        st.metric("Confidence", f"{confidence:.2f}")

    if confidence < 0.5:
        st.warning("⚠️ Low confidence — retake image")

    st.divider()

    # ---------------- IMPACT ----------------
    st.markdown("## 🌍 Impact Score")

    st.progress(impact_score / 10)

    if impact_score <= 3:
        st.success("Low environmental impact 🌱")
    elif impact_score <= 6:
        st.warning("Medium impact ⚠️")
    else:
        st.error("High impact 🔥")

    st.divider()

    # ---------------- RECYCLING ADVICE ----------------
    st.markdown("## ♻️ Recycling Advice")
    st.info(get_advice(label, confidence))

    st.divider()

    # ---------------- CO2 ----------------
    st.markdown("## 🌍 CO₂ Footprint")
    st.metric("CO₂ (kg)", round(carbon, 2))

    st.divider()

    # ---------------- PROGRESS STORY ----------------
    st.markdown("## 🌱 Your Impact Story")

    if impact_score <= 3:
        st.success("Great choice 🌱 low environmental damage")
    elif impact_score <= 6:
        st.warning("Moderate impact ⚠️ try reducing waste")
    else:
        st.error("High impact 🔥 consider alternatives")

    st.divider()

    # ---------------- TOP 3 ----------------
    st.markdown("## 🔍 Other Possibilities")

    for r in top3:
        st.write(f"{r['label']} — {r['score']:.2f}")

    st.divider()

    # ---------------- LOCAL GUIDE ----------------
    st.markdown("## 🌍 Local Guide")
    st.info(local_guide())

else:
    st.info("👆 Upload or capture an image to begin analysis")

st.divider()

# ---------------- ECO REPORT ----------------
st.subheader("📄 Eco Report System")

eco_score = max(0, 100 - st.session_state.total_co2 * 2)

st.write(f"🌱 Eco Score: {round(eco_score, 2)}/100")

if st.session_state.scan_count >= 10:

    if st.button("Generate Eco Report PDF"):

        data = {
            "scans": st.session_state.scan_count,
            "co2": round(st.session_state.total_co2, 2),
            "eco_score": round(eco_score, 2),
            "breakdown": st.session_state.waste_breakdown,
            "suggestions": "Reduce plastic usage, separate waste properly, and reuse materials where possible."
        }

        file = generate_pdf_report(data)

        with open(file, "rb") as f:
            st.download_button(
                "Download Eco Report",
                f,
                file_name="eco_report.pdf"
            )

else:
    st.info("Do at least 10 scans to unlock Eco Report 📊")
