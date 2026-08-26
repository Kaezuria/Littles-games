import curses
import random


# =========================
# SETTINGS
# =========================

WIDTH = 50
HEIGHT = 20

START_SPEED = 120
MIN_SPEED = 45


# =========================
# COLORS
# =========================

def setup_colors():
    curses.start_color()
    curses.use_default_colors()

    curses.init_pair(1, curses.COLOR_GREEN, -1)     # Snake
    curses.init_pair(2, curses.COLOR_RED, -1)       # Food
    curses.init_pair(3, curses.COLOR_CYAN, -1)      # Cyan
    curses.init_pair(4, curses.COLOR_YELLOW, -1)    # Score
    curses.init_pair(5, curses.COLOR_MAGENTA, -1)   # Title
    curses.init_pair(6, curses.COLOR_BLUE, -1)      # Border
    curses.init_pair(7, curses.COLOR_WHITE, -1)     # Text


# =========================
# MENU
# =========================

def menu(stdscr):

    curses.flushinp()

    height, width = stdscr.getmaxyx()

    selected = 0

    while True:

        stdscr.clear()

        title = "S N A K E"

        stdscr.addstr(
            height // 2 - 5,
            max(0, (width - len(title)) // 2),
            title,
            curses.color_pair(5) | curses.A_BOLD
        )

        subtitle = "Terminal Edition"

        stdscr.addstr(
            height // 2 - 3,
            max(0, (width - len(subtitle)) // 2),
            subtitle,
            curses.color_pair(3)
        )

        options = [
            "START GAME",
            "QUIT"
        ]

        for i, option in enumerate(options):

            y = height // 2 + i * 2
            x = max(0, (width - len(option)) // 2)

            if i == selected:

                stdscr.addstr(
                    y,
                    x,
                    "> " + option + " <",
                    curses.color_pair(4) | curses.A_BOLD
                )

            else:

                stdscr.addstr(
                    y,
                    x,
                    option,
                    curses.color_pair(7)
                )

        stdscr.addstr(
            height - 2,
            max(0, (width - 25) // 2),
            "↑ ↓ + ENTER",
            curses.color_pair(3)
        )

        stdscr.refresh()

        key = stdscr.getch()

        if key == curses.KEY_UP:
            selected = (selected - 1) % len(options)

        elif key == curses.KEY_DOWN:
            selected = (selected + 1) % len(options)

        elif key in (10, 13, curses.KEY_ENTER):

            if selected == 0:
                return True

            return False

        elif key in (ord("q"), ord("Q")):
            return False


# =========================
# GAME OVER
# =========================

def game_over(stdscr, score, high_score):

    curses.flushinp()

    height, width = stdscr.getmaxyx()

    stdscr.clear()

    title = "GAME OVER"

    stdscr.addstr(
        height // 2 - 4,
        max(0, (width - len(title)) // 2),
        title,
        curses.color_pair(2) | curses.A_BOLD
    )

    stdscr.addstr(
        height // 2 - 1,
        max(0, (width - 20) // 2),
        f"Score: {score}",
        curses.color_pair(4) | curses.A_BOLD
    )

    stdscr.addstr(
        height // 2,
        max(0, (width - 20) // 2),
        f"Best: {high_score}",
        curses.color_pair(3)
    )

    stdscr.addstr(
        height // 2 + 3,
        max(0, (width - 25) // 2),
        "[R] Play Again",
        curses.color_pair(1)
    )

    stdscr.addstr(
        height // 2 + 4,
        max(0, (width - 25) // 2),
        "[M] Main Menu",
        curses.color_pair(4)
    )

    stdscr.addstr(
        height // 2 + 5,
        max(0, (width - 25) // 2),
        "[Q] Quit",
        curses.color_pair(2)
    )

    stdscr.refresh()

    while True:

        key = stdscr.getch()

        if key in (ord("r"), ord("R")):
            return "restart"

        elif key in (ord("m"), ord("M")):
            return "menu"

        elif key in (ord("q"), ord("Q")):
            return "quit"


# =========================
# GAME
# =========================

def play_game(stdscr, high_score):

    curses.flushinp()

    height, width = stdscr.getmaxyx()

    # Make sure the terminal is large enough
    if height < HEIGHT + 7 or width < WIDTH + 2:

        stdscr.clear()

        message = "Terminal is too small!"

        stdscr.addstr(
            height // 2,
            max(0, (width - len(message)) // 2),
            message,
            curses.color_pair(2)
        )

        stdscr.addstr(
            height // 2 + 2,
            max(0, (width - 35) // 2),
            "Please resize your terminal.",
            curses.color_pair(7)
        )

        stdscr.refresh()
        stdscr.getch()

        return high_score, "menu"

    # =========================
    # GAME WINDOW
    # =========================

    game_win = curses.newwin(
        HEIGHT + 2,
        WIDTH + 2,
        5,
        (width - WIDTH - 2) // 2
    )

    # IMPORTANT:
    # This makes arrow keys work correctly.
    game_win.keypad(True)

    # Don't block forever
    game_win.timeout(START_SPEED)

    # =========================
    # SNAKE
    # =========================

    snake = [
        [HEIGHT // 2, WIDTH // 2],
        [HEIGHT // 2, WIDTH // 2 - 1],
        [HEIGHT // 2, WIDTH // 2 - 2]
    ]

    direction = curses.KEY_RIGHT

    # =========================
    # FOOD
    # =========================

    def new_food():

        while True:

            food = [
                random.randint(1, HEIGHT),
                random.randint(1, WIDTH)
            ]

            if food not in snake:
                return food

    food = new_food()

    score = 0
    level = 1

    # =========================
    # FIRST DRAW
    # =========================

    stdscr.clear()

    game_win.clear()

    # Border
    game_win.attron(curses.color_pair(6))
    game_win.border()
    game_win.attroff(curses.color_pair(6))

    # Food
    game_win.addch(
        food[0],
        food[1],
        "*",
        curses.color_pair(2) | curses.A_BOLD
    )

    # Snake
    for i, part in enumerate(snake):

        if i == 0:

            game_win.addch(
                part[0],
                part[1],
                "@",
                curses.color_pair(1) | curses.A_BOLD
            )

        else:

            game_win.addch(
                part[0],
                part[1],
                "o",
                curses.color_pair(1)
            )

    # Header
    stdscr.addstr(
        1,
        2,
        "🐍 SNAKE",
        curses.color_pair(5) | curses.A_BOLD
    )

    stdscr.addstr(
        1,
        width // 2 - 8,
        f"SCORE: {score}",
        curses.color_pair(4) | curses.A_BOLD
    )

    stdscr.addstr(
        1,
        width - 12,
        f"LEVEL: {level}",
        curses.color_pair(3) | curses.A_BOLD
    )

    stdscr.addstr(
        3,
        2,
        "Arrow Keys: Move",
        curses.color_pair(7)
    )

    stdscr.addstr(
        3,
        width - 10,
        "Q: Quit",
        curses.color_pair(2)
    )

    # Double buffering
    stdscr.noutrefresh()
    game_win.noutrefresh()
    curses.doupdate()

    # =========================
    # GAME LOOP
    # =========================

    while True:

        # Get keyboard input
        key = game_win.getch()

        # Quit
        if key in (ord("q"), ord("Q")):
            return high_score, "quit"

        # Directions
        if key == curses.KEY_UP:

            if direction != curses.KEY_DOWN:
                direction = curses.KEY_UP

        elif key == curses.KEY_DOWN:

            if direction != curses.KEY_UP:
                direction = curses.KEY_DOWN

        elif key == curses.KEY_LEFT:

            if direction != curses.KEY_RIGHT:
                direction = curses.KEY_LEFT

        elif key == curses.KEY_RIGHT:

            if direction != curses.KEY_LEFT:
                direction = curses.KEY_RIGHT

        # =========================
        # NEW HEAD
        # =========================

        head = snake[0].copy()

        if direction == curses.KEY_UP:
            head[0] -= 1

        elif direction == curses.KEY_DOWN:
            head[0] += 1

        elif direction == curses.KEY_LEFT:
            head[1] -= 1

        elif direction == curses.KEY_RIGHT:
            head[1] += 1

        # =========================
        # COLLISION
        # =========================

        if (
            head[0] <= 0
            or head[0] >= HEIGHT + 1
            or head[1] <= 0
            or head[1] >= WIDTH + 1
        ):
            break

        if head in snake:
            break

        # =========================
        # MOVE
        # =========================

        snake.insert(0, head)

        ate_food = head == food

        if ate_food:

            score += 1

            level = score // 5 + 1

            speed = max(
                MIN_SPEED,
                START_SPEED - (level - 1) * 10
            )

            game_win.timeout(speed)

            food = new_food()

            game_win.addch(
                food[0],
                food[1],
                "*",
                curses.color_pair(2) | curses.A_BOLD
            )

        else:

            tail = snake.pop()

            # Erase ONLY the old tail
            game_win.addch(
                tail[0],
                tail[1],
                " "
            )

        # =========================
        # DRAW HEAD
        # =========================

        game_win.addch(
            head[0],
            head[1],
            "@",
            curses.color_pair(1) | curses.A_BOLD
        )

        # Draw body
        if len(snake) > 1:

            body = snake[1]

            game_win.addch(
                body[0],
                body[1],
                "o",
                curses.color_pair(1)
            )

        # =========================
        # UPDATE HEADER
        # =========================

        stdscr.addstr(
            1,
            2,
            "🐍 SNAKE",
            curses.color_pair(5) | curses.A_BOLD
        )

        stdscr.addstr(
            1,
            width // 2 - 8,
            f"SCORE: {score}",
            curses.color_pair(4) | curses.A_BOLD
        )

        stdscr.addstr(
            1,
            width - 12,
            f"LEVEL: {level}",
            curses.color_pair(3) | curses.A_BOLD
        )

        # IMPORTANT:
        # No clear() here!
        stdscr.noutrefresh()
        game_win.noutrefresh()
        curses.doupdate()

    # =========================
    # GAME OVER
    # =========================

    if score > high_score:
        high_score = score

    result = game_over(
        stdscr,
        score,
        high_score
    )

    return high_score, result


# =========================
# MAIN
# =========================

def main(stdscr):

    # Hide cursor
    curses.curs_set(0)

    # Enable keyboard
    stdscr.keypad(True)

    # Colors
    setup_colors()

    high_score = 0

    while True:

        # Main menu
        start = menu(stdscr)

        if not start:
            break

        # Play
        high_score, result = play_game(
            stdscr,
            high_score
        )

        if result == "quit":
            break

        elif result == "restart":

            while result == "restart":

                high_score, result = play_game(
                    stdscr,
                    high_score
                )

                if result == "quit":
                    return

        elif result == "menu":
            continue


# =========================
# START
# =========================

if __name__ == "__main__":
    curses.wrapper(main)
