"""Treasure Run: a small turn-based terminal adventure."""

import os
import random
from typing import Set, Tuple

Position = Tuple[int, int]

WIDTH = 13
HEIGHT = 9
GEM_COUNT = 3
START: Position = (1, 1)
EXIT: Position = (HEIGHT - 2, WIDTH - 2)

WALLS: Set[Position] = {
    (1, 4), (1, 5), (1, 6),
    (2, 2), (2, 6), (2, 9),
    (3, 2), (3, 3), (3, 6), (3, 9),
    (4, 6), (4, 7), (4, 8), (4, 9),
    (5, 3), (5, 4), (5, 8),
    (6, 3), (7, 3), (7, 4), (7, 8),
}
MOVES = {
    "w": (-1, 0),
    "a": (0, -1),
    "s": (1, 0),
    "d": (0, 1),
}


def clear_screen() -> None:
    os.system("cls" if os.name == "nt" else "clear")


def is_walkable(position: Position) -> bool:
    row, column = position
    return (
        0 < row < HEIGHT - 1
        and 0 < column < WIDTH - 1
        and position not in WALLS
    )


def draw_map(player: Position, gems: Set[Position], guards: Set[Position]) -> None:
    print("   " + "-" * (WIDTH * 2 - 1))
    for row in range(HEIGHT):
        line = []
        for column in range(WIDTH):
            position = (row, column)
            if position in WALLS or row in (0, HEIGHT - 1) or column in (0, WIDTH - 1):
                symbol = "#"
            elif position == player:
                symbol = "@"
            elif position in guards:
                symbol = "G"
            elif position in gems:
                symbol = "*"
            elif position == EXIT:
                symbol = "E"
            else:
                symbol = "."
            line.append(symbol)
        print("   " + " ".join(line))
    print()


def move_position(position: Position, direction: str) -> Position:
    row, column = position
    delta_row, delta_column = MOVES[direction]
    candidate = (row + delta_row, column + delta_column)
    return candidate if is_walkable(candidate) else position


def move_guards(guards: Set[Position], player: Position) -> Set[Position]:
    moved_guards: Set[Position] = set()
    for guard in guards:
        options = [
            direction
            for direction in MOVES
            if move_position(guard, direction) not in moved_guards
        ]
        random.shuffle(options)
        options.sort(
            key=lambda direction: abs(move_position(guard, direction)[0] - player[0])
            + abs(move_position(guard, direction)[1] - player[1])
        )
        destination = move_position(guard, options[0]) if options else guard
        if destination == player:
            destination = guard
        moved_guards.add(destination)
    return moved_guards


def guard_is_nearby(guards: Set[Position], player: Position) -> bool:
    return any(
        abs(guard[0] - player[0]) + abs(guard[1] - player[1]) == 1
        for guard in guards
    )


def play() -> bool:
    player = START
    gems = {(1, 10), (5, 1), (7, 6)}
    guards = {(2, 4), (6, 10)}
    turns = 0
    last_message = "Find the gems and plan your route carefully."

    while True:
        clear_screen()
        print("=== TREASURE RUN ===")
        print("Collect every gem, then reach the exit before a guard catches you.")
        print("Move: W A S D   |   Quit: Q")
        collected = GEM_COUNT - len(gems)
        score = collected * 100 + max(0, 500 - turns * 10)
        print(f"Gems: {collected}/{GEM_COUNT}   Turns: {turns}   Score: {score}")
        print("Legend: @ you   * gem   G guard   E exit   # wall")
        print()
        draw_map(player, gems, guards)
        print(f"> {last_message}")

        if player in guards:
            print("A guard caught you. The treasure is lost!")
            return False
        if player == EXIT and not gems:
            print(f"You escaped with every gem in {turns} turns. Final score: {score}!")
            return True
        if player == EXIT and gems:
            last_message = "The exit is locked until you collect every gem."

        command = input("Your move: ").strip().lower()
        if command == "q":
            print("You leave the ruins behind. Maybe next time!")
            return False
        if command not in MOVES:
            last_message = "Please enter W, A, S, D, or Q."
            input("Press Enter to continue...")
            continue

        next_position = move_position(player, command)
        if next_position == player:
            last_message = "A wall blocks that path. Choose another direction."
            continue

        player = next_position
        last_message = "You move quietly through the ruins."
        if player in gems:
            last_message = "Gem collected! Keep moving."
        gems.discard(player)
        turns += 1
        guards = move_guards(guards, player)
        if player in guards:
            last_message = "A guard caught you!"
        elif guard_is_nearby(guards, player):
            last_message = "Careful: a guard is one step away!"


def main() -> None:
    while True:
        play()
        answer = input("\nPlay again? (y/n): ").strip().lower()
        if answer != "y":
            print("Thanks for playing Treasure Run!")
            break


if __name__ == "__main__":
    main()
