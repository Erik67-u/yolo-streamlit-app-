import streamlit as st
import requests
from PIL import Image
import io
import base64

# =====================
# CONFIG
# =====================
ENDPOINT_URL = "https://YOUR-ENDPOINT.azurewebsites.net/score"
API_KEY = "YOUR_API_KEY"

headers = {
    "Content-Type": "application/json",
    "Authorization": f"Bearer {API_KEY}"
}

# =====================
# STREAMLIT UI
# =====================
st.set_page_config(page_title="YOLO Object Detection", layout="centered")

st.title("🤖 YOLO Object Detection (Hugging Face + Azure ML)")
st.write("Lade ein Bild hoch und lasse KI Objekte erkennen")

uploaded_file = st.file_uploader("Bild hochladen", type=["jpg", "png", "jpeg"])

# =====================
# IMAGE HANDLING
# =====================
def image_to_base64(img):
    buffer = io.BytesIO()
    img.save(buffer, format="JPEG")
    return base64.b64encode(buffer.getvalue()).decode()

# =====================
# API REQUEST
# =====================
def predict(image_base64):
    payload = {
        "input_data": {
            "columns": ["image"],
            "data": [image_base64]
        }
    }

    response = requests.post(ENDPOINT_URL, json=payload, headers=headers)
    return response.json()

# =====================
# MAIN LOGIC
# =====================
if uploaded_file is not None:
    image = Image.open(uploaded_file)
    st.image(image, caption="Dein Bild", use_container_width=True)

    if st.button("🔍 Objekte erkennen"):
        with st.spinner("KI analysiert Bild..."):

            img_b64 = image_to_base64(image)
            result = predict(img_b64)

            st.success("Fertig!")

            st.json(result)
