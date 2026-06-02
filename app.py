import streamlit as st
from PIL import Image

from utils.hf_model import predict_image
from utils.recycling import get_advice, local_guide

# ---------------------------
# PAGE CONFIG
# ---------------------------
st.set_page_config(page_title="EcoSort AI", layout="wide")

st.title("🌱 EcoSort AI - Smart Waste Classifier")
st.write("Upload or capture an image to classify waste and get recycling advice.")

st.divider()

# ---------------------------
# ANALYTICS COUNTER
# ---------------------------
if "count" not in st.session_state:
    st.session_state.count = 0

st.session_state.count += 1
st.metric("Images Processed", st.session_state.count)

st.divider()

# ---------------------------
# INPUT SECTION
# ---------------------------
uploaded_file = st.file_uploader("Upload Image", type=["jpg", "png", "jpeg"])
camera_img = st.camera_input("📸 Take a picture")

image = None

if uploaded_file:
    image = Image.open(uploaded_file)

if camera_img:
    image = Image.open(camera_img)

# ---------------------------
# MAIN LOGIC
# ---------------------------
if image:

    st.image(image, caption="Input Image", use_container_width=True)

    st.info("🔄 Analyzing image using AI model...")

    top1, top3 = predict_image(image)

    label = top1["label"]
    confidence = top1["score"]

    st.divider()

    # ---------------------------
    # TOP 3 PREDICTIONS
    # ---------------------------
    st.subheader("🔍 Top Predictions")

    for r in top3:
        st.write(f"• {r['label']} — {r['score']:.2f}")

    st.divider()

    # ---------------------------
    # MAIN RESULT
    # ---------------------------
    st.subheader("♻️ Final Prediction")

    st.success(f"{label}")
    st.info(f"Confidence: {confidence:.2f}")

    if confidence < 0.6:
        st.warning("⚠️ Low confidence — try a clearer image")

    st.divider()

    # ---------------------------
    # RECYCLING ADVICE
    # ---------------------------
    st.subheader("💡 Recycling Advice")
    st.success(get_advice(label))

    st.divider()

    # ---------------------------
    # EXPLANATION
    # ---------------------------
    st.subheader("🧠 Why this prediction?")

    st.write(
        f"The AI model detected visual patterns similar to '{label.lower()}' "
        "based on shape, texture, and object structure."
    )

    st.divider()

    # ---------------------------
    # LOCAL GUIDE
    # ---------------------------
    st.subheader("🌍 Local Recycling Guide")
    st.info(local_guide())

    st.divider()

    # ---------------------------
    # USER FEEDBACK
    # ---------------------------
    st.subheader("📊 Feedback")

    correct = st.radio("Was the prediction correct?", ["Yes", "No"])

    if correct == "No":
        st.warning("Thanks for feedback — this helps improve future versions.")

else:
    st.warning("Please upload or capture an image to start analysis.")
