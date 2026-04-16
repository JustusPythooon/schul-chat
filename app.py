
from flask import Flask, render_template, request, redirect, session, send_from_directory, jsonify
from flask_socketio import SocketIO, emit, join_room
import os, uuid

app = Flask(__name__)
app.secret_key = 'secret'
socketio = SocketIO(app)

ADMIN_USERNAMES = {"Juli", "Pythoooo0", "Julius"}
messages = {}  # room -> list of messages

def is_admin():
    return session.get('user') in ADMIN_USERNAMES

@app.route('/', methods=['GET','POST'])
def login():
    if request.method == 'POST':
        session['user'] = request.form['username']
        session['is_admin'] = is_admin()
        return redirect('/chat')
    return render_template('login.html')

@app.route('/chat')
def chat():
    if 'user' not in session:
        return redirect('/')
    return render_template('chat.html', user=session['user'], admin=is_admin())

@app.route('/upload_avatar', methods=['POST'])
def upload_avatar():
    file = request.files['avatar']
    filename = session['user'] + '.png'
    file.save(os.path.join('static/avatars', filename))
    return redirect('/chat')

@app.route('/upload', methods=['POST'])
def upload():
    file = request.files['file']
    ext = file.filename.split('.')[-1]
    name = str(uuid.uuid4()) + '.' + ext
    path = os.path.join('uploads', name)
    file.save(path)
    return jsonify({'file': name})

@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory('uploads', filename)

@socketio.on('join')
def join(room):
    join_room(room)
    messages.setdefault(room, [])
    emit('history', messages[room], room=room)

@socketio.on('message')
def msg(data):
    msg = {
        'id': str(uuid.uuid4()),
        'user': session['user'],
        'text': data.get('text'),
        'file': data.get('file')
    }
    messages.setdefault(data['room'], []).append(msg)
    emit('message', msg, room=data['room'])

@socketio.on('delete_message')
def delete_message(data):
    room = data['room']
    msg_id = data['id']
    for m in messages.get(room, []):
        if m['id'] == msg_id:
            if m['user'] == session['user'] or is_admin():
                messages[room].remove(m)
                emit('delete', msg_id, room=room)
            break

if __name__ == '__main__':
    socketio.run(app, host='0.0.0.0', port=5000)
