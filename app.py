
from flask import Flask, render_template, request, redirect, session
from flask_socketio import SocketIO, emit, join_room
import os

app = Flask(__name__)
app.secret_key = 'secret'
socketio = SocketIO(app)

USERS = {}

@app.route('/', methods=['GET','POST'])
def login():
    if request.method=='POST':
        session['user']=request.form['username']
        return redirect('/chat')
    return render_template('login.html')

@app.route('/chat')
def chat():
    if 'user' not in session: return redirect('/')
    return render_template('chat.html', user=session['user'])

@app.route('/upload', methods=['POST'])
def upload():
    file = request.files['file']
    path = os.path.join('uploads', file.filename)
    file.save(path)
    return {'file': file.filename}

@socketio.on('join')
def join(data):
    join_room(data['room'])

@socketio.on('message')
def message(data):
    emit('message', data, broadcast=True)

if __name__ == '__main__':
    socketio.run(app, host='0.0.0.0', port=5000)
