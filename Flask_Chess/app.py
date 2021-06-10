import random
import json

from flask import Flask
from sqlalchemy.orm.query import AliasOption
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
    moves = db.Column(db.String(5000), nullable=False)
    finished = db.Column(db.Integer, nullable=False)

    def __repr__(self):
        return f"Post('{self.title}')"

# class Lobby(db.Document):
#     title = db.StringField(nullable=False)
#     player_num = db.IntegerField(nullable=False)
#     password = db.IntegerField(nullable=False)
#     gameState = db.StringField(nullable=False)
#     publicity = db.StringField(nullable=False)

# class Game_details(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     lobby_id = db.Column(db.Integer, db.ForeignKey('lobby.id'), nullable=False)
#     # lobby_id = db.Column(db.Integer)
#     moves = db.Column(db.String(5000))
#     title = db.Column(db.String(100), unique=False, nullable=False)
#     white_player = db.Column(db.String(20))
#     black_player = db.Column(db.String(20))

db.create_all()
gameLobby_list = []
game = {}
white_users = []
black_users = []
room_codes = []

@app.errorhandler(404)
def page_not_found(e):
    return render_template("error_404.html"), 400

@app.errorhandler(500)
def internal_error(e):
	return render_template("error_500.html"), 500

################################################3

@socketio.on('connect')
def on_connect():
    send("Someone had connected", broadcast=True)

@socketio.on('disconnect')
def on_disconnect():
    send("Someone had disconnected", broadcast=True)

@socketio.on('message')
def handleMessage(msg):
    print('Message:', str(msg))
    send(msg)

@socketio.on("move")
def move(data):
    emit("move", data, to=data["room"])

@socketio.on('join')
def on_join(data):
    guest_nubmer = random.randint(1000, 100000)
    username = "guest" + str(guest_nubmer)
    room = data['room']
    lobby = Lobby.query.filter_by(id=int(room)).first()
    if lobby.player_num % 2 == 1:
        white_users.append(username)
        lobby.white_player = username
    elif lobby.player_num % 2 == 0:
        black_users.append(username)
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

@app.route('/lobbies', methods=['GET'])
def lobbies():
    lobbies = Lobby.query.all()
    print(lobbies)
    lobbies_av = []
    for lobby in lobbies:
        if lobby.player_num == 1:
            lobbies_av.append(lobby)
    return render_template('lobbies.html', lobbies=lobbies_av)
    
@app.route('/replays', methods=['GET'])
def replays():
    lobbies = Lobby.query.all()
    lobbies_av = []
    for lobby in lobbies:
        if lobby.finished == 1:
            lobbies_av.append(lobby)
    return render_template('replays_page.html', lobbies=lobbies_av)

@app.route('/replay/<int:game_id>', methods=['GET'])
def replay(game_id):
    # table = table()
    lobby = Lobby.query.filter_by(id=game_id).first()
    white = lobby.white_player
    black = lobby.black_player
    game[str(game_id)] = table()

    return render_template('index_replay.html', 
    board=game[str(game_id)].board,
    id=str(game_id), 
    white=white,
    black=black,
    turn=lobby.player_num-1,
    moves = lobby.moves)


@app.route('/create_lobby', methods=['GET', 'POST'])
def create_lobby():
    global game
    if request.method == 'GET':
        return render_template('create_lobby.html')
    else:
        title = request.form['title']
        publicity = request.form['publicity']
        print(publicity)
        lobby = Lobby(title=title, player_num=0, password=random.randint(1000000, 10000000), gameState="Created", publicity=publicity, white_player="", black_player="", moves="", finished=0)
        db.session.add(lobby)
        db.session.commit()
        game[str(lobby.id)] = table()
        return redirect('/index/' + str(lobby.id))

@app.route('/join_lobby', methods=['GET', 'POST'])
def join_lobby():
    if request.method == 'GET':
        return render_template('join_lobby.html')
    else:
        code = request.form['code']
        for lobby in Lobby.query.all():
            if str(lobby.password) == code and lobby.player_num == 1:
                return redirect('/index/' + str(lobby.id))
        flash("Invalid code", 'warning')
        return redirect(url_for('join_lobby'))

@app.route('/index/<int:id>', methods=['GET', 'POST'])
def index(id):
    global game
    lobby = Lobby.query.filter_by(id=id).first()
    lobby.player_num = lobby.player_num + 1
    db.session.commit()
    white = lobby.white_player
    black = lobby.black_player
    print(type(game))
    print(game[str(id)])
    return render_template('index.html', 
    board=game[str(id)].board,
    id=str(id), 
    password=lobby.password,
    white=white,
    black=black,
    turn=lobby.player_num-1)

@app.route('/ajax', methods = ['POST'])
def ajax_request():
    global game
    old_pos_x = ""
    old_pos_y = ""
    new_pos_x = ""
    new_pos_y = ""
    id = request.form["room_id"]
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
                # print(coordinates)
                
        else:
            allowed = game[id].get_move_input(coordinates[0], coordinates[1])
            # print(coordinates)
            # lobby = Lobby.query.filter_by(id=id).first()
            # lobby.moves = lobby.moves + str(coordinates)
            # print(lobby.moves)
    else:
        coordinates = ["","","",""]
        allowed = False

    if(allowed == True):
        lobby = Lobby.query.filter_by(id=id).first()
        print(f'cooridinates[0] = "{game[id].convert_input_string_to_coordinates(coordinates[0], coordinates[1])}"')
        lobby.moves = lobby.moves + str(old_pos[9:11]) + str(new_pos[9:11])
        print(lobby.moves)

    turn = game[id].print_turn()
    print("allowed = ",allowed)

    game[id].print_board()

    if (allowed == True):
        for col in range(8):
                for row in range(8):
                    if game[id].board[col][row].name == "bk":
                        if game[id].checkmate(col, row):
                            flash("White is the winner")
                            print("Black king is dead")
                            lobby = Lobby.query.filter_by(id=id).first()
                            lobby.finished = 1
                            db.session.commit()
                            return ({"old_position": coordinates[0], "new_position":coordinates[1], "allowed":allowed, "restart":restart, "turn": turn, "redirect":url_for("replays")})

                    if game[id].board[col][row].name == "wk":
                        if game[id].checkmate(col, row):
                            flash("Black is the winner")
                            print("White king is dead")
                            lobby = Lobby.query.filter_by(id=id).first()
                            lobby.finished = 1
                            db.session.commit()
                            return ({"old_position": coordinates[0], "new_position":coordinates[1], "allowed":allowed, "restart":restart, "turn": turn, "redirect":url_for("replays")})



    return ({"old_position": coordinates[0], "new_position":coordinates[1], "allowed":allowed, "restart":restart, "turn": turn, "redirect":""})

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
