import os
from flask import (
    Flask, session, Blueprint, flash, g, redirect, render_template, request, url_for
)
from flask_socketio import SocketIO, send, join_room, leave_room, emit

from werkzeug.exceptions import abort


# create and configure the app
app = Flask(__name__, instance_relative_config=True)
app.config['SECRET_KEY'] = 'secret'
socketio = SocketIO(app)


# ensure the instance folder exists
try:
    os.makedirs(app.instance_path)
except OSError:
    pass


@app.route('/', methods=('GET', 'POST'))
def index():
    if request.method == 'POST':
        room_name = request.form['room_name']
        session['room'] = room_name
        return redirect(url_for('room', room=room_name))
    else:
        room_name = session.get('room', '')
        return render_template('index.html')
    
@app.route('/<string:room>')
def room(room):
    session['room'] = room
    return render_template('room.html')



@socketio.on('join')
def joined():
    room = session.get('room')
    join_room(room)
    print('User has entered : ' + room)
    emit('status', 'User has entered ' + session.get('room'), room=room)

@socketio.on('leave')
def left():
    room = session.get('room')
    leave_room(room)
    emit('status', 'User has left:' + session.get('room'), room=room)

@socketio.on('text')
def text(message):
    room = session.get('room')
    print('User has entered '+message+ ' in ' +session.get('room'))
    emit('message', message, room=room)
from . import events

if __name__ == "__main__":
    #app.run(host='0.0.0.0')
    socketio.run(app)
