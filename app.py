import streamlit as st
from PIL import Image

from utils.hf_model import predict_image
from utils.recycling import get_advice, local_guide
from utils.climate import get_carbon_impact

# -----------------------------
# PAGE CONFIG
# -----------------------------
st.set_page_config(page_title="EcoSort AI", layout="wide")

st.title("🌱 EcoSort AI - Smart Waste & Climate Assistant")
st.write("Upload or capture an image to analyze waste and environmental impact.")

st.divider()

# -----------------------------
# SIDEBAR STATS
# -----------------------------
with st.sidebar:
    st.header("📊 Dashboard")

    if "count" not in st.session_state:
        st.session_state.count = 0

    st.session_state.count += 1

    st.metric("Total Scans", st.session_state.count)

    st.markdown("---")
    st.info("AI-powered waste classification + climate impact analysis")

# -----------------------------
# INPUT MODE (FIXED CAMERA ISSUE)
# -----------------------------
st.subheader("📤 Input Section")

mode = st.radio("Choose Input Mode:", ["Upload Image", "Use Camera"])

image = None

if mode == "Upload Image":
    uploaded_file = st.file_uploader("Upload Image", type=["jpg", "png", "jpeg"])

    if uploaded_file:
        image = Image.open(uploaded_file)

elif mode == "Use Camera":
    camera_img = st.camera_input("Take a picture")

    if camera_img:
        image = Image.open(camera_img)

st.divider()

# -----------------------------
# MAIN LOGIC
# -----------------------------
if image:

    # IMAGE DISPLAY
    st.subheader("🖼️ Input Image")
    st.image(image, use_container_width=True)

    st.divider()

    # AI ANALYSIS
    st.subheader("🤖 AI Analysis")

    with st.spinner("Analyzing image..."):
        top1, top3 = predict_image(image)

    label = top1["label"]
    confidence = top1["score"]

    # -----------------------------
    # TOP 3 PREDICTIONS
    # -----------------------------
    st.markdown("### 🔍 Top Predictions")

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
    # 🌍 CLIMATE IMPACT (FIXED)
    # -----------------------------
    carbon = get_carbon_impact(label)

    st.markdown("## 🌍 Climate Impact")

    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric("CO₂ Impact", f"{carbon} kg")

    with col2:
        if carbon <= 0.05:
            st.success("Low Impact 🌱")
        elif carbon <= 0.15:
            st.warning("Medium Impact 🌿")
        else:
            st.error("High Impact 🔥")

    with col3:
        st.info("Estimated environmental footprint")

    st.divider()

    # -----------------------------
    # EXPLANATION
    # -----------------------------
    st.markdown("## 🧠 AI Explanation")

    st.write(
        f"The AI detected patterns similar to **{label.lower()}** "
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

    feedback = st.radio("Was the prediction correct?", ["Yes", "No"])

    if feedback == "No":
        st.warning("Thanks for your feedback — it helps improve the system.")

else:
    st.info("👆 Upload or capture an image to start analysis.")
