import os
import json
import math
from flask import (
    Flask, session, Blueprint, flash, g, redirect, render_template, request, url_for
)
from flask_socketio import SocketIO, send, join_room, leave_room, emit

from werkzeug.exceptions import abort


# create and configure the app
app = Flask(__name__, instance_relative_config=True)
app.config['SECRET_KEY'] = 'secret'
socketio = SocketIO(app, async_mode="eventlet")

# ensure the instance folder exists
try:
    os.makedirs(app.instance_path)
except OSError:
    pass

#Contains list of existing rooms and their respective users
# 'room' contains 
room_list = {}


@app.route('/', methods=('GET', 'POST'))
def index():
    if request.method == 'POST':
        room_name = request.form['room_name']
        #Make Room
        if request.form['action'] == 'make':     
            if room_name not in room_list:
                room_list[room_name] = { "Users": [], "Curr_Vid": "", "Queue": [], "Votes": 0}
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
    print(room_list[room])
    emit('user init', room_list[room], room=room)
    
    
@socketio.on('leave')
def left():
    room = session.get('room')
    room_list[room]["Users"].remove(session.get('username'))
    print('User has left')
    print(room_list[room]["Users"])
    leave_room(room)
    emit('user left', session.get('username'), room=room)
    emit('update users', room_list[room]["Users"], room=room)

@socketio.on('text')
def text(message):
    room = session.get('room')
    print('User has entered '+message+ ' in ' +session.get('room'))
    emit('message', {'message':message, 'username':session.get('username')}, room=room)

@socketio.on('add user')
def adduser(username):
    room = session.get('room')
    session['username'] = username
    room_list[room]["Users"].append(username)
    print(session.get('username') + ' has been added to room ' + room)
    print(room_list[room])
    emit('user added', username, room=room)
    emit('update users', room_list[room]["Users"], room=room)
    emit('load playlist', room_list[room]["Queue"], room=room)

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

@socketio.on('queue video')
def queuevideo(url):
    room = session.get('room')
    room_list[room]["Queue"].append(url)
    print(room_list[room])
    emit('add to queue', room_list[room]["Queue"], room=room)

@socketio.on('nextvideo')
def nextvideo():
    room = session.get('room')
    if len(room_list[room]["Queue"]) > 0:
        next_vid = room_list[room]["Queue"][0]
        del room_list[room]["Queue"][0]
        room_list[room]["Votes"] = 0
        print(room_list[room])
        emit('load next video', next_vid, room=room)
        emit('update curr vid client', next_vid, room=room)
        emit('update queue', room_list[room]["Queue"], room=room)
        emit('update votes', room_list[room]["Votes"], room=room)

@socketio.on('update curr vid')
def updateCurrVid(url):
    room = session.get('room')
    room_list[room]["Curr_Vid"] = url
    print(room_list[room])
    emit('update curr vid client', url, room=room)

@socketio.on('load video')
def loadvideo(url):
    room = session.get('room')
    emit('load new video', url, room=room)

@socketio.on('vote')
def vote():
    room = session.get('room')
    room_list[room]["Votes"] += 1
    votes = room_list[room]["Votes"]
    numusers = len(room_list[room]["Users"])
    if votes == math.ceil(numusers/2):
        if len(room_list[room]["Queue"]) > 0:
            next_vid = room_list[room]["Queue"][0]
            del room_list[room]["Queue"][0]
            room_list[room]["Votes"] = 0
            print(room_list[room])
            emit('load next video', next_vid, room=room)
            emit('update curr vid client', next_vid, room=room)
            emit('update queue', room_list[room]["Queue"], room=room)
            emit('update votes', room_list[room]["Votes"], room=room)

if __name__ == "__main__":
    #app.run(host='0.0.0.0')
    socketio.run(app)
