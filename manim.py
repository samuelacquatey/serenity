import google.generativeai as genai

genai.configure(api_key="AIzaSyBkeBW6aWXlVDuFA43MFZ3V1MnqAAzSch0")

model = genai.GenerativeModel("gemini-2.0-flash")

conversation_history = []

while True:
    user_input = input("You: ")
    if user_input.lower() in ["exit", "quit"]:
        break
    conversation_history.append({"role": "user", "content": user_input})
    
    formatted_history = [{"text": message["content"]} for message in conversation_history]
    
    response = model.generate_content(formatted_history)
    print("Bot:", response.text)
    
    conversation_history.append({"role": "bot", "content": response.text})
    
    if "generate a manim script" in user_input.lower():
        manim_request = "Generate a Manim script to explain the following concept: " + user_input
        conversation_history.append({"role": "user", "content": manim_request})
        
        formatted_history = [{"text": message["content"]} for message in conversation_history]
        
        manim_response = model.generate_content(formatted_history)
        print("Manim Script:", manim_response.text)
        
        conversation_history.append({"role": "bot", "content": manim_response.text})