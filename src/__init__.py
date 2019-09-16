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

#Contains list of existing rooms and their respective users
room_list = {}


@app.route('/', methods=('GET', 'POST'))
def index():
    if request.method == 'POST':
        room_name = request.form['room_name']
        #Make Room
        if request.form['action'] == 'make':     
            if room_name not in room_list:
                room_list[room_name] = []
                session['room'] = room_name
                return redirect(url_for('room', room=session.get('room')))
            else:
                print('Room already exists')
                return render_template('index.html')
        #Join Room
        if request.form['action'] == 'join':
            if room_name in room_list:
                return redirect(url_for('room', room=session.get('room')))
            else:
                print('Room does not exist')
                return render_template('index.html')
    else:
        room_name = session.get('room', '')
        return render_template('index.html')
    
@app.route('/<string:room>')
def room(room):
    if(room in room_list):
        session['room'] = room
        return render_template('room.html')
    else:
        return redirect(url_for('index'))

@socketio.on('join')
def joined():
    session['id'] = request.sid
    room = session.get('room')
    join_room(room)
    print('User has entered : ' + room)
    emit('user init', room_list[room], room=room)
    
@socketio.on('leave')
def left():
    room = session.get('room')
    room_list[room].remove(session.get('username'))
    print(room_list[room])
    leave_room(room)
    emit('user left', session.get('username'), room=room)

@socketio.on('text')
def text(message):
    room = session.get('room')
    print('User has entered '+message+ ' in ' +session.get('room'))
    emit('message', {'message':message, 'username':session.get('username')}, room=room)

@socketio.on('add user')
def adduser(username):
    room = session.get('room')
    session['username'] = username
    room_list[room].append(username)
    print(session.get('username') + ' has been added to room ' + room)
    print(room_list[room])
    emit('user added', username, room=room)

@socketio.on('video paused')
def pausevideo():
    room = session.get('room')
    print('video has been paused')
    emit('pause video', room=room)

@socketio.on('video played')
def playvideo():
    room = session.get('room')
    print('video playing')
    emit('play video', room=room)

@socketio.on('video buffering')
def buffervideo(time):
    room = session.get('room')
    print('video buffering')
    emit('buffer video', time, room=room)



if __name__ == "__main__":
    #app.run(host='0.0.0.0')
    socketio.run(app)
