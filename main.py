import tkinter as tk
from tkinter import ttk
import speech_recognition as sr
import pyttsx3

class SpeechConverterApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Speech Converter")


        self.root.configure(bg='#A5D1F3')

        self.root.geometry("600x500")

        self.label = ttk.Label(root, text="Enter text or use microphone:")
        self.label.pack(pady=10)

        self.text_entry = ttk.Entry(root, width=30)
        self.text_entry.pack(pady=10)

        self.language_label = ttk.Label(root, text="Select language:")
        self.language_label.pack(pady=5)

        # Language options
        self.language_options = [
            "English ('en')", "Hindi ('hi')", "Bengali ('bn')", "Telugu ('te')", "Marathi ('mr')",
            "Tamil ('ta')", "Urdu ('ur')", "Gujarati ('gu')", "Malayalam ('ml')",
            "Kannada ('kn')", "Oriya ('or')", "Punjabi ('pa')"
        ]

        self.selected_language = tk.StringVar(value=self.language_options[0])

        self.language_menu = ttk.Combobox(root, values=self.language_options, textvariable=self.selected_language)
        self.language_menu.pack(pady=5)

        self.result_label = ttk.Label(root, text="")
        self.result_label.pack(pady=10)

        # Increase button size and set a background color
        button_style = ttk.Style()
        button_style.configure('TButton', font=('Helvetica', 12), background='#606060', foreground='#6194BC')

        self.text_to_speech_button = ttk.Button(root, text="Text to Speech", command=self.text_to_speech, style='TButton')
        self.text_to_speech_button.pack(pady=12)

        self.speech_to_text_button = ttk.Button(root, text="Speech to Text", command=self.speech_to_text, style='TButton')
        self.speech_to_text_button.pack(pady=12)

    def text_to_speech(self):
        text = self.text_entry.get()
        language_code = self.get_selected_language_code()

        if text and language_code:
            engine = pyttsx3.init()
            engine.setProperty('rate', 150)  # Speed of speech
            engine.setProperty('voice', language_code)
            engine.say(text)
            engine.save_to_file(text, 'output.mp3')
            engine.runAndWait()
            self.result_label.config(text="Text to Speech conversion successful.")
        else:
            self.result_label.config(text="Please enter text and select a language before converting.")

    def speech_to_text(self):
        language_code = self.get_selected_language_code()

        with sr.Microphone() as source:
            print("Listening...")
            audio = sr.Recognizer().listen(source)

        try:
            text = sr.Recognizer().recognize_google(audio, language=language_code)
            self.result_label.config(text=f"You said: {text}")
            self.text_entry.delete(0, tk.END)
            self.text_entry.insert(0, text)
        except sr.UnknownValueError:
            self.result_label.config(text="Could not understand audio.")
        except sr.RequestError as e:
            self.result_label.config(text=f"Error with the speech recognition service; {e}")

    def get_selected_language_code(self):
        selected_option = self.selected_language.get()
        # Extract language code from the selected option
        language_code = selected_option.split("('")[1].split("')")[0]
        return language_code

if __name__ == "__main__":
    root = tk.Tk()
    app = SpeechConverterApp(root)
    root.mainloop()