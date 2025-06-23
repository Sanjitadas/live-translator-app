# utils/stt.py
import os
import sounddevice as sd
import soundfile as sf
import threading
import queue
import tempfile
import speech_recognition as sr

recording = False
audio_queue = queue.Queue()

def record_and_transcribe_async():
    global recording
    recording = True
    thread = threading.Thread(target=_record_audio)
    thread.start()
    return "Recording..."

def _record_audio():
    global recording
    samplerate = 16000
    duration = 30  # Max record time (s)
    temp_file = tempfile.NamedTemporaryFile(delete=False, suffix=".wav")
    filename = temp_file.name
    temp_file.close()

    print("Recording...")
    recording_data = sd.rec(int(duration * samplerate), samplerate=samplerate, channels=1, dtype='int16')
    sd.wait()
    print("Finished recording.")

    sf.write(filename, recording_data, samplerate)
    audio_queue.put(filename)

def stop_and_transcribe(lang_code="en-IN"):
    global recording
    recording = False
    recognizer = sr.Recognizer()

    try:
        audio_file_path = audio_queue.get(timeout=5)
    except queue.Empty:
        return "No audio captured."

    with sr.AudioFile(audio_file_path) as source:
        audio_data = recognizer.record(source)

    try:
        result = recognizer.recognize_google(audio_data, language=lang_code)
        return result
    except sr.UnknownValueError:
        return "Could not understand audio."
    except sr.RequestError:
        return "Could not request results from Google Speech Recognition service."











