import os
import eventlet
eventlet.monkey_patch()

from flask import Flask, render_template, request, make_response
from flask_socketio import SocketIO, send, emit, join_room, leave_room

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'
socketio = SocketIO(app, async_mode='eventlet')

pages = {
    'cat': 'goobie snoobert',
    'chat': 'chat',
}

@app.route('/')
def home():
    return render_template('home.html', pages=pages)

@app.route('/gallery')
@app.route('/cat')
def gallery():
    image_folder = os.path.join(app.static_folder, 'images')
    image_list = [f for f in os.listdir(image_folder) if f.lower().endswith(('.png', '.jpg', '.jpeg', '.gif', '.webp'))]
    return render_template('gallery.html', images=image_list)

@app.route('/about')
def about():
    return "<h2>This is the About page.</h2>"

@app.route('/howdyougethere?')
def howdyougethere():
    return "<h2>giggle</h2>"

@app.route('/chat')
def chat():
    username = request.cookies.get('username', '')
    resp = make_response(render_template('chat.html', username=username))
    return resp

@app.route('/song')
def song():
    return "<h2>🎵 This is the Song page.</h2>"

users = {}

@socketio.on('connect')
def handle_connect():
    pass  # Username will be sent by client after connect

@socketio.on('set_username')
def handle_set_username(username):
    users[request.sid] = username
    send(f"🟢 {username} joined the chat.", broadcast=True)
    emit('user_list', list(users.values()), broadcast=True)

@socketio.on('disconnect')
def handle_disconnect():
    username = users.pop(request.sid, None)
    if username:
        send(f"🔴 {username} left the chat.", broadcast=True)
        emit('user_list', list(users.values()), broadcast=True)

@socketio.on('message')
def handle_message(msg):
    username = users.get(request.sid, "Anonymous")
    send(f"{username}: {msg}", broadcast=True)

if __name__ == '__main__':
    socketio.run(app, host='0.0.0.0', port=int(os.environ.get('PORT', 60000)), debug=True, log_output=True)