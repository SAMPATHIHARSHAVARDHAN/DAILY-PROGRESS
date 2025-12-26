function makeMove(index) {
    fetch("/play", {
        method: "POST",
        headers: {"Content-Type": "application/json"},
        body: JSON.stringify({index: index})
    })
    .then(res => res.json())
    .then(data => {
        updateBoard(data.board)

        if (data.winner) {
            setTimeout(() => {
                window.location.href = "/result"
            }, 500)
        } else {
            document.getElementById("turn").innerText =
                "Player " + data.turn + " Turn"
        }
    })
}

function updateBoard(board) {
    let cells = document.getElementsByClassName("cell")
    for (let i = 0; i < 9; i++) {
        cells[i].innerText = board[i]
    }
}
