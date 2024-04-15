import socketio
import eventlet

from transformers import pipeline
from apiCAI import send_message, new_chat
from llm import send_message as LLMmessage, reset as LLMreset

# create the Socket.IO server
sio = socketio.Server()
app = socketio.WSGIApp(sio)

@sio.event
def imgcaption(sid, data):
    image_to_text = pipeline("image-to-text", model="nlpconnect/vit-gpt2-image-captioning")
    caption = image_to_text(data)
    return caption, 200

@sio.event
def chat(sid, data):
    if data['usellm'] == True:
        return LLMmessage(data['message']), 200
    else:     
        return send_message(data['message']), 200

@sio.event
def newchat(sid, data):
    LLMreset()
    return new_chat(), 200

@sio.event
def connect(sid, environ, auth):
    print('connect ', sid)

@sio.event
def disconnect(sid):
    print('disconnect ', sid)

if __name__ == '__main__':
    eventlet.wsgi.server(eventlet.listen(('', 6000)), app)
