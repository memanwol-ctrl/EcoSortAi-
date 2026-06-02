import streamlit as st
from PIL import Image

from utils.hf_model import predict_image
from utils.recycling import get_advice, local_guide
from utils.climate import get_carbon_impact

# -----------------------------
# PAGE CONFIG
# -----------------------------
st.set_page_config(page_title="EcoSort AI", layout="wide")

st.title("🌱 EcoSort AI")
st.write("AI-powered waste classification with climate impact insights")

st.divider()

# -----------------------------
# SESSION STATE INIT
# -----------------------------
if "scan_count" not in st.session_state:
    st.session_state.scan_count = 0

if "last_image_hash" not in st.session_state:
    st.session_state.last_image_hash = None

# -----------------------------
# SIDEBAR DASHBOARD
# -----------------------------
with st.sidebar:
    st.header("📊 Dashboard")
    st.metric("Total Scans", st.session_state.scan_count)

    st.markdown("---")
    st.info("Upload or capture waste images for AI analysis")

# -----------------------------
# INPUT MODE (FIXED CAMERA ISSUE)
# -----------------------------
st.subheader("📤 Input Section")

mode = st.radio("Choose input method:", ["Upload", "Camera"])

image = None

if mode == "Upload":
    uploaded_file = st.file_uploader("Upload Image", type=["jpg", "png", "jpeg"])

    if uploaded_file:
        image = Image.open(uploaded_file)

elif mode == "Camera":
    camera_img = st.camera_input("Take a picture")

    if camera_img:
        image = Image.open(camera_img)

st.divider()

# -----------------------------
# MAIN PROCESSING
# -----------------------------
if image:

    st.subheader("🖼️ Input Preview")
    st.image(image, use_container_width=True)

    st.divider()

    st.subheader("🤖 AI Analysis")

    with st.spinner("Analyzing image..."):
        top1, top3 = predict_image(image)

    label = top1["label"]
    confidence = top1["score"]

    # -----------------------------
    # REAL SCAN TRACKING FIX
    # -----------------------------
    image_id = str(image.tobytes()[:50])

    if st.session_state.last_image_hash != image_id:
        st.session_state.scan_count += 1
        st.session_state.last_image_hash = image_id

    # -----------------------------
    # TOP 3 RESULTS
    # -----------------------------
    st.markdown("### 🔍 Prediction Breakdown")

    for r in top3:
        st.progress(float(r["score"]))
        st.write(f"**{r['label']}** — {r['score']:.2f}")

    st.divider()

    # -----------------------------
    # FINAL RESULT CARD
    # -----------------------------
    st.markdown("## ♻️ Final Result")

    col1, col2, col3 = st.columns(3)

    with col1:
        st.success(label)

    with col2:
        st.metric("Confidence", f"{confidence:.2f}")

    with col3:
        if confidence < 0.6:
            st.warning("Low confidence")
        else:
            st.success("High confidence")

    st.divider()

    # -----------------------------
    # RECYCLING ADVICE
    # -----------------------------
    st.markdown("## 💡 Recycling Advice")
    st.info(get_advice(label))

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
    # AI EXPLANATION
    # -----------------------------
    st.markdown("## 🧠 AI Explanation")

    st.write(
        f"The model identified this as **{label.lower()}** "
        "based on learned visual patterns like shape and texture."
    )

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

    feedback = st.radio("Was prediction correct?", ["Yes", "No"])

    if feedback == "No":
        st.warning("Thanks for feedback — helps improve model accuracy")

else:
    st.info("👆 Upload or capture an image to start analysis")
