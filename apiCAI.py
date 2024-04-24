# catches
from characterai import PyCAI
import os
import tempthing

client = PyCAI(os.getenv("CHARACTERAI_TOKEN"))

char = "UNIA7ldJdQ3xxNQD6hGDBmuBJcr1gCyIK-xliu5C0gM"

chat = client.chat.get_chat(char)

participants = chat["participants"]

if not participants[0]["is_human"]:
    tgt = participants[0]["user"]["username"]
else:
    tgt = participants[1]["user"]["username"]


def send_message(message):
    chat = client.chat.get_chat(char)

    data = client.chat.send_message(chat["external_id"], tgt, message)

    text = data["replies"][0]["text"]

    return text


def new_chat():
    client.chat.new_chat(char)
    send_message(tempthing.initprompt)


# catches
