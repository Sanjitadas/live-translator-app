# web_app.py

import streamlit as st
from utils.stt import record_and_transcribe_async, stop_and_transcribe
from utils.ai_translator import ai_translate_with_dialects
from utils.tts import speak_text
import time
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

# 🎤 Start Recording
if mode in ["STT (Speech-to-Text)", "STS (Speech-to-Speech)"]:
    if not st.session_state["recording"]:
        if st.button("🎤 Start Recording"):
            st.session_state["recording"] = True
            record_and_transcribe_async()
            st.success("🔴 Recording... Click '⏹️ Stop Recording' when done.")
    else:
        if st.button("⏹️ Stop Recording"):
            st.session_state["recording"] = False
            st.info("🛑 Stopped. Processing...")
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
                # TTS or STS mode: speak it
        if mode in ["TTS (Text-to-Speech)", "STS (Speech-to-Speech)"]:
            st.session_state["audio_path"] = speak_text(translated_text, lang=output_lang)

# Show Results
if st.session_state["transcript"]:
    st.markdown("### 🗣️ You said:")
    st.text_area("Transcript", st.session_state["transcript"], height=100)

if st.session_state["translated"]:
    st.markdown(f"### ✅ {output_lang_name} (Translated Output):")
    st.text_area("Output", st.session_state["translated"], height=100)

if st.session_state["audio_path"] and os.path.exists(st.session_state["audio_path"]):
    st.audio(st.session_state["audio_path"], format="audio/mp3")
















