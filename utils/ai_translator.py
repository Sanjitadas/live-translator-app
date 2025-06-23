# utils/ai_translator.py
import cohere
import os
from dotenv import load_dotenv

load_dotenv()
COHERE_API_KEY = os.getenv("COHERE_API_KEY")
co = cohere.Client(COHERE_API_KEY)

def ai_translate_with_dialects(text, input_lang, output_lang):
    if not text.strip():
        return ""

    prompt = f"""You are a professional translator. Convert the following text from {input_lang} to fluent and grammatically correct {output_lang}. 
Ensure the translation is natural and easy to understand in American context. 
Original: {text}
Translated:"""

    try:
        response = co.generate(
            model="command-r-plus",
            prompt=prompt,
            max_tokens=200,
            temperature=0.5
        )
        return response.generations[0].text.strip()
    except Exception as e:
        return f"Translation error: {e}"













    for indian, us in replacements.items():
        text = text.replace(indian, us)
    return text
