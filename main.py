from google_auth_oauthlib.flow import InstalledAppFlow
import google.generativeai as genai

flow = InstalledAppFlow.from_client_secrets_file(
    'C:/Users/LENOVO/Desktop/dovey/system/client_secret.json',
    scopes = [
    "https://www.googleapis.com/auth/cloud-platform",
    "https://www.googleapis.com/auth/generative-language.tuning"
    ]
)
credentials = flow.run_local_server(port=0)

# Configure genai with OAuth credentials
genai.configure(credentials=credentials)

# Now you can use your fine-tuned model
model = genai.GenerativeModel('tunedModels/dovey-s2inbseyenwz')
response = model.generate_content("i feel really anxious about my future")
print(response.text)
