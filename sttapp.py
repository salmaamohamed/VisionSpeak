import streamlit as st
import whisper
import tempfile
import os, shutil

def speech_to_text(uploaded_audio, model_name="base", lang=None):
    """تحويل الصوت إلى نص باستخدام Whisper"""
    model = whisper.load_model(model_name)

    with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as tmp:
        tmp.write(uploaded_audio.read())
        tmp_path = tmp.name

    result = model.transcribe(tmp_path, language=lang)
    return result["text"].strip()

st.title("📖 VisionSpeak - STT APP")
st.header("Sound To Text")

uploaded_audio = st.file_uploader("Upload Audio File", type=["mp3", "wav"])
if uploaded_audio:
    lang_choice = st.radio("Choose Language:", ["auto", "ar", "en"], index=0)
    lang = None if lang_choice == "auto" else lang_choice

    text = speech_to_text(uploaded_audio, model_name="base", lang=lang)
    st.subheader("Extracted Text")
    st.text_area("", text, height=200)
