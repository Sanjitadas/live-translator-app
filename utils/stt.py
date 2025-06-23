# utils/stt.py

import os
import speech_recognition as sr

TEMP_FILE = "output/temp_live.wav"

def record_and_transcribe_async():
    return "Recording not supported in Streamlit Cloud. Please upload a WAV file."

def stop_and_transcribe(lang_code="en"):
    recognizer = sr.Recognizer()

    if not os.path.exists(TEMP_FILE):
        return "No audio file found."

    with sr.AudioFile(TEMP_FILE) as source:
        audio_data = recognizer.record(source)
        try:
            text = recognizer.recognize_google(audio_data, language=lang_code)
            return text
        except sr.UnknownValueError:
            return "Sorry, I couldn't understand the audio."
        except sr.RequestError:
            return "Speech Recognition service error."














