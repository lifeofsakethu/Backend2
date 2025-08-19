from flask import Flask
from flask_socketio import SocketIO, emit

app = Flask(__name__)
socketio = SocketIO(app, cors_allowed_origins="*")

# Relay WebRTC "offer" (SDP) to other peers
@socketio.on("offer")
def handle_offer(data):
    emit("offer", data, broadcast=True, include_self=False)

# Relay "answer" (SDP) to other peers
@socketio.on("answer")
def handle_answer(data):
    emit("answer", data, broadcast=True, include_self=False)

# Relay ICE candidates
@socketio.on("candidate")
def handle_candidate(data):
    emit("candidate", data, broadcast=True, include_self=False)

@app.route("/")
def index():
    return "✅ WebRTC Signaling Server Running"

if __name__ == "__main__":
    socketio.run(app, host="0.0.0.0", port=5000)
