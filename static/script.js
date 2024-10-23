const TILE_SIZE = 110; // Define tile size as a constant

// Game Logic
function getTilePosition(index) {
    return {
        row: Math.floor(index / 4),
        col: index % 4
    };
}

// Update the board
function updateBoard(board) {
    board.forEach((row, i) => {
        row.forEach((value, j) => {
            const tileId = `tile-${i * 4 + j}`;
            const tile = document.getElementById(tileId);
            if (tile) {
                tile.textContent = value === 0 ? '' : value;
                const position = getTilePosition(i * 4 + j);
                tile.style.transform = `translate(${position.col * TILE_SIZE}px, ${position.row * TILE_SIZE}px)`;
                tile.setAttribute('data-value', value);
            }
        });
    });
}

// Show overlay with given ID and content (game over or you win)
function showOverlay(id, content) {
    let overlay = document.getElementById(id);
    if (!overlay) {
        overlay = document.createElement('div');
        overlay.id = id;
        overlay.innerHTML = content;
        document.body.appendChild(overlay);
    } else {
        overlay.style.display = 'block';
    }
}

// Show the game over overlay
function showGameOver() {
    const gameOverContent = `
        <div class="overlay-content">
            <h1>Game Over!</h1>
            <button id="restart-btn">Restart</button>
        </div>
    `;
    showOverlay('game-over', gameOverContent);
    document.getElementById('restart-btn').addEventListener('click', resetGame);
}

// Show the you win overlay
function showYouWin() {
    const youWinContent = `
        <div class="overlay-content">
            <h1>You Win!</h1>
            <button id="continue-btn">Continue Playing</button>
            <button id="restart-btn">Restart</button>
        </div>
    `;
    showOverlay('you-win', youWinContent);

    // Use event delegation for button click listeners
    document.getElementById('you-win').addEventListener('click', function(event) {
        if (event.target.id === 'continue-btn') {
            document.getElementById('you-win').style.display = 'none';  // Hide the "You Win" overlay
        } else if (event.target.id === 'restart-btn') {
            resetGame();  // Reset the game if the player chooses to restart
        }
    });
}

// Reset the game state and update the board
function resetGame() {
    fetch('/reset', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' }
    })
    .then(response => response.json())
    .then(data => {
        console.log("Board after reset:", data.board);
        updateBoard(data.board);

        // Hide overlays instead of removing them
        const gameOverOverlay = document.getElementById('game-over');
        if (gameOverOverlay) {
            gameOverOverlay.style.display = 'none';
        }
        const youWinOverlay = document.getElementById('you-win');
        if (youWinOverlay) {
            youWinOverlay.style.display = 'none';
        }
    });
}

// Start the game by displaying the initial board
if (typeof initialBoard !== "undefined") {
    console.log("Displaying initial board");
    updateBoard(initialBoard);
}

// Handle keyboard input for movement
document.addEventListener('keydown', function(event) {
    const directionMap = {
        'ArrowUp': 'up',
        'ArrowDown': 'down',
        'ArrowLeft': 'left',
        'ArrowRight': 'right'
    };
    const direction = directionMap[event.key];

    if (direction) {
        fetch('/move', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ direction })
        })
        .then(response => response.json())
        .then(data => {
            console.log("Board received from Flask:", data.board);
            updateBoard(data.board);

            // Check for game status
            if (data.status === 'game_over') {
                showGameOver();  // Show the defeat screen when the game is over
            } else if (data.status === 'you_win') {
                showYouWin();  // Show the "You Win" screen when the player wins
            }
        });
    }
});
