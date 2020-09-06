import pygame
from random import randint

pygame.init()

# Set up size and title
win = pygame.display.set_mode((500, 500))
pygame.display.set_caption("Pong")

run = True

# Coordinates for player, computer, ball, and ball speed has a randomized y component
player = [450, 175, 20, 150]
computer = [30, 175, 20, 150]
ball = [250, 250]
ball_speed = [5, randint(-1, 1)]


ball_in_play = 0

# Computer hitting ball in randomized place makes it more fun
computer_goal = randint(0, 150)

# Set up the scores
pygame.font.init()
myfont = pygame.font.SysFont("Comic Sans MS", 60)
textsurface1 = myfont.render("0", True, (255, 255, 255))
textsurface2 = myfont.render("0", True, (255, 255, 255))

comp_score = 0
player_score = 0

# Main loop
while run:
    # Time delay to speed up program
    pygame.time.delay(10)

    # If they quit exit
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

    # Check keys, move player
    keys = pygame.key.get_pressed()

    if keys[pygame.K_UP] and player[1] > -50:
        player[1] -= 5
    if keys[pygame.K_DOWN] and player[1] < 400:
        player[1] += 5

    # If the ball is in play
    if ball_in_play == 0:
        # Move the computer towards where it wants to hit the ball (slower than player so it's fair)
        if computer[1] + computer_goal < ball[1]:
            computer[1] += 2
        elif computer[1] + computer_goal > ball[1]:
            computer[1] -= 2

        # If player hits the ball, change its direction based on where the ball was hit
        if player[1] <= ball[1] <= player[1] + 150 and ball[0] == 440:
            ball_speed = [-5, -1 * (((player[1] + 75) - ball[1]) // 20)]

        # Bounce the ball off the top and bottom
        if ball[1] <= 0:
            ball_speed[1] = abs(ball_speed[1])

        if ball[1] >= 500:
            ball_speed[1] = -1 * abs(ball_speed[1])

        # Set the ball's velocity based on where the computer hit it, set a new computer goal
        if computer[1] <= ball[1] <= computer[1] + 150 and ball[0] == 60:
            ball_speed = [5, -1 * (((computer[1] + 75) - ball[1]) // 20)]
            computer_goal = randint(0, 150)

        # If the ball goes off an end, give a point to someone
        if ball[0] >= 500 or ball[0] <= 0:
            if ball[0] >= 500:
                comp_score += 1
                textsurface1 = myfont.render(str(comp_score), True, (255, 255, 255))
            else:
                player_score += 1
                textsurface2 = myfont.render(str(player_score), True, (255, 255, 255))

            # Reset the ball for next point
            ball = [250, 250]
            ball_speed = (
                [5, randint(-1, 1)] if randint(0, 1) == 0 else [-5, randint(-1, 1)]
            )
            player = [450, 175, 20, 150]
            computer = [30, 175, 20, 150]
            ball_in_play = 20

        # Increment the ball speed
        ball[0] += ball_speed[0]
        ball[1] += ball_speed[1]

    else:
        # Ball is not in play
        ball_in_play -= 1

    # Set the window to black
    win.fill((0, 0, 0))

    # Draw the players, middle line, ball, scores, etc
    for num in range(20):
        pygame.draw.rect(win, (255, 255, 255), (248, num * 25, 4, 20))

    pygame.draw.rect(win, (255, 0, 0), player)
    pygame.draw.rect(win, (0, 0, 255), computer)
    pygame.draw.circle(win, (255, 255, 255), ball, 10)
    win.blit(
        textsurface1,
        (
            125 - textsurface1.get_rect().width / 2,
            50 - textsurface1.get_rect().height / 2,
        ),
    )
    win.blit(
        textsurface2,
        (
            375 - textsurface2.get_rect().width / 2,
            50 - textsurface2.get_rect().height / 2,
        ),
    )

    # Update display
    pygame.display.update()

pygame.quit()
