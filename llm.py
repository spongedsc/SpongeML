from litellm import completion
import os

starthistory = []

history = starthistory

def send_message(message):
    global history
    history.append({"content": message,"role":"user"})
    response = completion(
            model="ollama/SpongeAss", 
            messages = history, 
            api_base=os.getenv("OLLAMA_URL"),
)

    history.append({ "content": response['choices'][0]['message']['content'], "role": "assistant" })
    
    return response['choices'][0]['message']['content']

def reset():
    global history
    history = starthistory