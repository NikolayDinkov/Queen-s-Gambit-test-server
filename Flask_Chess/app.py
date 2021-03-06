from flask import Flask
from flask import render_template, request, redirect, make_response, url_for, flash

app = Flask(__name__)


@app.route('/')
def hello_world(board=None):
    board = [[0 for x in range(8)] for y in range(8)]
    return render_template("display_board.html", board=board)

@app.route('/2')
def second_page():
    board = [[0 for x in range(8)] for y in range(8)]
    return render_template("index.html", board=board)

if __name__ == '__main__':
    app.run(debug=True)
