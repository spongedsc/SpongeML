import socketio
import eventlet
import psutil
import spongelang

from transformers import pipeline
from apiCAI import send_message, new_chat

# create the Socket.IO server
sio = socketio.Server()
app = socketio.WSGIApp(sio)


@sio.event
def imgcaption(sid, data):
    if psutil.virtual_memory().available / 1048576 < 3000:
        print("Image Recognition Skipped due to low memory")
        return "", 200
    image_to_text = pipeline(
        "image-to-text", model="nlpconnect/vit-gpt2-image-captioning"
    )
    caption = image_to_text(data)
    return caption, 200


@sio.event
def chat(sid, data):
    msg = send_message(send_message(data["message"]))
    code = spongelang.extract_spongelang(msg)
    if code:
        try:
            out = spongelang.process_function_calls(code, spongelang.functions)
        except Exception as e:
            out = f"ERROR! {type(e).__name__}: {e}"
        return msg + f"\n\nSpongeLang output:\n\n```\n{out}\n```", 200
    return msg, 200


@sio.event
def newchat(sid, data):
    return new_chat(), 200


@sio.event
def connect(sid, environ, auth):
    print("connect", sid)


@sio.event
def disconnect(sid):
    print("disconnect", sid)


if __name__ == "__main__":
    eventlet.wsgi.server(eventlet.listen(("", 6000)), app)
