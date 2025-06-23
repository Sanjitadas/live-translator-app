import streamlit as st
from utils.stt import transcribe_wav_file
from utils.tts import speak_text
from utils.ai_translator import ai_translate_with_dialects

st.set_page_config(page_title="🎙️ Live Multilingual Translator", layout="centered")

st.markdown("<h2 style='text-align: center;'>🎙️ Live Multilingual Translator</h2>", unsafe_allow_html=True)

languages = {
    "Indian English": "en-IN",
    "US English": "en",
    "Hindi": "hi",
    "Spanish": "es"
}

col1, col2 = st.columns(2)
with col1:
    input_lang_name = st.selectbox("🎯 Input Language", list(languages.keys()), index=0)
with col2:
    output_lang_name = st.selectbox("🌍 Output Language", list(languages.keys()), index=1)

input_lang = languages[input_lang_name]
output_lang = languages[output_lang_name]

mode = st.radio("🔁 Choose Mode", [
    "TTT (Text-to-Text)",
    "STT (Speech-to-Text)",
    "TTS (Text-to-Speech)",
    "STS (Speech-to-Speech)"
])

text_input = st.text_area("✍️ Type or Speak:", placeholder="You can type or record, then click Translate")

# 🎤 Upload WAV file
uploaded_file = st.file_uploader("🎤 Upload a WAV audio file for transcription", type=["wav"])

if uploaded_file is not None and mode in ["STT (Speech-to-Text)", "STS (Speech-to-Speech)"]:
    transcript = transcribe_wav_file(uploaded_file, lang_code=input_lang)
    st.success(f"🗣️ Transcribed:\n\n{transcript}")
    st.session_state["transcript"] = transcript
else:
    transcript = text_input

# 🌐 Translate
if st.button("🌐 Translate"):
    if not transcript.strip():
        st.warning("Please provide input text or audio.")
    else:
        translated_text = ai_translate_with_dialects(transcript, input_lang_name, output_lang_name)
        st.success(f"📝 Translated:\n\n{translated_text}")

        with open("output/output.txt", "w", encoding="utf-8") as f:
            f.write(translated_text)

        # STS or TTS
        if mode in ["TTS (Text-to-Speech)", "STS (Speech-to-Speech)"]:
            speak_text(translated_text, lang=output_lang)





















