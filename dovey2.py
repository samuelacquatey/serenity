from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
import google.generativeai as genai
import os

SCOPES = [
    "https://www.googleapis.com/auth/cloud-platform",
    "https://www.googleapis.com/auth/generative-language.retriever"
]

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

genai.configure(credentials=load_creds())

model = genai.GenerativeModel('tunedModels/dovey-s2inbseyenwz')

user = input("Enter your name: ")
print(f"Dovey: Hi {user}, how can I help you today?")

while True:
    user_input = input("You: ")
    if user_input.lower() in ['exit', 'quit', 'bye']:
        print("Ending conversation. Goodbye!")
        break
    
    response = model.generate_content(user_input)
    print(f"AI: {response.text}")
