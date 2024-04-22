# based on the chat example from textgen docs
# i actually tested this
# i forced myself to listen to lhugueny on loop while coding this so i can be more grateful for coding in silence

import requests

url = "http://127.0.0.1:5000/v1/chat/completions"

headers = {"Content-Type": "application/json"}

history = []


def send_message(message: str, character: str = "Assistant"):
    history.append({"role": "user", "content": message})
    data = {"mode": "chat", "character": character, "messages": history}
    response = requests.post(
        url, headers=headers, json=data, verify=False  # DevSkim: ignore DS126186
    )
    ai_response = response.json()["choices"][0]["message"]["content"]
    history.append({"role": "assistant", "content": ai_response})
    return ai_response


def reset_history():
    history.clear()
