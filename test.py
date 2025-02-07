import google.generativeai as genai

genai.configure(api_key="AIzaSyBkeBW6aWXlVDuFA43MFZ3V1MnqAAzSch0")

model = genai.GenerativeModel("gemini-pro")

conversation_history = []

while True:
    user_input = input("You: ")
    if user_input.lower() in ["exit", "quit"]:
        break
    conversation_history.append({"role": "user", "content": user_input})
    
    formatted_history = [{"text": message["content"]} for message in conversation_history]
    
    if "brainrot" in user_input.lower():
        formatted_history.append({"text": "Respond in brainrot style."})
    
    response = model.generate_content(formatted_history)
    
    print("Bot:", response.text)
    
    conversation_history.append({"role": "bot", "content": response.text})