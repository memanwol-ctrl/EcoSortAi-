import streamlit as st
from PIL import Image

from utils.hf_model import predict_image
from utils.recycling import get_advice, local_guide

# -----------------------------
# PAGE CONFIG
# -----------------------------
st.set_page_config(
    page_title="EcoSort AI",
    layout="wide"
)

st.title("🌱 EcoSort AI - Smart Waste Intelligence System")
st.write("Upload or capture an image to analyze waste and get recycling guidance.")

st.divider()

# -----------------------------
# ANALYTICS
# -----------------------------
if "count" not in st.session_state:
    st.session_state.count = 0

st.session_state.count += 1

st.metric("Images Analyzed", st.session_state.count)

st.divider()

# -----------------------------
# INPUT SECTION (FIXED CAMERA UX)
# -----------------------------
st.subheader("📤 Input Section")

use_camera = st.checkbox("📸 Use Camera Instead of Upload")

image = None

if use_camera:
    camera_img = st.camera_input("Take a picture")

    if camera_img:
        image = Image.open(camera_img)

else:
    uploaded_file = st.file_uploader("Upload Image", type=["jpg", "png", "jpeg"])

    if uploaded_file:
        image = Image.open(uploaded_file)

st.divider()

# -----------------------------
# MAIN ANALYSIS FLOW
# -----------------------------
if image:

    st.subheader("🖼️ Uploaded Image")
    st.image(image, use_container_width=True)

    st.subheader("📊 AI Analysis")

    with st.spinner("Analyzing image using AI model..."):
        top1, top3 = predict_image(image)

    label = top1["label"]
    confidence = top1["score"]

    # -----------------------------
    # TOP 3 PREDICTIONS
    # -----------------------------
    st.markdown("### 🔍 Prediction Breakdown")

    for r in top3:
        st.progress(float(r["score"]))
        st.write(f"**{r['label']}** — {r['score']:.2f}")

    st.divider()

    # -----------------------------
    # FINAL RESULT (CLEAN UI)
    # -----------------------------
    st.markdown("## ♻️ Final Result")

    col1, col2 = st.columns(2)

    with col1:
        st.success(f"{label}")

    with col2:
        st.metric("Confidence", f"{confidence:.2f}")

    if confidence < 0.6:
        st.warning("⚠️ Low confidence — try a clearer image")

    st.divider()

    # -----------------------------
    # RECYCLING ADVICE
    # -----------------------------
    st.markdown("## 💡 Recycling Advice")
    st.info(get_advice(label))

    st.divider()

    # -----------------------------
    # AI EXPLANATION
    # -----------------------------
    st.markdown("## 🧠 AI Explanation")

    st.write(
        f"The model detected visual patterns similar to **{label.lower()}** "
        "based on shape, texture, and object features learned during training."
    )

    st.divider()

    # -----------------------------
    # LOCAL GUIDE
    # -----------------------------
    st.markdown("## 🌍 Local Recycling Guide")
    st.info(local_guide())

    st.divider()

    # -----------------------------
    # FEEDBACK
    # -----------------------------
    st.markdown("## 📊 Feedback")

    correct = st.radio("Was this prediction correct?", ["Yes", "No"])

    if correct == "No":
        st.warning("Thanks for feedback — this will help improve future versions.")

else:
    st.info("👆 Upload or capture an image to start analysis.")
