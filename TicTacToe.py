"""
Tic Tac Toe game in Python
Two players (X and O) take turns in the terminal.
"""

def display_board(board):
    print()
    for i in range(3):
        row = f" {board[i*3]} | {board[i*3+1]} | {board[i*3+2]} "
        print(row)
        if i < 2:
            print("---+---+---")
    print()


def check_win(board, player):
    combinations = [
        (0, 1, 2), (3, 4, 5), (6, 7, 8),  # rows
        (0, 3, 6), (1, 4, 7), (2, 5, 8),  # columns
        (0, 4, 8), (2, 4, 6)              # diagonals
    ]
    return any(all(board[c] == player for c in combo) for combo in combinations)


def board_full(board):
    return all(cell != " " for cell in board)


def ask_move(board, player):
    while True:
        try:
            choice = input(f"Player {player}, choose a cell (1-9): ")
            cell = int(choice) - 1
            if cell < 0 or cell > 8:
                print("Please choose a number between 1 and 9.")
            elif board[cell] != " ":
                print("That cell is already taken, choose another one.")
            else:
                return cell
        except ValueError:
            print("Invalid input, please enter a number between 1 and 9.")


def play():
    board = [" "] * 9
    current_player = "X"

    print("Welcome to Tic Tac Toe!")
    print("Cells are numbered 1 to 9 like this:")
    print(" 1 | 2 | 3 ")
    print("---+---+---")
    print(" 4 | 5 | 6 ")
    print("---+---+---")
    print(" 7 | 8 | 9 ")

    while True:
        display_board(board)
        cell = ask_move(board, current_player)
        board[cell] = current_player

        if check_win(board, current_player):
            display_board(board)
            print(f"🎉 Player {current_player} wins!")
            break

        if board_full(board):
            display_board(board)
            print("It's a draw!")
            break

        current_player = "O" if current_player == "X" else "X"

    play_again = input("Do you want to play again? (y/n): ").strip().lower()
    if play_again == "y":
        play()
    else:
        print("Thanks for playing, see you next time!")


if __name__ == "__main__":
    play()
