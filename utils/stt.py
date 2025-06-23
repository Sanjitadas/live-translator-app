# utils/stt.py
import speech_recognition as sr # type: ignore

recognizer = sr.Recognizer()

def record_and_transcribe_async():
    return "Recording... (click Stop when finished)"

def stop_and_transcribe(lang_code="en"):
    with sr.Microphone() as source:
        audio_data = recognizer.listen(source, phrase_time_limit=10)
        try:
            transcript = recognizer.recognize_google(audio_data, language=lang_code)
            return transcript
        except sr.UnknownValueError:
            return "Sorry, could not understand."
        except sr.RequestError:
            return "Speech recognition service is unavailable."









