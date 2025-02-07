import os
import speech_recognition as sr
import google.cloud.speech as speech
from google.cloud import texttospeech
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
import google.generativeai as genai
import simpleaudio as sa

# Set up Google Cloud Clients
speech_client = speech.SpeechClient()
tts_client = texttospeech.TextToSpeechClient()

# Initialize speech recognizer
recognizer = sr.Recognizer()

# OAuth 2.0 authentication
SCOPES = ["https://www.googleapis.com/auth/cloud-platform"]

def load_creds():
    creds = None
    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json', SCOPES)
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'C:/Users/LENOVO/Desktop/dovey/system/client_secret.json',
                SCOPES
            )
            creds = flow.run_local_server(port=0)
        with open('token.json', 'w') as token:
            token.write(creds.to_json())
    return creds

# Load credentials for API requests
creds = load_creds()

# Initialize Generative AI Model
genai.configure(api_key=creds.token)
model = genai.GenerativeModel('tunedModels/dovey-s2inbseyenwz')

# Speech-to-Text (STT) Function
def listen():
    with sr.Microphone() as source:
        print("Listening...")
        recognizer.adjust_for_ambient_noise(source)
        audio = recognizer.listen(source)
    
    try:
        response = speech_client.recognize(
            config=speech.RecognitionConfig(
                encoding=speech.RecognitionConfig.AudioEncoding.LINEAR16,
                language_code="en-US"
            ),
            audio=speech.RecognitionAudio(content=audio.get_wav_data())
        )

        if response.results:
            return response.results[0].alternatives[0].transcript
        else:
            return "Sorry, I didn't catch that."
    
    except Exception as e:
        print("Error:", e)
        return "Error processing audio"

# Text-to-Speech (TTS) Function using simpleaudio
def speak(text):
    synthesis_input = texttospeech.SynthesisInput(text=text)
    voice = texttospeech.VoiceSelectionParams(
        language_code="en-US",
        ssml_gender=texttospeech.SsmlVoiceGender.NEUTRAL
    )
    audio_config = texttospeech.AudioConfig(
        audio_encoding=texttospeech.AudioEncoding.LINEAR16  # WAV format
    )

    response = tts_client.synthesize_speech(
        input=synthesis_input, voice=voice, audio_config=audio_config
    )

    # Play audio directly with simpleaudio
    wave_obj = sa.WaveObject(response.audio_content, num_channels=1, bytes_per_sample=2, sample_rate=24000)
    play_obj = wave_obj.play()
    play_obj.wait_done()

# Main Chatbot Loop
user = input("Enter your name: ")
print(f"Dovey: Hi {user}, how can I help you today?")
speak(f"Hi {user}, how can I help you today?")

while True:
    print("Waiting for user input...")
    user_input = listen()
    print(f"You: {user_input}")

    if user_input.lower() in ['exit', 'quit', 'bye']:
        print("Ending conversation. Goodbye!")
        speak("Ending conversation. Goodbye!")
        break
    
    # Generate AI response using Google Generative AI model
    print("Generating AI response...")
    ai_response = model.generate_content(user_input)
    response_text = ai_response.text if hasattr(ai_response, "text") else "I couldn't generate a response."

    print(f"AI: {response_text}")
    speak(response_text)