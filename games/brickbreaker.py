import pygame

pygame.init()

# Set up window
win = pygame.display.set_mode((500, 500))
pygame.display.set_caption("Brick Breaker")

# Controls the loop
run = True

# Positions for rectangle, ball, and velocity coords
rect = [100, 400, 100, 20]
ball = [200, 200]
vel = [0, 4]

# Holds whether the blocks are in place or broken
blocks = [
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
]

# Go until run is false
while run:
    # Time skip to make the game run faster
    pygame.time.delay(10)

    # If they quit, set run to false
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

    # Move the rectangle based on the arrow keys
    keys = pygame.key.get_pressed()

    if keys[pygame.K_LEFT] and rect[0] > 0:
        rect[0] -= 7
    if keys[pygame.K_RIGHT] and rect[0] < 400:
        rect[0] += 7

    # For each block
    for i in range(3):
        for j in range(10):
            # If the block is still there
            if blocks[i][j] == 1:
                # Delete blocks as the ball is touching them
                if (
                    ball[0] >= j * 50
                    and ball[0] <= j * 50 + 50
                    and ball[1] == i * 50 + 60
                ):
                    blocks[i][j] = 0
                    vel[1] = abs(vel[1])
                if (
                    ball[0] >= j * 50
                    and ball[0] <= j * 50 + 50
                    and ball[1] == i * 50 - 10
                ):
                    blocks[i][j] = 0
                    vel[1] = -1 * abs(vel[1])
                if (
                    ball[0] > j * 50 - 10
                    and ball[0] < j * 50 + 60
                    and ball[1] > i * 50 - 10
                    and ball[1] < i * 50 + 60
                ):
                    blocks[i][j] = 0

                    # Reverse the direction of the ball
                    if ball[0] < j * 50 + 25:
                        vel[0] = -1 * abs(vel[0])
                    else:
                        vel[0] = abs(vel[0])

    # Reverse direction of the ball if it hits the end
    if ball[0] <= 10 or ball[0] >= 490:
        vel[0] = -1 * vel[0]
    if ball[1] <= 10:
        vel[1] = -1 * vel[1]

    # End game if ball goes through bottom
    if ball[1] >= 490:
        run = False

    # Ball bounding off the player's wall
    if ball[1] == 400 and ball[0] >= rect[0] and ball[0] <= rect[0] + 100:
        vel[1] = -1 * vel[1]

        vel[0] = -1 * (((rect[0] + 50) - ball[0]) // 10)

    # Ball moving
    ball[0] += vel[0]
    ball[1] += vel[1]

    # Start with a black window
    win.fill((0, 0, 0))

    # Draw rect and ball in the right positions
    pygame.draw.rect(win, (255, 0, 0), rect)
    pygame.draw.circle(win, (255, 255, 255), ball, 10)

    # Draw all the current blocks and update the display
    for i in range(3):
        for j in range(10):
            if blocks[i][j] == 1:
                pygame.draw.rect(win, (0, 0, 0), (j * 50, i * 50, 50, 50))
                pygame.draw.rect(win, (0, 0, 255), (j * 50 + 5, i * 50 + 5, 40, 40))
    pygame.display.update()

pygame.quit()
