# utils/tts.py

from gtts import gTTS
import os
from tempfile import NamedTemporaryFile
from playsound import playsound

def speak_text(text: str):
    try:
        tts = gTTS(text=text, lang='en')
        with NamedTemporaryFile(delete=False, suffix=".mp3") as fp:
            temp_path = fp.name
            tts.save(temp_path)
        playsound(temp_path)
        os.remove(temp_path)
    except Exception as e:
        print("TTS error:", e)






