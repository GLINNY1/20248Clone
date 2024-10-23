# 2048 Game

This is a web-based implementation of the popular game **2048** built using **Flask** (backend) and **JavaScript** (frontend). The goal of the game is to combine tiles with the same values to reach the number **2048**.

## Features

- Move tiles using the arrow keys (Up, Down, Left, Right).
- Tiles combine when they match, doubling the value.
- Game over and victory screens when appropriate.
- A simple UI that dynamically updates the board.
- Reset option to start a new game.
- Continue playing even after reaching 2048.

## Technology Stack

- **Backend**: Python (Flask) for handling the game logic and API requests.
- **Frontend**: HTML, CSS, JavaScript for rendering the game board and capturing user input.
- **AJAX**: Used to handle requests between the frontend and the Flask server asynchronously.

## Project Structure

```bash
.
├── static/
│   ├── styles.css         # Contains CSS styles for the game board and overlays
│   └── script.js          # Main JavaScript logic for updating the board and handling user interaction
├── templates/
│   └── index.html         # Main HTML file rendering the game board
├── app.py                 # Flask server handling the backend logic
└── README.md              # Project documentation
