# streamlit_app.py

import streamlit as st
import cv2
import numpy as np
from PIL import Image

# -------------------------------
# Page Config
# -------------------------------
st.set_page_config(
    page_title="Advanced OpenCV Streamlit App with Super-Resolution",
    layout="centered",
    page_icon="🖼️",
)

st.title("🖼️ Advanced OpenCV Streamlit App")
st.write(
    """
    📸 Upload an image or use your webcam.  
    ✨ Apply filters, transformations & AI upscaling (SD ➜ HD)!
    """
)

# -------------------------------
# Session State
# -------------------------------
if "img" not in st.session_state:
    st.session_state.img = None

# -------------------------------
# Input Source
# -------------------------------
option = st.sidebar.radio(
    "📷 Input Source",
    ("Upload Image", "Use Webcam"),
    horizontal=True,
)

if option == "Upload Image":
    uploaded_file = st.sidebar.file_uploader(
        "Choose an image...", type=["jpg", "jpeg", "png"]
    )
    if uploaded_file is not None:
        file_bytes = np.asarray(bytearray(uploaded_file.read()), dtype=np.uint8)
        img = cv2.imdecode(file_bytes, 1)
        st.session_state.img = img
    else:
        st.stop()

elif option == "Use Webcam":
    st.subheader("📸 Take a Picture")
    st.info("👉 Your camera preview is below. Use good lighting for better quality!")
    img_file_buffer = st.camera_input("Take a picture")
    if img_file_buffer is not None:
        img = Image.open(img_file_buffer)
        img = np.array(img)
        img = cv2.cvtColor(img, cv2.COLOR_RGB2BGR)
        st.session_state.img = img
    else:
        st.stop()

# -------------------------------
# Reset Button
# -------------------------------
if st.sidebar.button("🔄 Reset All"):
    st.session_state.img = None
    st.rerun()

# -------------------------------
# Work Copy
# -------------------------------
if st.session_state.img is None:
    st.warning("⚠️ No image loaded.")
    st.stop()

output = st.session_state.img.copy()

# -------------------------------
# Filters & Adjustments
# -------------------------------
st.sidebar.header("🎨 Filters & Adjustments")

# Grayscale
if st.sidebar.checkbox("Grayscale"):
    output = cv2.cvtColor(output, cv2.COLOR_BGR2GRAY)

# Blur
if st.sidebar.checkbox("Blur"):
    k = st.sidebar.slider("Kernel Size", 1, 25, 5, step=2)
    output = cv2.GaussianBlur(output, (k, k), 0)

# Canny Edge
if st.sidebar.checkbox("Canny Edge"):
    t1 = st.sidebar.slider("Threshold 1", 0, 300, 100)
    t2 = st.sidebar.slider("Threshold 2", 0, 300, 200)
    output = cv2.Canny(output, t1, t2)

# Brightness & Contrast
if st.sidebar.checkbox("Adjust Brightness/Contrast"):
    brightness = st.sidebar.slider("Brightness", -100, 100, 0)
    contrast = st.sidebar.slider("Contrast", 0.5, 3.0, 1.0, step=0.1)
    if len(output.shape) == 2:
        output = cv2.cvtColor(output, cv2.COLOR_GRAY2BGR)
    output = cv2.convertScaleAbs(output, alpha=contrast, beta=brightness)

# -------------------------------
# Transform Tools
# -------------------------------
st.sidebar.header("🔄 Transform")

# Rotation
if st.sidebar.checkbox("Rotate"):
    angle = st.sidebar.slider("Angle", -180, 180, 0)
    (h, w) = output.shape[:2]
    center = (w // 2, h // 2)
    M = cv2.getRotationMatrix2D(center, angle, 1.0)
    output = cv2.warpAffine(output, M, (w, h))

# Flip
flip_option = st.sidebar.selectbox("Flip Image", ("None", "Horizontal", "Vertical"))
if flip_option == "Horizontal":
    output = cv2.flip(output, 1)
elif flip_option == "Vertical":
    output = cv2.flip(output, 0)

# -------------------------------
# Draw Tools
# -------------------------------
st.sidebar.header("✏️ Annotate")

if st.sidebar.checkbox("Draw Rectangle"):
    x = st.sidebar.slider("X", 0, output.shape[1], 50)
    y = st.sidebar.slider("Y", 0, output.shape[0], 50)
    w = st.sidebar.slider("Width", 1, output.shape[1], 100)
    h = st.sidebar.slider("Height", 1, output.shape[0], 100)
    color = (255, 0, 0)
    thickness = 2
    output = cv2.rectangle(output, (x, y), (x + w, y + h), color, thickness)

if st.sidebar.checkbox("Add Text"):
    text = st.sidebar.text_input("Text", "OpenCV Streamlit!")
    pos_x = st.sidebar.slider("Text X", 0, output.shape[1], 50)
    pos_y = st.sidebar.slider("Text Y", 0, output.shape[0], 50)
    font_scale = st.sidebar.slider("Font Scale", 0.5, 3.0, 1.0)
    font_color = (0, 0, 255)
    output = cv2.putText(
        output, text, (pos_x, pos_y), cv2.FONT_HERSHEY_SIMPLEX, font_scale, font_color, 2
    )

# -------------------------------
# Face Detection
# -------------------------------
st.sidebar.header("👤 Face Detection")

if st.sidebar.checkbox("Detect Faces"):
    face_cascade = cv2.CascadeClassifier(
        cv2.data.haarcascades + "haarcascade_frontalface_default.xml"
    )
    gray = cv2.cvtColor(output, cv2.COLOR_BGR2GRAY) if len(output.shape) == 3 else output
    faces = face_cascade.detectMultiScale(gray, 1.1, 4)
    for (x, y, w, h) in faces:
        output = cv2.rectangle(output, (x, y), (x + w, y + h), (0, 255, 0), 2)

# -------------------------------
# AI Super-Resolution SD ➜ HD
# -------------------------------
st.sidebar.header("📈 Super-Resolution")

if st.sidebar.checkbox("Convert SD ➜ HD"):
    try:
        sr = cv2.dnn_superres.DnnSuperResImpl_create()
        # You must download EDSR_x4.pb and put it in your project folder
        sr.readModel("EDSR_x4.pb")
        sr.setModel("edsr", 4)  # or other scale
        output = sr.upsample(output)
        st.success("✅ Image upscaled using AI Super-Resolution (EDSR x4).")
    except Exception as e:
        st.error(f"⚠️ Error: {e}")
        st.info(
            "👉 Make sure you have EDSR_x4.pb in your project folder.\n"
            "Download from: https://github.com/Saafke/EDSR_Tensorflow"
        )

# -------------------------------
# Show Result
# -------------------------------
st.subheader("📌 Processed Image")

if len(output.shape) == 2:
    st.image(output, channels="GRAY", use_container_width=True)
else:
    output_rgb = cv2.cvtColor(output, cv2.COLOR_BGR2RGB)
    st.image(output_rgb, channels="RGB", use_container_width=True)

# -------------------------------
# Download
# -------------------------------
file_format = st.sidebar.selectbox("📥 Download Format", ("PNG", "JPEG"))
result_img = output_rgb if len(output.shape) == 3 else output

result_pil = Image.fromarray(result_img)
buffer = cv2.imencode(
    ".png" if file_format == "PNG" else ".jpg", np.array(result_pil)
)[1].tobytes()

st.download_button(
    label=f"⬇️ Download as {file_format}",
    data=buffer,
    file_name=f"processed_image.{file_format.lower()}",
    mime="image/png" if file_format == "PNG" else "image/jpeg",
)

st.info("✅ Try different filters & AI upscaling for best results!")
