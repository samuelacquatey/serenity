from fastapi import FastAPI, File, UploadFile
from fastapi.responses import FileResponse
import speech_recognition as sr
import pyttsx3
import google.generativeai as genai
from google.oauth2.credentials import Credentials
import os

app = FastAPI()

# Initialize speech recognizer and text-to-speech engine
recognizer = sr.Recognizer()
tts_engine = pyttsx3.init()

# Load Google API credentials
if os.path.exists("token.json"):
    creds = Credentials.from_authorized_user_file("token.json")
    genai.configure(credentials=creds)
else:
    raise Exception("Token file not found. Run authentication process first.")

# Load AI Model
model = genai.GenerativeModel('tunedModels/dovey-s2inbseyenwz')

# Function to convert text to speech
def speak(text):
    tts_engine.save_to_file(text, "response.mp3")
    tts_engine.runAndWait()

@app.post("/chat/audio")
async def chat_audio(file: UploadFile = File(...)):
    try:
        # Save audio file
        audio_path = f"audio/{file.filename}"
        with open(audio_path, "wb") as audio_file:
            audio_file.write(file.file.read())

        # Convert speech to text
        with sr.AudioFile(audio_path) as source:
            audio_data = recognizer.record(source)
            user_text = recognizer.recognize_google(audio_data)
        
        print(f"User: {user_text}")

        # Generate AI response
        response = model.generate_content(user_text)
        ai_response = response.text

        # Convert AI response to speech
        speak(ai_response)

        return {"response": ai_response, "audio_url": "/audio/response.mp3"}
    except Exception as e:
        return {"error": str(e)}

@app.get("/audio/response.mp3")
async def get_audio():
    return FileResponse("response.mp3", media_type="audio/mpeg")
