from google_auth_oauthlib.flow import InstalledAppFlow
import google.generativeai as genai

# Step 1: Initialize the OAuth flow and get credentials
flow = InstalledAppFlow.from_client_secrets_file(
    'C:/Users/LENOVO/Desktop/dovey/system/client_secret.json',
    scopes=[
        "https://www.googleapis.com/auth/cloud-platform",
        "https://www.googleapis.com/auth/generative-language.tuning"
    ]
)
credentials = flow.run_local_server(port=0)

# Step 2: Configure genai with OAuth credentials
genai.configure(credentials=credentials)

print("Authorization successful. You can now start the conversation.")

# Now you can use your fine-tuned model
model = genai.GenerativeModel('tunedModels/dovey-s2inbseyenwz')

# Step 3: Set up a loop to continuously prompt the user for input
while True:
    user_input = input("You: ")
    
    if user_input.lower() in ['exit', 'quit', 'bye']:
        print("Ending the conversation. Goodbye!")
        break
    
    # Step 4: Process the user's input and generate a response
    response = model.generate_content(prompt=user_input)
    
    # Step 5: Print the response
    print(f"AI: {response['text']}")