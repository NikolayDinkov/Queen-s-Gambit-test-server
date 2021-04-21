import random
import json

from flask import Flask
from chess import table
from flask import render_template, request, redirect, make_response, url_for, flash, jsonify

from flask_socketio import SocketIO, join_room, send, emit
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import text
from flask_mongoengine import MongoEngine

app = Flask(__name__)
app.config['SECRET_KEY'] = 'azsumsecretkey'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test1.db'
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db = SQLAlchemy(app)

socketio = SocketIO(app)

# app.config['MONGODB_SETTINGS'] = {
#     'db': 'your_database',
#     'host': 'localhost',
#     'port': 27017
# }

# db = MongoEngine()
# db.init_app(app)

class Lobby(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), unique=False, nullable=False)
    player_num = db.Column(db.Integer, nullable=False)
    password = db.Column(db.Integer, nullable=False)
    gameState = db.Column(db.String(15), unique=False, nullable=False)
    publicity = db.Column(db.String(15), unique=False, nullable=False)
    white_player = db.Column(db.String(20))
    black_player = db.Column(db.String(20))

    def __repr__(self):
        return f"Post('{self.title}')"

# class Lobby(db.Document):
#     title = db.StringField(nullable=False)
#     player_num = db.IntegerField(nullable=False)
#     password = db.IntegerField(nullable=False)
#     gameState = db.StringField(nullable=False)
#     publicity = db.StringField(nullable=False)


db.create_all()
gameLobby_list = []
game = {}
users = {}
room_codes = []

################################################3


@socketio.on('connect')
def on_connect():
    pass

@socketio.on('disconnect')
def on_connect():
    send("Someone had disconnected")

@socketio.on('message')
def handleMessage(msg):
    print('Message:', str(msg))
    send(msg)

@socketio.on("move")
def move(data):
    emit("move", data, to=data["room"])

@socketio.on("get_session_id")
def get_sessino_id():
    emit("session_id", request.sid)

@socketio.on('join')
def on_join(data):
    guest_nubmer = random.randint(1000, 100000)
    username = "guest" + str(guest_nubmer)
    room = data['room']
    lobby = Lobby.query.filter_by(id=int(room)).first()
    if lobby.player_num == 1:
        lobby.white_player = username
    elif lobby.player_num == 2:
        lobby.black_player = username
    db.session.commit()
    

    print("WOw username is {}".format(username))
    print("player: {} has joined room: {}".format(username, room))
    join_room(room)
    emit("guests_names", {"white" : lobby.white_player, "black" : lobby.black_player}, to=room)
    #send("player \"" + username + "\" has joined.", to=room)

@socketio.on('leave')
def on_leave(data):
    username = data['username']
    room = data['room']
    leave_room(room)
    send(username + ' has left the room.', to=room)

##########################################################

@app.route('/', methods=['GET', 'POST'])
def front_page():
    return render_template('frontPage.html')

@app.route('/lobbies', methods=['GET', 'POST'])
def lobbies():
    lobbies = Lobby.query.all()
    lobbies_av = []
    for lobby in lobbies:
        if lobby.player_num == 1:
            lobbies_av.append(lobby)
    return render_template('lobbies.html', lobbies=lobbies_av)

@app.route('/create_lobby', methods=['GET', 'POST'])
def create_lobby():
    if request.method == 'GET':
        return render_template('create_lobby.html')
    else:
        title = request.form['title']
        publicity = request.form['publicity']
        print(publicity)
        lobby = Lobby(title=title, player_num=0, password=random.randint(1000000, 10000000), gameState="Created", publicity=publicity, white_player="", black_player="")
        db.session.add(lobby)
        db.session.commit()
        return redirect('/index/' + str(lobby.id))

@app.route('/join_lobby', methods=['GET', 'POST'])
def join_lobby():
    if request.method == 'GET':
        return render_template('join_lobby.html')
    else:
        code = request.form['code']
        for lobby in Lobby.query.all():
            if str(lobby.password) == code and lobby.player_num == 1:
                lobby.player_num = 2
                db.session.commit()
                return redirect('/index/' + str(lobby.id))
        # flash("Invalid code", 'warning')
        return redirect(url_for('join_lobby'))

@app.route('/index/<int:id>', methods=['GET', 'POST'])
def index(id):
    global game
    game[str(id)] = table()
    # gameLobby_list.append(game)
    # print(game.board[0][0].name)
    lobby = Lobby.query.filter_by(id=id).first()
    lobby.player_num = lobby.player_num + 1
    white = lobby.white_player
    black = lobby.black_player
    db.session.commit()
    #flash(lobby.title)
    #flash(lobby.password)
    return render_template('index.html', board=game[str(id)].board, id=str(id), password=lobby.password, white=white, black=black)

@app.route('/ajax', methods = ['POST'])
def ajax_request():
    global game
    old_pos_x = ""
    old_pos_y = ""
    new_pos_x = ""
    new_pos_y = ""
    id = request.form["room_id"]

    print((type(id)))

    old_pos = request.form['old_pos']
    if old_pos != "":
        old_pos_x = int(old_pos[9])
        old_pos_y = int(old_pos[10])

    new_pos = request.form['new_pos']
    if new_pos != "":
        new_pos_x = int(new_pos[9])
        new_pos_y = int(new_pos[10])

    restart = request.form['restart']
    if restart == "True":
        game[id] = table()

    if old_pos != "" and new_pos != "":
        coordinates = game[id].convert_coordinates_to_string(old_pos_x, old_pos_y, new_pos_x, new_pos_y)
        if (game[id].board[old_pos_y][old_pos_x].name in ["wk", "wr", "bk", "br"]
        and game[id].board[new_pos_y][new_pos_x].name in ["wk", "wr", "bk", "br"]):
            if ((coordinates[0][0] == "E" or coordinates[1][0] == "E")
            and (coordinates[1][0] == "A" or coordinates[0][0] == "A")):
                allowed = game[id].get_move_input("0-0-0")
            elif ((coordinates[0][0] == "E" or coordinates[1][0] == "E")
            and (coordinates[1][0] == "H" or coordinates[0][0] == "H")):
                allowed = game[id].get_move_input("0-0")
        else:
            allowed = game[id].get_move_input(coordinates[0], coordinates[1])
    else:
        coordinates = ["","","",""]
        allowed = False

    turn = game[id].print_turn()
    print("allowed = ",allowed)

    game[id].print_board()

    return ({"old_position": coordinates[0], "new_position":coordinates[1], "allowed":allowed, "restart":restart, "turn": turn})

if __name__ == '__main__':
    socketio.run(app, debug=True)



"""
@app.route('/ajax', methods = ['POST', 'GET'])
def ajax_request():
    old_pos_x = ""
    old_pos_y = ""
    new_pos_x = ""
    new_pos_y = ""

    old_pos = request.form['old_pos']
    if old_pos != "":
        old_pos_x = int(old_pos[9])
        old_pos_y = int(old_pos[10])

    new_pos = request.form['new_pos']
    if new_pos != "":
        new_pos_x = int(new_pos[9])
        new_pos_y = int(new_pos[10])

    restart = request.form['restart']
    if restart == "True":
        global game
        game = table()

    if old_pos != "" and new_pos != "":
        coordinates = game.convert_coordinates_to_string(old_pos_x, old_pos_y, new_pos_x, new_pos_y)
        if (game.board[old_pos_y][old_pos_x].name in ["wk", "wr", "bk", "br"]
        and game.board[new_pos_y][new_pos_x].name in ["wk", "wr", "bk", "br"]):
            if ((coordinates[0][0] == "E" or coordinates[1][0] == "E")
            and (coordinates[1][0] == "A" or coordinates[0][0] == "A")):
                allowed = game.get_move_input("0-0-0")
                restart = "refresh"
            elif ((coordinates[0][0] == "E" or coordinates[1][0] == "E")
            and (coordinates[1][0] == "H" or coordinates[0][0] == "H")):
                allowed = game.get_move_input("0-0")
                restart = "refresh"
        else:
            allowed = game.get_move_input(coordinates[0], coordinates[1])
    else:
        coordinates = ["","","",""]
        allowed = False

    return jsonify(old_position=coordinates[0], new_position=coordinates[1], allowed=allowed, restart=restart)

"""
