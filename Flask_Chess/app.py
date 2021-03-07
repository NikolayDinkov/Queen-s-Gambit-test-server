from flask import Flask
from flask import render_template, request, redirect, make_response, url_for, flash

app = Flask(__name__)

images = {1:"br", 2:"bn", 3:"bb", 4:"bq", 5:"bk", 6:"bp", 7:"wr", 8:"wn", 9:"wb", 10:"wq", 11:"wk", 12:"wp"}
board = [[0 for x in range(8)] for y in range(8)]

@app.route('/')
def hello_world():
    for i in range(1,6):
        board[0][i-1] = i
        board[7][i-1] = 6+i
    for i in range(3,0,-1):
        board[0][5+3-i] = i
        board[7][5+3-i] = 6+i
    for i in range(0,8):
        board[1][i] = 6
        board[6][i] = 12

    return render_template("display_board.html", board=board, images=images)

@app.route('/2')
def second_page():
    for i in range(1,6):
        board[0][i-1] = i
        board[7][i-1] = 6+i
    for i in range(3,0,-1):
        board[0][5+3-i] = i
        board[7][5+3-i] = 6+i
    for i in range(0,8):
        board[1][i] = 6
        board[6][i] = 12

    return render_template("index.html", board=board, images=images)

if __name__ == '__main__':
    app.run(debug=True)
