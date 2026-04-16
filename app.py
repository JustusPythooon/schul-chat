
from flask import Flask, render_template, request, redirect, session
from flask_socketio import SocketIO, emit, join_room
import sqlite3, uuid

app = Flask(__name__)
app.secret_key = 'secret'
socketio = SocketIO(app)

DB = 'chat.db'

def db():
    return sqlite3.connect(DB, check_same_thread=False)

cur = db().cursor()
cur.execute('CREATE TABLE IF NOT EXISTS users (name TEXT PRIMARY KEY)')
cur.execute('CREATE TABLE IF NOT EXISTS messages (id TEXT, room TEXT, user TEXT, text TEXT)')
db().commit()

@app.route('/', methods=['GET','POST'])
def login():
    if request.method == 'POST':
        u = request.form['username']
        session['user'] = u
        cur = db().cursor()
        cur.execute('INSERT OR IGNORE INTO users VALUES (?)', (u,))
        db().commit()
        return redirect('/chat')
    return render_template('login.html')

@app.route('/chat')
def chat():
    users = [u[0] for u in db().cursor().execute('SELECT name FROM users')]
    return render_template('chat.html', user=session['user'], users=users)

@socketio.on('join')
def join(data):
    join_room(data)
    cur = db().cursor()
    msgs = cur.execute('SELECT id,user,text FROM messages WHERE room=?', (data,)).fetchall()
    for m in msgs:
        emit('message', {'id': m[0], 'user': m[1], 'text': m[2]}, room=session.sid)

@socketio.on('send')
def send(data):
    mid = str(uuid.uuid4())
    cur = db().cursor()
    cur.execute('INSERT INTO messages VALUES (?, ?, ?, ?)', (mid, data['room'], session['user'], data['text']))
    db().commit()
    emit('message', {'id': mid, 'user': session['user'], 'text': data['text']}, room=data['room'])

if __name__ == '__main__':
    socketio.run(app, host='0.0.0.0', port=5000)
