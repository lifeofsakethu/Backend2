from flask import Flask
from flask_socketio import SocketIO, emit, join_room, leave_room
import eventlet

eventlet.monkey_patch()

app = Flask(__name__)
socketio = SocketIO(app, cors_allowed_origins="*")

broadcaster_sid = None

@socketio.on("broadcaster")
def handle_broadcaster():
    global broadcaster_sid
    broadcaster_sid = request.sid
    print("Broadcaster connected:", broadcaster_sid)

@socketio.on("watcher")
def handle_watcher():
    if broadcaster_sid:
        emit("watcher", request.sid, room=broadcaster_sid)

@socketio.on("offer")
def handle_offer(data):
    watcher_id = data["id"]
    offer = data["offer"]
    emit("offer", {"id": request.sid, "offer": offer}, room=watcher_id)

@socketio.on("answer")
def handle_answer(data):
    emit("answer", {"id": request.sid, "answer": data["answer"]}, room=data["id"])

@socketio.on("candidate")
def handle_candidate(data):
    emit("candidate", {"id": request.sid, "candidate": data["candidate"]}, room=data["id"])

@socketio.on("disconnect")
def handle_disconnect():
    global broadcaster_sid
    if request.sid == broadcaster_sid:
        broadcaster_sid = None
    else:
        emit("disconnectPeer", request.sid, room=broadcaster_sid)

if __name__ == "__main__":
    socketio.run(app, host="0.0.0.0", port=5000)