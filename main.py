import socketio
import eventlet
import psutil
import spongelang

from transformers import pipeline
from apiCAI import send_message, new_chat
from llm import send_message as LLMmessage, reset as LLMreset

# create the Socket.IO server
sio = socketio.Server()
app = socketio.WSGIApp(sio)


@sio.event
def imgcaption(sid, data):
    if (
        psutil.virtual_memory().available / 1048576 < 2000
    ):  # check if available ram is less than 2gb (2GB != 2048MB btw 2GiB == 2048MiB GB != GiB MB != MiB you're just an idiot)
        print("THERE'S LESS THAN 2GB RAM HELP")
        return "", 200
    image_to_text = pipeline(
        "image-to-text", model="nlpconnect/vit-gpt2-image-captioning"
    )
    caption = image_to_text(data)
    return caption, 200


@sio.event
def chat(sid, data):
    if data["usellm"] == True:
        return LLMmessage(data["message"]), 200
    else:
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
    LLMreset()
    return new_chat(), 200


@sio.event
def connect(sid, environ, auth):
    print("connect", sid)


@sio.event
def disconnect(sid):
    print("disconnect", sid)


if __name__ == "__main__":
    eventlet.wsgi.server(eventlet.listen(("", 6000)), app)
