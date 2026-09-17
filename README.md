# Littles Games

A collection of small terminal games written in Python.

## Games

### Hangman

Guess the hidden word one letter at a time before you run out of attempts.

File: `Handman_minigame.py`

### Snake

Control the snake, eat the food, and try to achieve the highest score without
hitting the wall or yourself.

File: `Snake.py`

### Tic Tac Toe

Two players take turns placing `X` and `O`. The first player to align three
symbols wins.

File: `TicTacToe.py`

## Requirements

- Python 3.8 or newer
- Windows is recommended for Snake because it uses `msvcrt` and the Windows
  console API for real-time keyboard input.

## Installation

Clone the repository and open its folder:

```powershell
git clone https://github.com/Kaezuria/Littles-games.git
cd Littles-games
```

No external Python packages are required. The games use only the Python
standard library.

## Run A Game

Start Hangman:

```powershell
python Handman_minigame.py
```

Start Snake:

```powershell
python Snake.py
```

Start Tic Tac Toe:

```powershell
python TicTacToe.py
```

## Controls

### Hangman

- Enter one letter at a time.
- Type `y` when asked if you want to play again.

### Snake

- `W` or Up Arrow: move up
- `S` or Down Arrow: move down
- `A` or Left Arrow: move left
- `D` or Right Arrow: move right
- `Q`: quit

### Tic Tac Toe

Enter a number from `1` to `9` to select a cell:

```text
 1 | 2 | 3
---+---+---
 4 | 5 | 6
---+---+---
 7 | 8 | 9
```

## Project Structure

```text
Littles-games/
├── Handman_minigame.py
├── Snake.py
├── TicTacToe.py
└── README.md
```

## Author

Created by **Kaezuria**.
