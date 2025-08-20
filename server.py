from flask import Flask, request
from flask_socketio import SocketIO, emit
import eventlet

eventlet.monkey_patch()

app = Flask(__name__)
socketio = SocketIO(app, cors_allowed_origins="*", logger=True, engineio_logger=True)

broadcaster_sid = None

@socketio.on("broadcaster")
def handle_broadcaster():
    global broadcaster_sid
    broadcaster_sid = request.sid
    print("✅ Broadcaster connected:", broadcaster_sid)
    emit("broadcaster-ready", {"ok": True}, to=broadcaster_sid)

@socketio.on("watcher")
def handle_watcher():
    if broadcaster_sid:
        print("👀 Watcher joined:", request.sid, "→ notifying broadcaster")
        emit("watcher", request.sid, room=broadcaster_sid)
    else:
        print("⚠️ Watcher joined but no broadcaster yet:", request.sid)

@socketio.on("offer")
def handle_offer(data):
    watcher_id = data["id"]
    offer = data["offer"]
    print("📤 Offer from broadcaster → watcher:", watcher_id)
    emit("offer", {"id": request.sid, "offer": offer}, room=watcher_id)

@socketio.on("answer")
def handle_answer(data):
    print("📥 Answer from watcher → broadcaster:", data["id"])
    emit("answer", {"id": request.sid, "answer": data["answer"]}, room=data["id"])

@socketio.on("candidate")
def handle_candidate(data):
    target = data["id"]
    print("🧊 ICE candidate relayed to:", target)
    emit("candidate", {"id": request.sid, "candidate": data["candidate"]}, room=target)

@socketio.on("disconnect")
def handle_disconnect():
    global broadcaster_sid
    print("🔌 Disconnect:", request.sid)
    if request.sid == broadcaster_sid:
        print("❌ Broadcaster disconnected")
        broadcaster_sid = None
    else:
        emit("disconnectPeer", request.sid, room=broadcaster_sid)

@app.route("/")
def index():
    return "WebRTC signaling server OK"

if __name__ == "__main__":
    # eventlet is installed, so this will use the eventlet web server
    socketio.run(app, host="0.0.0.0", port=5000)