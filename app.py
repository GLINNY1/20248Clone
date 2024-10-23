from flask import Flask, jsonify, render_template, request
import random # generating random numbers for empty tiles
import copy # copying the board 

app = Flask(__name__)

# Game Logic
class Game2048:

    # Initializing the board 
    def __init__(self):
        self.boardStart() # calls the boardStart function
    
    def boardStart(self):
        self.board = [[0] * 4 for _ in range(4)] # setting the board to 4x4
        self.newTile() # generates a new tile on the board either 2 or 4
        self.newTile() # generates a new tile on the board either 2 or 4
        self.game_won = False # checks if the game is won or not

    # Add a new tile to the board
    def newTile(self): 
        # Find all empty tiles on the board and creates a list of them
        empty_tiles = [(i, j) for i in range(4) for j in range(4) if self.board[i][j] == 0]
        # if there are empty tiles in the board generates a random number between 2 and 4 and adds it to the board
        if empty_tiles:
            i, j = random.choice(empty_tiles)
            self.board[i][j] = random.choice([2, 4])

    # Move the tiles in the board
    def move(self, direction):
        original_board = copy.deepcopy(self.board)

        # Movement operations abstracted into reusable functions
        def apply_move(board, transpose=False, reverse=False):
            if transpose:
                board = self.transpose(board)
            if reverse:
                board = self.reverse(board)
            board = self.merge(board)
            if reverse:
                board = self.reverse(board)
            if transpose:
                board = self.transpose(board)
            return board

        # Dictionary of movement operations
        moves = {
            'up': lambda b: apply_move(b, transpose=True),
            'down': lambda b: apply_move(b, transpose=True, reverse=True),
            'left': apply_move,
            'right': lambda b: apply_move(b, reverse=True)
        }

        # Perform the movement
        if direction in moves:
            self.board = moves[direction](self.board)
            
        # Check if the board has changed
        if self.board != original_board:
            self.newTile()

        # Check if the game is over
        if self.gameOver():
            return "game_over"
        
        # Check if the game is won
        if self.checkWin():
            return "you_win"

    # Reverse the board
    def reverse(self, board):
        return [row[::-1] for row in board]

    # Transpose the board
    def transpose(self, board):
        return [list(row) for row in zip(*board)]

    # Merge the tiles
    def merge(self, board):
        for i in range(4):
            temp = [x for x in board[i] if x != 0]
            j = 0
            while j < len(temp) - 1:
                if temp[j] == temp[j + 1]:
                    temp[j] *= 2
                    temp.pop(j + 1)  # Remove the merged tile
                j += 1
            board[i] = temp + [0] * (4 - len(temp))
        return board
    
    # Check if the game is over
    def gameOver(self):
        # Check if any move is possible (adjacent tiles can merge or empty tiles exist)
        for i in range(4):
            for j in range(4):
                if self.board[i][j] == 0 or \
                   (j < 3 and self.board[i][j] == self.board[i][j + 1]) or \
                   (i < 3 and self.board[i][j] == self.board[i + 1][j]):
                    return False
        return True

    # Check if the game is won
    def checkWin(self):
        if not self.game_won:
            for row in self.board:
                if 2048 in row:
                    self.game_won = True
                    return True
        return False

# Flask Routes
game = Game2048()

@app.route('/')
def index(): # route for the home page
    return render_template('index.html', board=game.board)

@app.route('/move', methods=['POST'])
def move(): # route for moving the tiles
    direction = request.json['direction']
    result = game.move(direction)

    if result == "game_over":
        return jsonify({'board': game.board, 'status': 'game_over'})
    elif result == "you_win":
        return jsonify({'board': game.board, 'status': 'you_win'})

    return jsonify({'board': game.board})

@app.route('/reset', methods=['POST'])
def reset(): # route for resetting the game
    game.boardStart()
    return jsonify({'board': game.board})

if __name__ == '__main__': # main function
    app.run(debug=True)
