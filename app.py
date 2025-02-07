from flask import Flask, request, jsonify
import speech_recognition as sr
import pyttsx3
from google_auth_oauthlib.flow import InstalledAppFlow
from google.oauth2.credentials import Credentials
import google.generativeai as genai
import os

app = Flask(__name__)

# Initialize the recognizer and text-to-speech engine
recognizer = sr.Recognizer()
tts_engine = pyttsx3.init()

def speak(text):
    tts_engine.say(text)
    tts_engine.runAndWait()

def listen():
    with sr.Microphone() as source:
        print("Listening...")
        audio = recognizer.listen(source)
        try:
            return recognizer.recognize_google(audio)
        except sr.UnknownValueError:
            return "Sorry, I did not understand that."
        except sr.RequestError:
            return "Sorry, my speech service is down."

# Step 1: Initialize the OAuth flow and get credentials
flow = InstalledAppFlow.from_client_secrets_file(
    'C:/Users/LENOVO/Desktop/dovey/system/client_secret.json',  # Customize this path
    scopes=[
        "https://www.googleapis.com/auth/cloud-platform",
        "https://www.googleapis.com/auth/generative-language.tuning"
    ]
)
creds = flow.run_local_server(port=0)
with open('token.json', 'w') as token:
    token.write(creds.to_json())

genai.configure(credentials=creds)

model = genai.GenerativeModel('tunedModels/dovey-s2inbseyenwz')

@app.route("/api/speech-to-text", methods=["POST"])
def speech_to_text():
    user_input = listen()
    if user_input.lower() in ['exit', 'quit', 'bye']:
        response_text = "Ending conversation. Goodbye!"
    else:
        response = model.generate_content(user_input)
        response_text = response.text
    speak(response_text)
    return jsonify({"response": response_text})

if __name__ == "__main__":
    app.run(debug=True)