import google.generativeai as genai

# Use API key authentication (NOT OAuth)
genai.configure(api_key="AIzaSyBkeBW6aWXlVDuFA43MFZ3V1MnqAAzSch0")  # Replace with your actual API key

# Load the fine-tuned model
model = genai.GenerativeModel("tunedModels/dovey-s2inbseyenwz")

# Generate response
response = model.generate_content("I feel really anxious about my future.")
print(response.text)
