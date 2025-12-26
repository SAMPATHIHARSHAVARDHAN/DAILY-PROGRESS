from flask import Flask, render_template, request, jsonify, redirect, url_for

app = Flask(__name__)

board = [""] * 9
current_player = "X"
winner_result = ""

def check_winner():
    wins = [
        (0,1,2),(3,4,5),(6,7,8),
        (0,3,6),(1,4,7),(2,5,8),
        (0,4,8),(2,4,6)
    ]
    for a,b,c in wins:
        if board[a] == board[b] == board[c] and board[a] != "":
            return board[a]
    if "" not in board:
        return "Draw"
    return None

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/play", methods=["POST"])
def play():
    global current_player, winner_result
    index = request.json["index"]

    if board[index] == "":
        board[index] = current_player
        result = check_winner()

        if result:
            winner_result = result
            return jsonify(board=board, winner=result)

        current_player = "O" if current_player == "X" else "X"

    return jsonify(board=board, winner=None, turn=current_player)

@app.route("/result")
def result():
    return render_template("result.html", winner=winner_result)

@app.route("/reset")
def reset():
    global board, current_player, winner_result
    board = [""] * 9
    current_player = "X"
    winner_result = ""
    return redirect(url_for("home"))

if __name__ == "__main__":
    app.run(debug=True)
