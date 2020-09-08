import pygame
import requests
import json
import random


def update_square(i, j, value, board):
    """Updates the board with a certain value"""
    board[i][j] = value


def check_valid(board):
    """Checks if the board is correct so far"""

    # Check there are no repeated numbers horizontally
    for i in range(9):
        num_set = []
        for j in range(9):
            index = 9 * i + j

            if board[index]:
                if board[index] in num_set:
                    return False
                else:
                    num_set.append(board[index])

    # Vertically
    for j in range(9):
        num_set = []
        for i in range(9):
            index = 9 * i + j

            if board[index]:
                if board[index] in num_set:
                    return False
                else:
                    num_set.append(board[index])

    # For each mini square
    for n in range(9):
        top_corner_i, top_corner_j = n // 3 * 3, n * 3 % 3

        num_set = []
        for i in range(top_corner_i, top_corner_i + 3):
            for j in range(top_corner_j, top_corner_j + 3):
                index = 9 * i + j

                if board[index]:
                    if board[index] in num_set:
                        for newi in range(top_corner_i, top_corner_i + 3):
                            output = ""
                            for newj in range(top_corner_j, top_corner_j + 3):
                                output += str(board[newi * 9 + newj % 9])
                        return False
                    else:
                        num_set.append(board[index])

    # If false wasn't returned, return true
    return True


def solve(index, board):
    """Solves the board, returns solved board"""

    # If we're at the end of the board and it's valid
    if index == 81 and check_valid(board):
        # Return a copy of current board
        return list(board)

    # If the value is already set, return solve from next index
    elif board[index] != 0:
        return solve(index + 1, board)

    # Put in the numbers from 1 to 9
    for num in range(1, 10):
        board[index] = num

        # If the board is valid, return the solve if it exists
        if check_valid(board):
            result = solve(index + 1, board)
            if result is not None:
                return result

        # Backtrack, or set the space to 0
        board[index] = 0


def get_sudoku(difficulty):
    """Retrieve a sudoku puzzle from api"""
    request_url = (
        f"http://www.cs.utep.edu/cheon/ws/sudoku/new/?size=9?level={difficulty}"
    )

    sudoku_dict = json.loads(requests.get(request_url).text)
    sudoku_board = [0 for x in range(81)]

    # Update the board with given values, and return
    for info in sudoku_dict["squares"]:
        sudoku_board[info["y"] * 9 + info["x"] % 9] = info["value"]

    return sudoku_board


# Start pygame
pygame.init()

# Set up window
win = pygame.display.set_mode((450, 600))
pygame.display.set_caption("Sudoku")

run = True

# Keep running till game is closed
while run:
    # Font for difficulty selector
    myfont = pygame.font.SysFont("Comic Sans MS", 60)
    easy_text = myfont.render("EASY", True, (255, 255, 255))
    medium_text = myfont.render("MEDIUM", True, (255, 255, 255))
    hard_text = myfont.render("HARD", True, (255, 255, 255))

    # Difficulty will store the difficulty
    difficulty = -1
    select_diff = True

    while select_diff:
        pygame.time.delay(10)

        # If they quit, exit
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()

            # Choose difficulty based on where they click
            if event.type == pygame.MOUSEBUTTONUP:
                x, y = pygame.mouse.get_pos()

                # Top third is easy, second third is medium, last is hard
                if 0 <= y < 200:
                    difficulty = 1
                elif 200 <= y < 400:
                    difficulty = 2
                elif 400 <= y <= 600:
                    difficulty = 3

                # Exit the difficulty selector screen
                select_diff = False

        # Start with black screen
        win.fill((0, 0, 0))

        # Based on the mouse, I color in that third
        mouse_x, mouse_y = pygame.mouse.get_pos()

        if 0 <= mouse_y < 200:
            pygame.draw.rect(win, (0, 255, 0), [0, 0, 450, 200])
        elif 200 <= mouse_y < 400:
            pygame.draw.rect(win, (255, 255, 0), [0, 200, 450, 200])
        elif 400 <= mouse_y <= 600:
            pygame.draw.rect(win, (255, 0, 0), [0, 400, 450, 200])

        # Add the centered text for easy, medium, hard
        win.blit(
            easy_text,
            (
                225 - easy_text.get_rect().width / 2,
                100 - easy_text.get_rect().height / 2,
            ),
        )
        win.blit(
            medium_text,
            (
                225 - medium_text.get_rect().width / 2,
                300 - medium_text.get_rect().height / 2,
            ),
        )
        win.blit(
            hard_text,
            (
                225 - hard_text.get_rect().width / 2,
                500 - hard_text.get_rect().height / 2,
            ),
        )

        pygame.display.update()

    # Get the puzzle of the chosen difficulty
    board = get_sudoku(difficulty)

    # Create a copy that represents the game
    board_in_play = list(board)

    # Get solution from another copy so original board isn't ruined
    boardcopy = list(board)
    solution = solve(0, boardcopy)

    # Some numbers will be green/red
    colors = [0 for x in range(81)]

    myfont = pygame.font.SysFont("Comic Sans MS", 20)

    main_loop = True

    # Iterate while game is in play
    while main_loop:
        pygame.time.delay(50)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()

            # If they just clicked, update the square and reset color for that square
            if event.type == pygame.MOUSEBUTTONUP:
                x, y = pygame.mouse.get_pos()
                if y <= 450:
                    row, col = y // 50, x // 50
                    if board[row * 9 + col % 9] == 0:
                        board_in_play[row * 9 + col % 9] = (
                            board_in_play[row * 9 + col % 9] + 1
                        ) % 10
                        colors[row * 9 + col % 9] = 0

        keys = pygame.key.get_pressed()

        # If they want a hint, fill an open square and color it green
        if keys[pygame.K_h]:
            open_spaces = []
            for i in range(81):
                if board_in_play[i] == 0:
                    open_spaces.append(i)

            if len(open_spaces) != 0:
                hint_space = random.choice(open_spaces)
                board_in_play[hint_space] = solution[hint_space]
                colors[hint_space] = 1
                # Make a delay so it doesn't spam hints
                pygame.time.delay(100)

        # If they press c, compare to solution and color board
        if keys[pygame.K_c]:
            for num in range(81):
                if board[num] == 0:
                    if board_in_play[num] == solution[num]:
                        colors[num] = 1
                    else:
                        colors[num] = -1

            # If the board is solved, go to end screen
            if board_in_play == solution:
                main_loop = False

        # Draw the lines of the board
        win.fill((0, 0, 0))
        pygame.draw.lines(
            win, (255, 255, 255), True, [(0, 0), (450, 0), (450, 450), (0, 450)], 10
        )

        point_sets = [
            [(150, 0), (150, 450)],
            [(300, 0), (300, 450)],
            [(0, 150), (450, 150)],
            [(0, 300), (450, 300)],
        ]
        for point_set in point_sets:
            pygame.draw.line(win, (255, 255, 255), point_set[0], point_set[1], 10)

        point_sets = [
            [(50, 0), (50, 450)],
            [(100, 0), (100, 450)],
            [(200, 0), (200, 450)],
            [(250, 0), (250, 450)],
            [(350, 0), (350, 450)],
            [(400, 0), (400, 450)],
        ]
        point_sets.extend(
            [[(x[0][1], x[0][0]), (x[1][1], x[1][0])] for x in point_sets]
        )
        for point_set in point_sets:
            pygame.draw.line(win, (255, 255, 255), point_set[0], point_set[1], 5)

        # Draw each number with the correct color
        for num in range(81):
            if board_in_play[num] != 0:
                color = (255, 255, 255)
                if colors[num] == 1:
                    color = (0, 255, 0)
                elif colors[num] == -1:
                    color = (255, 0, 0)

                num_text = myfont.render(str(board_in_play[num]), True, color)
                win.blit(
                    num_text,
                    (
                        num % 9 * 50 + 25 - num_text.get_rect().width / 2,
                        num // 9 * 50 + 25 - num_text.get_rect().height / 2,
                    ),
                )

        # Display instructions at the bottom
        click_text = myfont.render("Click to change numbers", True, (255, 255, 255))
        hint_text = myfont.render("Press H to get a hint", True, (255, 255, 255))
        check_text = myfont.render(
            "Press C to check what you have", True, (255, 255, 255)
        )
        win.blit(click_text, (225 - click_text.get_rect().width / 2, 470))
        win.blit(hint_text, (225 - hint_text.get_rect().width / 2, 510))
        win.blit(check_text, (225 - check_text.get_rect().width / 2, 550))

        pygame.display.update()

    # Set up the fonts for the end screen
    endfont = pygame.font.SysFont("Comic Sans MS", 60)
    solve_text = endfont.render("Solved!", True, (0, 255, 0))

    promptfont = pygame.font.SysFont("Comic Sans MS", 30)
    prompt_text = promptfont.render("Click anywhere to play again!", True, (0, 255, 0))

    end_screen = True

    # Keep going till they exit or want to play again
    while end_screen:
        pygame.time.delay(10)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()

            # If they click anywhere, I end this loop and start again
            if event.type == pygame.MOUSEBUTTONUP:
                end_screen = False

        # Draw lines, but green this time
        win.fill((0, 0, 0))
        pygame.draw.lines(
            win, (0, 255, 0), True, [(0, 0), (450, 0), (450, 450), (0, 450)], 10
        )

        point_sets = [
            [(150, 0), (150, 450)],
            [(300, 0), (300, 450)],
            [(0, 150), (450, 150)],
            [(0, 300), (450, 300)],
        ]
        for point_set in point_sets:
            pygame.draw.line(win, (0, 255, 0), point_set[0], point_set[1], 10)

        point_sets = [
            [(50, 0), (50, 450)],
            [(100, 0), (100, 450)],
            [(200, 0), (200, 450)],
            [(250, 0), (250, 450)],
            [(350, 0), (350, 450)],
            [(400, 0), (400, 450)],
        ]
        point_sets.extend(
            [[(x[0][1], x[0][0]), (x[1][1], x[1][0])] for x in point_sets]
        )
        for point_set in point_sets:
            pygame.draw.line(win, (0, 255, 0), point_set[0], point_set[1], 5)

        # All numbers are green
        for num in range(81):
            if board_in_play[num] != 0:
                color = (0, 255, 0)

                num_text = myfont.render(str(board_in_play[num]), True, color)
                win.blit(
                    num_text,
                    (
                        num % 9 * 50 + 25 - num_text.get_rect().width / 2,
                        num // 9 * 50 + 25 - num_text.get_rect().height / 2,
                    ),
                )

        # Display final text
        win.blit(solve_text, (225 - solve_text.get_rect().width / 2, 450))
        win.blit(prompt_text, (225 - prompt_text.get_rect().width / 2, 525))

        pygame.display.update()
