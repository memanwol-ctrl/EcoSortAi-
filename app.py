import streamlit as st
from PIL import Image

from utils.hf_model import predict_image
from utils.recycling import map_waste, get_advice

st.set_page_config(page_title="EcoSort AI", layout="wide")

st.title("🌱 EcoSort AI - Smart Waste Classifier (AI Powered)")

st.write("Upload an image and get waste classification + recycling advice.")

uploaded_file = st.file_uploader("Upload Image", type=["jpg", "png", "jpeg"])

if uploaded_file:

    image = Image.open(uploaded_file)
    st.image(image, caption="Uploaded Image", use_container_width=True)

    st.info("Analyzing image using HuggingFace AI...")

    label, confidence = predict_image(image)

    category = map_waste(label)
    advice = get_advice(category)

    st.subheader("🔍 Prediction Result")
    st.write("Raw Model Label:", label)
    st.write(f"Confidence: {confidence:.2f}")

    st.subheader("♻️ Waste Category")
    st.success(category)

    st.subheader("💡 Recycling Advice")
    st.info(advice)

    if confidence < 0.5:
        st.warning("Low confidence prediction. Try a clearer image.")
