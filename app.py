import streamlit as st
from PIL import Image

from utils.clip_model import predict_waste_clip
from utils.recycling import get_advice, local_guide
from utils.climate import get_carbon_impact

# ---------------- PAGE CONFIG ----------------
st.set_page_config(page_title="EcoSort Impact Tracker", layout="wide")

st.title("🌍 EcoSort AI — Impact Tracker")
st.write("Not just classification — track your environmental impact over time.")

st.divider()

# ---------------- SESSION STATE ----------------
if "scan_count" not in st.session_state:
    st.session_state.scan_count = 0

if "total_impact" not in st.session_state:
    st.session_state.total_impact = 0

# ---------------- SIDEBAR (MISSION SYSTEM) ----------------
with st.sidebar:
    st.header("🌍 Your Eco Mission")

    st.metric("Scans", st.session_state.scan_count)
    st.metric("Total Impact Score", st.session_state.total_impact)

    st.write("🎯 Goal: 20 scans = Eco Report Unlock")

    progress = min(st.session_state.scan_count / 20, 1.0)
    st.progress(progress)

    if progress < 1:
        st.info("Keep going 🌱 you're building impact awareness")
    else:
        st.success("🎉 Eco Report Unlocked!")

# ---------------- INPUT ----------------
st.subheader("📸 Upload or Capture Waste Image")

mode = st.radio("Choose input:", ["Upload", "Camera"])

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

    # ---------------- IMPACT SYSTEM ----------------
    if "plastic" in label:
        impact_score = 8
    elif "metal" in label:
        impact_score = 5
    elif "glass" in label:
        impact_score = 4
    elif "paper" in label:
        impact_score = 2
    else:
        impact_score = 6

    # ---------------- UPDATE STATS ----------------
    st.session_state.scan_count += 1
    st.session_state.total_impact += impact_score

    # ---------------- RESULTS ----------------
    st.markdown("## 🔍 Result")

    col1, col2 = st.columns(2)

    with col1:
        st.success(f"{label}")

    with col2:
        st.metric("Confidence", f"{confidence:.2f}")

    st.divider()

    # ---------------- IMPACT SECTION ----------------
    st.markdown("## 🌍 Environmental Impact")

    st.progress(impact_score / 10)

    if impact_score <= 3:
        st.success("Low Impact 🌱 Good environmental choice")
    elif impact_score <= 6:
        st.warning("Medium Impact ⚠️ Try better recycling")
    else:
        st.error("High Impact 🔥 Environmental concern")

    st.write(f"Impact Score: {impact_score}/10")

    st.divider()

    # ---------------- RECYCLING ADVICE ----------------
    st.markdown("## ♻️ Recycling Advice")
    st.info(get_advice(label, confidence))

    st.divider()

    # ---------------- CO2 ----------------
    carbon = get_carbon_impact(label)

    st.markdown("## 🌍 CO₂ Footprint")
    st.metric("CO₂ Impact", f"{carbon} kg")

    st.divider()

    # ---------------- PERSONAL IMPACT MESSAGE ----------------
    st.markdown("## 🌱 Your Impact Story")

    if impact_score <= 3:
        st.success("Great job 🌱 You chose a low-impact item.")
    elif impact_score <= 6:
        st.warning("Moderate impact ⚠️ You can improve your waste habits.")
    else:
        st.error("High impact detected 🔥 Try reducing plastic usage.")

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
    st.info("👆 Upload or capture an image to start your eco impact journey")
