# web_app.py
import streamlit as st
from utils.stt import record_and_transcribe_async, stop_and_transcribe
from utils.ai_translator import ai_translate_with_dialects
from utils.tts import speak_text

# 🌐 ISO codes map
lang_code_map = {
    "Indian English": "en",
    "US English": "en",
    "Hindi": "hi",
    "Spanish": "es"
}

st.set_page_config(page_title="Live Multilingual Translator", layout="centered")

st.markdown("## 🎙️ Live Multilingual Translator")

# 🎯 Language selectors
col1, col2 = st.columns(2)
with col1:
    input_lang = st.selectbox("🎯 Input Language", options=list(lang_code_map.keys()), index=0)
with col2:
    output_lang = st.selectbox("🌍 Output Language", options=list(lang_code_map.keys()), index=1)

# 🔁 Mode selector
mode = st.radio("🔁 Choose Mode", options=["TTT (Text-to-Text)", "STT (Speech-to-Text)", "TTS (Text-to-Speech)", "STS (Speech-to-Speech)"])

# 🎙️ User input
user_input = st.text_area("✍️ Type or Speak:", placeholder="You can type or record, then click Translate")

# 🧠 States
if "recording" not in st.session_state:
    st.session_state.recording = False
if "transcript" not in st.session_state:
    st.session_state.transcript = ""
if "translated" not in st.session_state:
    st.session_state.translated = ""

# 🎤 Start Recording
if st.button("🎤 Start Recording"):
    st.session_state.recording = True
    st.session_state.transcript = ""
    status = record_and_transcribe_async()
    st.success("🔴 Recording...")

# ⏹️ Stop Recording
if st.session_state.recording:
    if st.button("⏹️ Stop"):
        st.session_state.recording = False
        lang_code = lang_code_map.get(input_lang, "en")
        transcript = stop_and_transcribe(lang_code=lang_code)
        st.session_state.transcript = transcript
        st.success("🛑 Stopped. Processing...")

        translated = ai_translate_with_dialects(transcript, input_lang, output_lang)
        st.session_state.translated = translated

        with open("output/output.txt", "w", encoding="utf-8") as f:
            f.write(translated)

        if "TTS" in mode or "STS" in mode:
            speak_text(translated)

# 🔁 Translate Button
if st.button("🔁 Translate"):
    if user_input.strip():
        st.session_state.transcript = user_input
        translated = ai_translate_with_dialects(user_input, input_lang, output_lang)
        st.session_state.translated = translated

        with open("output/output.txt", "w", encoding="utf-8") as f:
            f.write(translated)

        if "TTS" in mode or "STS" in mode:
            speak_text(translated)

# 🎯 Display Output
if st.session_state.transcript:
    st.markdown("### 🗣️ You said:")
    st.text_area("Transcript", st.session_state.transcript, height=100)

if st.session_state.translated:
    st.markdown(f"### ✅ {output_lang} (Translated Output):")
    st.text_area("Output", st.session_state.translated, height=120)













