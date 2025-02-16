import customtkinter as ctk
import speech_recognition as sr
import pyttsx3
from googletrans import Translator, LANGUAGES

#  Initialize Translator and Speech Engine
translator = Translator()
speech_engine = pyttsx3.init()

#  Convert Speech to Text
def recognize_speech():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        status_label.configure(text=" Listening...")
        app.update()
        
        try:
            audio = recognizer.listen(source, timeout=10)
            recognized_text = recognizer.recognize_google(audio)
            input_box.delete("1.0", "end")  
            input_box.insert("end", recognized_text)
            status_label.configure(text=" Voice Captured!")
        except sr.UnknownValueError:
            status_label.configure(text=" Couldn't recognize speech. Try again!")
        except sr.RequestError:
            status_label.configure(text=" Speech service unavailable.")

#  Translate Text
def translate_text():
    original_text = input_box.get("1.0", "end").strip()
    from_lang = language_codes[source_language.get()]
    to_lang = language_codes[target_language.get()]

    if original_text:
        translated = translator.translate(original_text, src=from_lang, dest=to_lang)
        output_box.configure(state="normal")
        output_box.delete("1.0", "end")
        output_box.insert("end", translated.text)
        output_box.configure(state="disabled")
        speak_text(translated.text)  #  Speak the translated text

#  Speak Translated Text
def speak_text(text):
    speech_engine.say(text)
    speech_engine.runAndWait()

#  Clear Text Fields
def clear_text():
    input_box.delete("1.0", "end")
    output_box.configure(state="normal")
    output_box.delete("1.0", "end")
    output_box.configure(state="disabled")

# UI Setup
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

#  Main Application Window
app = ctk.CTk()
app.title(" AI Voice Translator")
app.geometry("650x550")

#  Language Dictionary
language_codes = {LANGUAGES[code].capitalize(): code for code in LANGUAGES}

#  Title Label
title_label = ctk.CTkLabel(app, text=" AI Voice Translator", font=("Arial", 25, "bold"))
title_label.pack(pady=10)

#  Language Selection Frame
language_frame = ctk.CTkFrame(app)
language_frame.pack(pady=10, padx=10)

source_label = ctk.CTkLabel(language_frame, text="From:", font=("Arial", 14))
source_label.grid(row=0, column=0, padx=10, pady=5, sticky="e")

source_language = ctk.CTkComboBox(language_frame, values=list(language_codes.keys()), width=200)
source_language.grid(row=0, column=1, padx=10, pady=5)
source_language.set("English")

target_label = ctk.CTkLabel(language_frame, text="To:", font=("Arial", 14))
target_label.grid(row=0, column=2, padx=10, pady=5, sticky="w")

target_language = ctk.CTkComboBox(language_frame, values=list(language_codes.keys()), width=200)
target_language.grid(row=0, column=3, padx=10, pady=5)
target_language.set("Hindi")

#  Input Text Box
input_label = ctk.CTkLabel(app, text="Enter or Speak Text:")
input_label.pack(pady=5)
input_box = ctk.CTkTextbox(app, height=100, width=500)
input_box.pack(pady=5)

# Buttons
button_frame = ctk.CTkFrame(app)
button_frame.pack(pady=10)

translate_btn = ctk.CTkButton(button_frame, text=" Translate", command=translate_text, width=120)
translate_btn.grid(row=0, column=0, padx=10)

clear_btn = ctk.CTkButton(button_frame, text=" Clear", command=clear_text, width=120)
clear_btn.grid(row=0, column=1, padx=10)

voice_btn = ctk.CTkButton(button_frame, text=" Speak", command=recognize_speech, width=120)
voice_btn.grid(row=0, column=2, padx=10)

# Output Text Box
output_label = ctk.CTkLabel(app, text="Translated Text:")
output_label.pack(pady=5)
output_box = ctk.CTkTextbox(app, height=100, width=500, state="disabled")
output_box.pack(pady=5)

# Speech Status Label
status_label = ctk.CTkLabel(app, text="", font=("Arial", 12))
status_label.pack(pady=5)

# Run Application
app.mainloop()
