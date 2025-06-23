# utils/stt.py
import speech_recognition as sr

def transcribe_wav_file(file, lang_code="en-IN"):
    recognizer = sr.Recognizer()
    with sr.AudioFile(file) as source:
        audio_data = recognizer.record(source)
    try:
        return recognizer.recognize_google(audio_data, language=lang_code)
    except sr.UnknownValueError:
        return "Could not understand the audio."
    except sr.RequestError as e:
        return f"Google STT error: {e}"















