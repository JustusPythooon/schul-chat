
from flask import Flask, render_template, request, redirect, session
from flask_socketio import SocketIO, emit, join_room

app = Flask(__name__)
app.secret_key = 'secret'
socketio = SocketIO(app)

ADMIN_USERNAMES = {"Juli", "Pythoooo0", "Julius"}
USERS = set()

@app.route('/', methods=['GET','POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        USERS.add(username)
        session['user'] = username
        session['is_admin'] = username in ADMIN_USERNAMES
        return redirect('/dashboard')
    return render_template('login.html')

@app.route('/dashboard')
def dashboard():
    if 'user' not in session:
        return redirect('/')
    return render_template('dashboard.html', admin=session.get('is_admin'))

@app.route('/chat')
def chat():
    if 'user' not in session:
        return redirect('/')
    return render_template('chat.html', user=session['user'])

@app.route('/admin')
def admin():
    if not session.get('is_admin'):
        return 'Zugriff verweigert', 403
    return render_template('admin.html', users=USERS)

@socketio.on('message')
def msg(data):
    emit('message', {'user': session.get('user'), 'text': data}, broadcast=True)

if __name__ == '__main__':
    socketio.run(app, host='0.0.0.0', port=5000)
