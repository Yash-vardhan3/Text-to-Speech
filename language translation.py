import tkinter as tk
from tkinter import ttk
from googletrans import LANGUAGES
import speech_recognition as sr
from googletrans import Translator
from gtts import gTTS
import os
from playsound import playsound
from transformers import pipeline
import langdetect
from sklearn.metrics import accuracy_score

# Function to recognize speech using the microphone
def recognize_speech():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        print("Please speak now...")
        try:
            audio = recognizer.listen(source, timeout=5)  # Adjust timeout as needed
            text = recognizer.recognize_google(audio)
            print(f"Recognized Text: {text}")
            return text
        except sr.WaitTimeoutError:
            print("Timeout error: No speech detected within timeout period.")
            return None
        except sr.UnknownValueError:
            print("Error: Unable to recognize speech")
            return None
        except sr.RequestError as e:
            print(f"Error fetching results; {e}")
            return None

# Function to detect language
def detect_language(text):
    try:
        lang = langdetect.detect(text)
        print(f"Detected Language: {lang}")
        return lang
    except Exception as e:
        print(f"Language detection error: {e}")
        return None

# Function to translate text
def translate_text(text, src_lang='en', dest_lang='es'):
    translator = Translator()
    try:
        translated = translator.translate(text, src=src_lang, dest=dest_lang)
        print(f"Translated Text: {translated.text}")
        return translated.text
    except Exception as e:
        print(f"Translation error: {e}")
        return None

# Function to perform sentiment analysis
def analyze_sentiment(text):
    sentiment_analyzer = pipeline('sentiment-analysis')
    try:
        result = sentiment_analyzer(text)[0]
        print(f"Sentiment: {result['label']}, Score: {result['score']}")
        return result
    except Exception as e:
        print(f"Sentiment analysis error: {e}")
        return None

# Function to extract keywords
def extract_keywords(text):
    # This is a placeholder for a keyword extraction method.
    # For a real implementation, you can use libraries like spaCy or YAKE.
    keywords = text.split()[:3]  # Mock implementation: taking first 3 words as keywords
    print(f"Extracted Keywords: {keywords}")
    return keywords

# Function to speak translated text
def speak_text(text, lang='es'):
    lang_code_map = {
        'af': 'af',     # Afrikaans
        'sq': 'sq',     # Albanian
        'am': 'am',     # Amharic
        'ar': 'ar',     # Arabic
        'hy': 'hy',     # Armenian
        'az': 'az',     # Azerbaijani
        'eu': 'eu',     # Basque
        'be': 'be',     # Belarusian
        'bn': 'bn',     # Bengali
        'bs': 'bs',     # Bosnian
        'bg': 'bg',     # Bulgarian
        'ca': 'ca',     # Catalan
        'ceb': 'ceb',   # Cebuano
        'ny': 'ny',     # Chichewa
        'zh-CN': 'zh',  # Chinese (Simplified)
        'zh-TW': 'zh',  # Chinese (Traditional)
        'co': 'co',     # Corsican
        'hr': 'hr',     # Croatian
        'cs': 'cs',     # Czech
        'da': 'da',     # Danish
        'nl': 'nl',     # Dutch
        'en': 'en',     # English
        'eo': 'eo',     # Esperanto
        'et': 'et',     # Estonian
        'tl': 'tl',     # Filipino
        'fi': 'fi',     # Finnish
        'fr': 'fr',     # French
        'fy': 'fy',     # Frisian
        'gl': 'gl',     # Galician
        'ka': 'ka',     # Georgian
        'de': 'de',     # German
        'el': 'el',     # Greek
        'gu': 'gu',     # Gujarati
        'ht': 'ht',     # Haitian Creole
        'ha': 'ha',     # Hausa
        'haw': 'haw',   # Hawaiian
        'iw': 'iw',     # Hebrew
        'he': 'he',     # Hebrew (alternative code)
        'hi': 'hi',     # Hindi
        'hmn': 'hmn',   # Hmong
        'hu': 'hu',     # Hungarian
        'is': 'is',     # Icelandic
        'ig': 'ig',     # Igbo
        'id': 'id',     # Indonesian
        'ga': 'ga',     # Irish
        'it': 'it',     # Italian
        'ja': 'ja',     # Japanese
        'jv': 'jv',     # Javanese
        'kn': 'kn',     # Kannada
        'kk': 'kk',     # Kazakh
        'km': 'km',     # Khmer
        'rw': 'rw',     # Kinyarwanda
        'ko': 'ko',     # Korean
        'ku': 'ku',     # Kurdish (Kurmanji)
        'ky': 'ky',     # Kyrgyz
        'lo': 'lo',     # Lao
        'la': 'la',     # Latin
        'lv': 'lv',     # Latvian
        'lt': 'lt',     # Lithuanian
        'lb': 'lb',     # Luxembourgish
        'mk': 'mk',     # Macedonian
        'mg': 'mg',     # Malagasy
        'ms': 'ms',     # Malay
        'ml': 'ml',     # Malayalam
        'mt': 'mt',     # Maltese
        'mi': 'mi',     # Maori
        'mr': 'mr',     # Marathi
        'mn': 'mn',     # Mongolian
        'my': 'my',     # Myanmar (Burmese)
        'ne': 'ne',     # Nepali
        'no': 'no',     # Norwegian
        'or': 'or',     # Odia (Oriya)
        'ps': 'ps',     # Pashto
        'fa': 'fa',     # Persian
        'pl': 'pl',     # Polish
        'pt': 'pt',     # Portuguese
        'pa': 'pa',     # Punjabi
        'ro': 'ro',     # Romanian
        'ru': 'ru',     # Russian
        'sm': 'sm',     # Samoan
        'gd': 'gd',     # Scots Gaelic
        'sr': 'sr',     # Serbian
        'sn': 'sn',     # Shona
        'sd': 'sd',     # Sindhi
        'si': 'si',     # Sinhala
        'sk': 'sk',     # Slovak
        'sl': 'sl',     # Slovenian
        'so': 'so',     # Somali
        'st': 'st',     # Southern Sotho
        'es': 'es',     # Spanish
        'su': 'su',     # Sundanese
        'sw': 'sw',     # Swahili
        'sv': 'sv',     # Swedish
        'tg': 'tg',     # Tajik
        'ta': 'ta',     # Tamil
        'tt': 'tt',     # Tatar
        'te': 'te',     # Telugu
        'th': 'th',     # Thai
        'tr': 'tr',     # Turkish
        'tk': 'tk',     # Turkmen
        'uk': 'uk',     # Ukrainian
        'ur': 'ur',     # Urdu
        'ug': 'ug',     # Uyghur
        'uz': 'uz',     # Uzbek
        'vi': 'vi',     # Vietnamese
        'cy': 'cy',     # Welsh
        'xh': 'xh',     # Xhosa
        'yi': 'yi',     # Yiddish
        'yo': 'yo',     # Yoruba
        'zu': 'zu'      # Zulu
    }
    
    lang_code = lang_code_map.get(lang, 'en')
    
    try:
        tts = gTTS(text=text, lang=lang_code)
        filename = "translated_audio.mp3"
        tts.save(filename)
        playsound(filename)
        os.remove(filename)
    except Exception as e:
        print(f"Text-to-speech error: {e}")

# Function to handle real-time translation process
def real_time_translation(src_lang_var, dest_lang_var):
    src_lang = src_lang_var.get()
    dest_lang = dest_lang_var.get()

    recognized_text = recognize_speech()
    if not recognized_text:
        output_text.delete(1.0, tk.END)
        output_text.insert(tk.END, "Error: Failed to recognize speech.")
        return

    detected_lang = detect_language(recognized_text)
    if detected_lang:
        output_text.delete(1.0, tk.END)
        output_text.insert(tk.END, f"Detected Language: {detected_lang}\n\n")
    else:
        output_text.delete(1.0, tk.END)
        output_text.insert(tk.END, "Error: Failed to detect language.")
        return

    sentiment = analyze_sentiment(recognized_text)
    if sentiment:
        output_text.insert(tk.END, f"Sentiment: {sentiment['label']} (Score: {sentiment['score']})\n\n")
    else:
        output_text.insert(tk.END, "Error: Failed to perform sentiment analysis.")
        return

    keywords = extract_keywords(recognized_text)
    output_text.insert(tk.END, f"Keywords: {', '.join(keywords)}\n\n")

    translated_text = translate_text(recognized_text, src_lang, dest_lang)
    if not translated_text:
        output_text.insert(tk.END, "Error: Failed to translate text.")
        return

    output_text.insert(tk.END, f"Translated Text: {translated_text}\n\n")

    speak_text(translated_text, lang=dest_lang)

# Create Tkinter window
root = tk.Tk()
root.title("Real-Time Language Translation")

# Language selection labels and dropdowns
src_lang_label = ttk.Label(root, text="Source Language:")
src_lang_label.grid(row=0, column=0, padx=10, pady=10)

src_lang_var = tk.StringVar()
src_lang_dropdown = ttk.Combobox(root, textvariable=src_lang_var, values=list(LANGUAGES.values()), state="readonly")
src_lang_dropdown.grid(row=0, column=1, padx=10, pady=10)
src_lang_dropdown.current(0)  # Set default value

dest_lang_label = ttk.Label(root, text="Destination Language:")
dest_lang_label.grid(row=1, column=0, padx=10, pady=10)

dest_lang_var = tk.StringVar()
dest_lang_dropdown = ttk.Combobox(root, textvariable=dest_lang_var, values=list(LANGUAGES.values()), state="readonly")
dest_lang_dropdown.grid(row=1, column=1, padx=10, pady=10)
dest_lang_dropdown.current(1)  # Set default value

# Input and output text boxes
input_text_label = ttk.Label(root, text="Input:")
input_text_label.grid(row=2, column=0, padx=10, pady=10)

input_text = tk.Entry(root, width=50)
input_text.grid(row=2, column=1, padx=10, pady=10)

output_text_label = ttk.Label(root, text="Translated Output:")
output_text_label.grid(row=3, column=0, padx=10, pady=10)

output_text = tk.Text(root, height=10, width=50)
output_text.grid(row=3, column=1, padx=10, pady=10)

# Translate button
translate_btn = ttk.Button(root, text="Translate", command=lambda: real_time_translation(src_lang_var, dest_lang_var))
translate_btn.grid(row=4, columnspan=2, padx=10, pady=10)

# Run the Tkinter event loop
root.mainloop()
