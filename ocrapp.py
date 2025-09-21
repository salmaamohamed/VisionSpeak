import streamlit as st
import pytesseract
from PIL import Image
from gtts import gTTS
from langdetect import detect
import io
import pdfplumber

def image_to_text(img, lang="ara+eng"):
    """تحويل صورة إلى نص"""
    image = Image.open(img)
    text = pytesseract.image_to_string(image, lang=lang)
    return text.strip()

def pdf_to_text(pdf_file):
    """استخراج النصوص من PDF"""
    text = ""
    with pdfplumber.open(pdf_file) as pdf:
        for page in pdf.pages:
            text += page.extract_text() or ""
    return text.strip()

def text_to_speech(text, slow=False):
    """تحويل النص إلى كلام"""
    if not text.strip():
        return None, None
    try:
        lang = detect(text)
        tts = gTTS(text=text, lang=lang, slow=slow)
        mp3_fp = io.BytesIO()
        tts.write_to_fp(mp3_fp)
        mp3_fp.seek(0)
        return mp3_fp, lang
    except Exception as e:
        st.error(f"خطأ في تحويل النص إلى كلام: {e}")
        return None, None

st.title("📖 VisionSpeak - OCR APP")
st.header("Image/PDF to Text")
uploaded_file = st.file_uploader("Upload Image or PDF", type=["png", "jpg", "jpeg", "pdf"])
if uploaded_file:
    if uploaded_file.name.endswith(".pdf"):
        text = pdf_to_text(uploaded_file)
    else:
        text = image_to_text(uploaded_file)

    st.subheader("Extracted Text")
    st.text_area("", text, height=200)

    if st.button("Read Text"):
        audio, lang = text_to_speech(text)
        if audio:
            st.audio(audio)
            st.download_button("Download Audio", audio, file_name="ocr_output.mp3") 