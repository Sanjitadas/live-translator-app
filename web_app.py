# web_app.py

import streamlit as st
from utils.stt import record_and_transcribe_async, stop_and_transcribe
from utils.ai_translator import ai_translate_with_dialects
from utils.tts import speak_text
import os

st.set_page_config(page_title="🎙️ Live Multilingual Translator", layout="centered")

st.markdown("<h2 style='text-align: center;'>🎙️ Live Multilingual Translator</h2>", unsafe_allow_html=True)

# 🌐 Language Options
languages = {
    "Indian English": "en-IN",
    "US English": "en",
    "Hindi": "hi",
    "Spanish": "es"
}

# State Variables
if "recording" not in st.session_state:
    st.session_state["recording"] = False
if "transcript" not in st.session_state:
    st.session_state["transcript"] = ""
if "translated" not in st.session_state:
    st.session_state["translated"] = ""
if "audio_path" not in st.session_state:
    st.session_state["audio_path"] = None

# 🎯 Language Selection
col1, col2 = st.columns(2)
with col1:
    input_lang_name = st.selectbox("🎯 Input Language", list(languages.keys()), index=0)
with col2:
    output_lang_name = st.selectbox("🌍 Output Language", list(languages.keys()), index=1)

input_lang = languages[input_lang_name]
output_lang = languages[output_lang_name]

# 🔁 Mode
mode = st.radio("🔁 Choose Mode", ["TTT (Text-to-Text)", "STT (Speech-to-Text)", "TTS (Text-to-Speech)", "STS (Speech-to-Speech)"])

# ✍️ Input Box
text_input = st.text_area("✍️ Type or Speak:", placeholder="You can type or record, then click Translate")

# 🎤 Upload or Record
if mode in ["STT (Speech-to-Text)", "STS (Speech-to-Speech)"]:
    uploaded_file = st.file_uploader("🎤 Upload a WAV audio file for transcription", type=["wav"])
    if uploaded_file:
        temp_path = "output/temp_live.wav"
        with open(temp_path, "wb") as f:
            f.write(uploaded_file.read())
        st.success("✅ Audio file uploaded.")

        if st.button("🧠 Transcribe Audio"):
            st.session_state["transcript"] = stop_and_transcribe(lang_code=input_lang)
            st.success(f"🗣️ You said:\n\n{st.session_state['transcript']}")

# 🔁 Translate Button
if st.button("🌐 Translate"):
    if mode.startswith("TTT") and text_input.strip():
        transcript = text_input.strip()
    elif mode.startswith("STT") or mode.startswith("STS"):
        transcript = st.session_state["transcript"]
    else:
        transcript = text_input.strip()

    if transcript:
        translated_text = ai_translate_with_dialects(transcript, input_lang_name, output_lang_name)
        st.session_state["translated"] = translated_text

        # Save to output.txt
        with open("output/output.txt", "w", encoding="utf-8") as f:
            f.write(translated_text)

        # TTS or STS mode: speak it
        if mode in ["TTS (Text-to-Speech)", "STS (Speech-to-Speech)"]:
            speak_text(translated_text)

        st.success(f"✅ Translated:\n\n{translated_text}")



















