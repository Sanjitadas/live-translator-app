# utils/tts.py

from gtts import gTTS
import os
import tempfile
import streamlit as st

def speak_text(text, lang_code="en"):
    try:
        # Convert text to speech using gTTS
        tts = gTTS(text=text, lang=lang_code)

        # Save to a temporary MP3 file
        with tempfile.NamedTemporaryFile(delete=False, suffix=".mp3") as tmp_file:
            temp_path = tmp_file.name
            tts.save(temp_path)

        # Play audio in Streamlit
        audio_bytes = open(temp_path, "rb").read()
        st.audio(audio_bytes, format="audio/mp3")

        # Optionally remove the temp file afterward
        os.remove(temp_path)

    except Exception as e:
        st.error(f"Error in TTS: {e}")







