import pygame


def check_win(player, board):
    """Checks if a player has won yet"""

    # Go through every horizontal, vertical, diagonal line of four
    # If they are all the player, return True
    for i in range(len(board)):
        for j in range(len(board[0]) - 4 + 1):
            if (
                board[i][j]
                == board[i][j + 1]
                == board[i][j + 2]
                == board[i][j + 3]
                == player
            ):
                return True

    for i in range(len(board) - 4 + 1):
        for j in range(len(board[0])):
            if (
                board[i][j]
                == board[i + 1][j]
                == board[i + 2][j]
                == board[i + 3][j]
                == player
            ):
                return True

    for i in range(len(board) - 4 + 1):
        for j in range(len(board[0]) - 4 + 1):
            if (
                board[i][j]
                == board[i + 1][j + 1]
                == board[i + 2][j + 2]
                == board[i + 3][j + 3]
                == player
            ):
                return True

            if (
                board[i][j + 3]
                == board[i + 1][j + 2]
                == board[i + 2][j + 1]
                == board[i + 3][j]
                == player
            ):
                return True

    # If there were no sets of 4, return false
    return False


def make_move(player, space, board):
    """Updates the board with a new move"""
    col = int(space) - 1

    # Go from the bottom up, place character in the first open row in that col
    for row in range(5, -1, -1):
        if board[row][col] != "X" and board[row][col] != "O":
            board[row][col] = player
            break
    return


def remove_move(space, board):
    """Removes a move (for recursive backtracking)"""
    col = int(space) - 1

    # Go from the top down, remove the highest character
    for row in range(6):
        if board[row][col] == "X" or board[row][col] == "O":
            board[row][col] = " "
            break
    return


def valid_moves(board):
    """Returns the valid moves in the position"""
    valid = []

    # For each col, if the top space is open it's a valid move
    for col in range(7):
        if board[0][col] == " ":
            valid.append(str(col + 1))
    return valid


def check_draw(board):
    """Checks if there's a draw (wins will be checked first)"""
    # If there are no valid moves and nobody has won, it's a draw
    return len(valid_moves(board)) == 0


def heuristic(player, board):
    """Function to evaluate board position (my own function)"""

    # Store the opponent's character
    opponent = "X" if player == "O" else "O"

    # I start each at a score of 100
    score = 100

    # All horizontal lines
    for i in range(len(board)):
        for j in range(len(board[0]) - 4 + 1):
            # If it's blocked by the opponent, decrease score by 1
            if (
                board[i][j] == opponent
                or board[i][j + 1] == opponent
                or board[i][j + 2] == opponent
                or board[i][j + 3] == opponent
            ):
                score -= 1

            # Otherwise, if you fill 2 add row, if you fill 3 add 3*row
            # Lower rows are prioritized, since they're more immediate threats
            else:
                line_score = (
                    (board[i][j] == player)
                    + (board[i][j + 1] == player)
                    + (board[i][j + 2] == player)
                    + (board[i][j + 3] == player)
                )
                if line_score == 2:
                    score += i + 1
                elif line_score == 3:
                    score += 3 * (i + 1)

    # Vertical
    for i in range(len(board) - 4 + 1):
        for j in range(len(board[0])):
            if (
                board[i][j] == opponent
                or board[i + 1][j] == opponent
                or board[i + 2][j] == opponent
                or board[i + 3][j] == opponent
            ):
                score -= 1
            else:
                line_score = (
                    (board[i][j] == player)
                    + (board[i + 1][j] == player)
                    + (board[i + 2][j] == player)
                    + (board[i + 3][j] == player)
                )
                if line_score == 2:
                    score += i + 2 + 1
                elif line_score == 3:
                    score += 3 * (i + 2 + 1)

    # Diagonals
    for i in range(len(board) - 4 + 1):
        for j in range(len(board[0]) - 4 + 1):
            if (
                board[i][j] == opponent
                or board[i + 1][j + 1] == opponent
                or board[i + 2][j + 2] == opponent
                or board[i + 3][j + 3] == opponent
            ):
                score -= 1
            else:
                line_score = (
                    (board[i][j] == player)
                    + (board[i + 1][j + 1] == player)
                    + (board[i + 2][j + 2] == player)
                    + (board[i + 3][j + 3] == player)
                )
                filled = [
                    (board[i][j] == player),
                    (board[i + 1][j + 1] == player),
                    (board[i + 2][j + 2] == player),
                    (board[i + 3][j + 3] == player),
                ]

                for num in range(3, -1, -1):
                    if not filled[num]:
                        if line_score == 2:
                            score += i + num + 1
                            break
                        elif line_score == 3:
                            score += 3 * (i + num + 1)
                            break

            if (
                board[i][j + 3] == opponent
                or board[i + 1][j + 2] == opponent
                or board[i + 2][j + 1] == opponent
                or board[i + 3][j] == opponent
            ):
                score -= 1
            else:
                line_score = (
                    (board[i][j + 3] == player)
                    + (board[i + 1][j + 2] == player)
                    + (board[i + 2][j + 1] == player)
                    + (board[i + 3][j] == player)
                )
                filled = [
                    (board[i][j + 3] == player),
                    (board[i + 1][j + 2] == player),
                    (board[i + 2][j + 1] == player),
                    (board[i + 3][j] == player),
                ]

                for num in range(3, -1, -1):
                    if not filled[num]:
                        if line_score == 2:
                            score += i + num + 1
                            break
                        elif line_score == 3:
                            score += 3 * (i + num + 1)
                            break

    # Return heuristic score
    return score


def compute_move(player, move, depth, deepest, board):
    """Computes a score for a move in the position (for the computer's use)"""
    # First, make the move
    make_move(player, move, board)

    # Check for wins, -1000 is completely losing, 1000 is completely winning, 0 is drawn
    if check_win("X", board):
        return -1000
    if check_win("O", board):
        return 1000
    if check_draw(board):
        return 0

    # Based on the depth I passed in, if it reaches the deepest I return the heuristic difference
    # Positive difference is winning, negative is losing
    # The greater the difference, the more winning the computer is (according to my function)
    if depth == deepest:
        return heuristic("O", board) - heuristic("X", board)

    # If I'm looking at the computer's side
    if player == "O":
        # For use with min function
        score = 2000

        # For each move X could make, compute it with 1 more depth and then remove the move
        for move in valid_moves(board):
            score = min(score, compute_move("X", move, depth + 1, deepest, board))
            remove_move(move, board)

        # Return the min, implying best possible play for X
        return score

    # If I'm looking at the human's side
    else:
        # For use with max function
        score = -2000

        # Same thing, just max implying best possible computer play
        for move in valid_moves(board):
            score = max(score, compute_move("O", move, depth + 1, deepest, board))
            remove_move(move, board)

        return score


# Start pygame
pygame.init()

# Set up window
win = pygame.display.set_mode((700, 600))
pygame.display.set_caption("Connect Four")

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

    # Keep running till they close game or progress to main loop
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
                    difficulty = 0
                elif 200 <= y < 400:
                    difficulty = 1
                elif 400 <= y <= 600:
                    difficulty = 2

                # Exit the difficulty selector screen
                select_diff = False

        # Start with black screen
        win.fill((0, 0, 0))

        # Based on the mouse, I color in that third
        mouse_x, mouse_y = pygame.mouse.get_pos()

        if 0 <= mouse_y < 200:
            pygame.draw.rect(win, (0, 255, 0), [0, 0, 700, 200])
        elif 200 <= mouse_y < 400:
            pygame.draw.rect(win, (255, 255, 0), [0, 200, 700, 200])
        elif 400 <= mouse_y <= 600:
            pygame.draw.rect(win, (255, 0, 0), [0, 400, 700, 200])

        # Add the centered text for easy, medium, hard
        win.blit(
            easy_text,
            (
                350 - easy_text.get_rect().width / 2,
                100 - easy_text.get_rect().height / 2,
            ),
        )
        win.blit(
            medium_text,
            (
                350 - medium_text.get_rect().width / 2,
                300 - medium_text.get_rect().height / 2,
            ),
        )
        win.blit(
            hard_text,
            (
                350 - hard_text.get_rect().width / 2,
                500 - hard_text.get_rect().height / 2,
            ),
        )

        pygame.display.update()

    # Initialize the board to all spaces
    board = [[" " for x in range(7)] for y in range(6)]

    # Winner will store who won
    winner = -2
    main_loop = True

    # Keep running till game ends
    while main_loop:
        pygame.time.delay(10)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()

            # Make move based on where they click
            if event.type == pygame.MOUSEBUTTONUP:
                x, y = pygame.mouse.get_pos()

                # Their move is evaluated by the x position of the mouse
                player_move = str(x // 100 + 1)

                # If their move is valid
                if player_move in valid_moves(board):

                    # Make the move
                    make_move("X", player_move, board)

                    # Check for game win
                    if check_win("X", board):
                        winner = 1
                        main_loop = False
                        break

                    # Find best computer move, depth of search is difficulty (0, 1, or 2)
                    best_move = ""
                    best_score = -2000

                    for move in valid_moves(board):
                        score = compute_move("O", move, 0, difficulty, board)
                        remove_move(move, board)

                        if score > best_score:
                            best_move = move
                            best_score = score

                    # Make the best move
                    make_move("O", best_move, board)

                    # Check for win and draw now, all spaces could be filled
                    if check_win("O", board):
                        winner = -1
                        main_loop = False
                        break
                    elif check_draw(board):
                        winner = 0
                        main_loop = False
                        break

        # Fill the window with yellow, and draw all the characters/spaces
        win.fill((255, 255, 0))
        for i in range(6):
            for j in range(7):
                color = (0, 0, 0)
                if board[i][j] == "X":
                    color = (255, 0, 0)
                elif board[i][j] == "O":
                    color = (0, 0, 255)

                pygame.draw.circle(win, color, (j * 100 + 50, i * 100 + 50), 45)

        pygame.display.update()

    # Set up font for whoever won
    myfont = pygame.font.SysFont("Comic Sans MS", 60)
    winner_text = None
    if winner == 1:
        winner_text = myfont.render("Congrats! You won!", True, (255, 0, 255))
    elif winner == -1:
        winner_text = myfont.render("Sorry! Computer won!", True, (255, 0, 255))
    else:
        winner_text = myfont.render("Draw!", True, (255, 0, 255))

    myfont = pygame.font.SysFont("Comic Sans MS", 40)
    replay_text = myfont.render("Click anywhere to play again!", True, (255, 0, 255))

    end_screen = True

    # Keep going until they exit or want to play again
    while end_screen:
        pygame.time.delay(10)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()

            # If they click anywhere, I end this loop and start again
            if event.type == pygame.MOUSEBUTTONUP:
                end_screen = False

        # Freeze the end state
        win.fill((255, 255, 0))
        for i in range(6):
            for j in range(7):
                color = (0, 0, 0)
                if board[i][j] == "X":
                    color = (255, 0, 0)
                elif board[i][j] == "O":
                    color = (0, 0, 255)

                pygame.draw.circle(win, (0, 0, 0), (j * 100 + 50, i * 100 + 50), 45, 5)
                pygame.draw.circle(win, color, (j * 100 + 50, i * 100 + 50), 45)

        # Display end messages
        win.blit(
            winner_text,
            (
                350 - winner_text.get_rect().width / 2,
                50 - winner_text.get_rect().height / 2,
            ),
        )
        win.blit(
            replay_text,
            (
                350 - replay_text.get_rect().width / 2,
                150 - replay_text.get_rect().height / 2,
            ),
        )

        pygame.display.update()
