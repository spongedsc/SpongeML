import socketio
import eventlet
import psutil
import textgenwui
import requests
import os

from transformers import pipeline
from apiCAI import send_message, new_chat

# create the Socket.IO server
sio = socketio.Server()
app = socketio.WSGIApp(sio)


@sio.event
def imgcaption(sid, data):
    try:
        if psutil.virtual_memory().available / 1048576 < 3000:
            print("Image recognition skipped due to low memory")
            return "", 200
        image_to_text = pipeline(
            "image-to-text", model="nlpconnect/vit-gpt2-image-captioning"
        )
        caption = image_to_text(data)
        return caption, 200
    except Exception as e:
        print(f"Error occurred during image recognition: {e}")
        return "", 500


@sio.event
def chat(sid, data: dict):
    try:
        if data.get("textgenwui") == True:
            msg = textgenwui.send_message(
                data["message"],
                os.getenv("TEXTGENWUI_CHARACTER"),
            )
        else:
            msg = send_message(send_message(data["message"]))
        return msg, 200
    except Exception as e:
        print(f"Error occurred during chat: {e}")
        return "", 500


@sio.event
def imagerecognitionenabled(sid, data):
    try:
        if psutil.virtual_memory().available / 1048576 < 3000:
            return False, 200
        else:
            return True, 200
    except Exception as e:
        print(f"Error occurred during chat: {e}")
        return "", 500


@sio.event
def localgenenabled(sid, data):
    try:
        requests.get(
            os.getenv("TEXTGENWUI_ENDPOINT").split("/v1/")[0]
        )  # shitty hack that probably isnt gonna work 100% of the time
    except requests.exceptions.ConnectionError:
        return False, 200
    return True, 200


@sio.event
def newchat(sid, data):
    textgenwui.reset_history()
    return new_chat(), 200


@sio.event
def connect(sid, environ, auth):
    print("connect", sid)


@sio.event
def disconnect(sid):
    print("disconnect", sid)


if __name__ == "__main__":
    eventlet.wsgi.server(eventlet.listen(("", 6000)), app)
