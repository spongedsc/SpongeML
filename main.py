# keep in mind i have no idea how python works
import socketio
import eventlet
from transformers import pipeline

# create a Socket.IO server
sio = socketio.Server()
app = socketio.WSGIApp(sio)

@sio.event
def imgcaption(sid, data):
    image_to_text = pipeline("image-to-text", model="nlpconnect/vit-gpt2-image-captioning")
    caption = image_to_text(data)
    return caption, 200

@sio.event
def connect(sid, environ, auth):
    print('connect ', sid)

@sio.event
def disconnect(sid):
    print('disconnect ', sid)

if __name__ == '__main__':
    eventlet.wsgi.server(eventlet.listen(('', 6000)), app)