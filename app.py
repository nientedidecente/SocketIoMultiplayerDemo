from flask import Flask, render_template, request
from flask_socketio import SocketIO, emit
import uuid

app = Flask(__name__)
app.config['SECRET_KEY'] = 'c8m349cty02x'
socketio = SocketIO(app)
games = []


def findgame(sid):
    global games

    if not games or games[-1]['player2'] is not None:
        gameid = str(uuid.uuid4())
        games.append({'player1': sid, 'player2': None, 'gameid': gameid})
        return gameid
    else:
        games[-1]['player2'] = sid
        return games[-1]['gameid']


@app.route('/')
def sessions():
    return render_template('gamepage.html')


@socketio.on('login')
def login(json):
    print('new user: {}'.format(request.sid))
    gameid = findgame(request.sid)
    print('match assigned: {}'.format(gameid))
    emit('match_created', gameid)


if __name__ == '__main__':
    socketio.run(app, debug=True)
