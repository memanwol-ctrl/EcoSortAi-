import streamlit as st
from PIL import Image

from utils.hf_model import predict_image
from utils.recycling import get_advice, local_guide
from utils.climate import get_carbon_impact

# -----------------------------
# PAGE CONFIG
# -----------------------------
st.set_page_config(page_title="EcoSort AI", layout="wide")

st.title("🌱 EcoSort AI — Waste & Climate Intelligence")
st.write("Upload or capture waste images for AI classification and environmental insights.")

st.divider()

# -----------------------------
# SESSION STATE (SAFE SCAN TRACKING)
# -----------------------------
if "scan_count" not in st.session_state:
    st.session_state.scan_count = 0

if "last_image_id" not in st.session_state:
    st.session_state.last_image_id = None

# -----------------------------
# SIDEBAR DASHBOARD
# -----------------------------
with st.sidebar:
    st.header("📊 Dashboard")
    st.metric("Total Scans", st.session_state.scan_count)
    st.info("AI detects waste type + recycling + climate impact")

# -----------------------------
# INPUT SECTION (FIXED CAMERA ISSUE)
# -----------------------------
st.subheader("📤 Input Section")

mode = st.radio("Choose input method:", ["Upload Image", "Use Camera"])

image = None

if mode == "Upload Image":
    file = st.file_uploader("Upload image", type=["jpg", "png", "jpeg"])
    if file:
        image = Image.open(file)

elif mode == "Use Camera":
    cam = st.camera_input("Capture image")
    if cam:
        image = Image.open(cam)

st.divider()

# -----------------------------
# MAIN PROCESSING
# -----------------------------
if image:

    st.subheader("🖼️ Image Preview")
    st.image(image, use_container_width=True)

    st.divider()

    st.subheader("🤖 AI Analysis")

    with st.spinner("Analyzing waste type..."):
        top1, top3 = predict_image(image)

    label = top1["label"]
    confidence = top1["score"]

    # -----------------------------
    # REAL SCAN TRACKING (FIXED)
    # -----------------------------
    image_id = str(image.tobytes()[:60])

    if st.session_state.last_image_id != image_id:
        st.session_state.scan_count += 1
        st.session_state.last_image_id = image_id

    # -----------------------------
    # TOP 3 RESULTS
    # -----------------------------
    st.markdown("### 🔍 Prediction Breakdown")

    for r in top3:
        st.progress(float(r["score"]))
        st.write(f"**{r['label']}** — {r['score']:.2f}")

    st.divider()

    # -----------------------------
    # FINAL RESULT
    # -----------------------------
    st.markdown("## ♻️ Final Result")

    col1, col2 = st.columns(2)

    with col1:
        st.success(label)

    with col2:
        st.metric("Confidence", f"{confidence:.2f}")

    if confidence < 0.6:
        st.warning("⚠️ Low confidence — try a clearer image")

    st.divider()

    # -----------------------------
    # RECYCLING ADVICE (IMPROVED SOURCE)
    # -----------------------------
    st.markdown("## 💡 Recycling Advice")
    st.info(get_advice(label, confidence))

    st.divider()

    # -----------------------------
    # 🌍 CLIMATE IMPACT
    # -----------------------------
    carbon = get_carbon_impact(label)

    st.markdown("## 🌍 Climate Impact")

    c1, c2, c3 = st.columns(3)

    with c1:
        st.metric("CO₂ Impact", f"{carbon} kg")

    with c2:
        if carbon <= 0.05:
            st.success("Low Impact 🌱")
        elif carbon <= 0.15:
            st.warning("Medium Impact 🌿")
        else:
            st.error("High Impact 🔥")

    with c3:
        st.info("Estimated environmental footprint")

    st.divider()

    # -----------------------------
    # AI EXPLANATION (CLEANED)
    # -----------------------------
    st.markdown("## 🧠 AI Explanation")

    st.write(
        f"This object was classified as **{label}** because the model detected "
        "visual similarities in shape, texture, and structure compared to training data."
    )

    st.info("💡 Tip: clearer lighting improves accuracy significantly.")

    st.divider()

    # -----------------------------
    # LOCAL GUIDE
    # -----------------------------
    st.markdown("## 🌍 Local Recycling Guide")
    st.info(local_guide())

    st.divider()

    # -----------------------------
    # FEEDBACK SYSTEM
    # -----------------------------
    st.markdown("## 📊 Feedback")

    feedback = st.radio("Was this prediction correct?", ["Yes", "No"])

    if feedback == "No":
        st.warning("Thanks — your feedback helps improve the system.")

else:
    st.info("👆 Upload or capture an image to start analysis")
