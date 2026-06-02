from utils.climate import get_carbon_impact
import streamlit as st
from PIL import Image

from utils.hf_model import predict_image
from utils.recycling import get_advice, local_guide

# -----------------------------
# PAGE CONFIG
# -----------------------------
st.set_page_config(
    page_title="EcoSort AI",
    page_icon="♻️",
    layout="wide"
)

# -----------------------------
# HEADER (STARTUP STYLE)
# -----------------------------
st.markdown("""
    <div style="text-align:center; padding: 10px;">
        <h1>♻️ EcoSort AI</h1>
        <p style="font-size:18px; color:gray;">
        Smart Waste Classification & Recycling Assistant
        </p>
    </div>
""", unsafe_allow_html=True)

st.markdown("---")

# -----------------------------
# SIDEBAR DASHBOARD
# -----------------------------
with st.sidebar:
    st.title("📊 Dashboard")

    if "count" not in st.session_state:
        st.session_state.count = 0

    st.session_state.count += 1

    st.metric("Scans Today", st.session_state.count)

    st.markdown("---")
    st.info("Upload or capture waste images to classify and get recycling advice.")

# -----------------------------
# INPUT MODE
# -----------------------------
st.subheader("📤 Input Mode")

# -----------------------------
# MODE CONTROL (IMPORTANT FIX)
# -----------------------------
if "mode" not in st.session_state:
    st.session_state.mode = "upload"

colA, colB = st.columns(2)

with colA:
    if st.button("📁 Upload Image"):
        st.session_state.mode = "upload"

with colB:
    if st.button("📸 Use Camera"):
        st.session_state.mode = "camera"

st.write(f"Current mode: **{st.session_state.mode}**")

image = None

# -----------------------------
# UPLOAD MODE
# -----------------------------
if st.session_state.mode == "upload":
    uploaded_file = st.file_uploader("Upload Image", type=["jpg", "png", "jpeg"])

    if uploaded_file:
        image = Image.open(uploaded_file)

# -----------------------------
# CAMERA MODE (ONLY WHEN SELECTED)
# -----------------------------
elif st.session_state.mode == "camera":
    camera_img = st.camera_input("Take a photo")

    # IMPORTANT: only trigger once image exists
    if camera_img:
        image = Image.open(camera_img)

# -----------------------------
# MAIN APP FLOW
# -----------------------------
if image:

    # IMAGE PREVIEW + ANALYSIS PANEL
    col1, col2 = st.columns([1, 1])

    with col1:
        st.markdown("### 🖼️ Input Image")
        st.image(image, use_container_width=True)

    with col2:
        st.markdown("### 🤖 AI Analysis")

        with st.spinner("AI is analyzing the image..."):
            top1, top3 = predict_image(image)

        label = top1["label"]
        confidence = top1["score"]
        carbon = get_carbon_impact(label)

        st.markdown("#### 🔍 Top Predictions")

        for r in top3:
            st.progress(float(r["score"]))
            st.write(f"**{r['label']}** — `{r['score']:.2f}`")

    st.markdown("---")

    # RESULT CARD
    st.markdown("## ♻️ Result")

    result_col1, result_col2, result_col3 = st.columns(3)

    with result_col1:
        st.markdown("""
        <div style="padding:15px; border-radius:10px; background-color:#1f1f1f;">
            <h3>Prediction</h3>
            <p style="font-size:18px;">{}</p>
        </div>
        """.format(label), unsafe_allow_html=True)

    with result_col2:
        st.markdown("""
        <div style="padding:15px; border-radius:10px; background-color:#1f1f1f;">
            <h3>Confidence</h3>
            <p style="font-size:18px;">{:.2f}</p>
        </div>
        """.format(confidence), unsafe_allow_html=True)

    with result_col3:
        if confidence < 0.6:
            st.warning("Low Confidence")
        else:
            st.success("High Confidence")

    st.markdown("---")
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
    st.info("Estimate based on material type")

    # RECYCLING ADVICE CARD
    st.markdown("## 💡 Recycling Insight")

    st.success(get_advice(label))

    st.markdown("---")

    # EXPLANATION SECTION
    st.markdown("## 🧠 AI Explanation")

    st.info(
        f"The model detected visual patterns similar to **{label.lower()}** "
        "based on shape, texture, and object structure learned from training data."
    )

    st.markdown("---")

    # LOCAL GUIDE
    st.markdown("## 🌍 Local Recycling Guide")

    st.warning(local_guide())

    st.markdown("---")

    # FEEDBACK
    st.markdown("## 📊 Feedback")

    feedback = st.radio("Was the prediction correct?", ["Yes", "No"])

    if feedback == "No":
        st.error("Thanks! This feedback helps improve the system.")

    else:
        st.markdown("""
        <div style="text-align:center; padding:40px;">
            <h3>📸 Upload or Capture an Image to Start</h3>
            <p style="color:gray;">AI will analyze waste type and suggest recycling steps</p>
        </div>
    """, unsafe_allow_html=True)
