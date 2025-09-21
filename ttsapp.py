
from gtts import gTTS
import io
from langdetect import detect

def text_to_speech(text, filename="output.mp3", lang="ar",slow=False):
    """
    تحويل النص إلى كلام وحفظه في ملف صوتي.
    يرجع مسار الملف لو نجح، أو None لو النص فاضي.
    """

    if not text or not text.strip():
        return None  
    
    try:
        lang = detect(text)
        print("Language detected:", lang)
        tts = gTTS(text=text, lang=lang, slow=slow)
        mp3_fp = io.BytesIO()
        tts.write_to_fp(mp3_fp)
        mp3_fp.seek(0)
        return mp3_fp
    except Exception as e:
        print(f"خطأ في تحويل النص إلى كلام: {e}")
        return None

####################################################################################################################
import streamlit as st

st.title("📖 VisionSpeak - TTS APP")
st.header("Text To sound")
input_text = st.text_area("Enter Text")

lang = st.radio("Choose Language :", ["auto","ar", "en"], index=0, key="tts_lang")

slow = st.checkbox(" Slow Rrading", key="tts_slow")

if st.button("Read The Text", key="tts_btn"):
    audio_file = text_to_speech(input_text, lang=("ara+eng" if lang=="auto" else lang), slow=slow)
    
    if audio_file:
        st.audio(audio_file, format="audio/mp3")
        st.download_button(
            label="Download Audio",
            data=audio_file,
            file_name="text_output.mp3",
            mime="audio/mp3"
        )
    else:
        st.warning("No Text Found To Convert")