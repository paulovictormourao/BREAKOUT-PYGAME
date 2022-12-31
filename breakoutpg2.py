import pygame
from pygame.locals import *
import math
from sys import exit


def verify_bricks():
    global brick_list, colors
    for b in brick_list:
            if b.top==250 or b.top==230:
                color = (255, 255, 0)
            elif b.top==210 or b.top==190:
                color = (0, 255, 0)
            elif b.top==170 or b.top==150:
                color = (255, 140, 0)
            else:
                color = (255, 0, 0)
            bricks = pygame.draw.rect(screen, color, b)


pygame.init()

white = (255, 255, 255)
black = (0, 0, 0)

# Screen
sc_width = 700
sc_height = 750
screen = pygame.display.set_mode((sc_width, sc_height))
frames = pygame.time.Clock()


# Draw paddle
pd_height = 30
pd_width = 150
x_pd = sc_width/2 - pd_width/2


# Draw ball
radius = 12
y_ball = sc_height/2
x_ball = sc_width/2
pygame.draw.circle(screen, white, (x_ball, y_ball), radius)
yd = 1
xd = 0


# Bricks
x_list = [30, 79, 128, 177, 226, 275, 324, 373, 422, 471, 520, 569, 618, 617]
y_list = [250, 230, 210, 190, 170, 150, 130,  110]
brick_list = []

for x in range(14):
    for y in range(8):
        bricks = pygame.Rect(x_list[x], y_list[y], 44, 16)
        brick_list.append(bricks)

while True:

    # Support Lines
    pygame.draw.line(screen, white, (350, 750), (350, 0))
    pygame.draw.line(screen, white, (0, 375), (700, 375))

    # User
    for event in pygame.event.get():
        # Quits if you close the window
        if event.type == QUIT:
            pygame.display.quit()
            exit()

    if pygame.key.get_pressed()[K_LEFT]:
        if x_pd > 0:
            x_pd += -2
        else:
            x_pd = 0
    if pygame.key.get_pressed()[K_RIGHT]:
        if x_pd < sc_width - pd_width:
            x_pd += 2
        else:
            x_pd = sc_width - pd_width

    # Draw
    paddle = pygame.draw.rect(screen, white, (x_pd, 680, pd_width, pd_height))
    ball = pygame.draw.circle(screen, white, (x_ball, y_ball), radius)
    verify_bricks()

    # Ball move
    y_ball += yd
    x_ball += xd

    # Collision with the paddle
    if paddle.colliderect(ball):
        yd = -1
        if x_pd + 75 - x_ball <= 75:
            xd = 2 * math.cos(x_pd + 75 - x_ball)
        else:
            xd = 2 * math.cos(x_pd + 75 - x_ball)

    # Collision with the roof
    if y_ball <= 0 + radius:
        yd = 1

    # Collision with the left wall
    if x_ball <= 0 + radius:
        xd = 1

    # Collision with the right wall
    if x_ball >= sc_width - radius:
        xd = -1

    # Collision with the flor
    if y_ball >= sc_height - radius:
        x_ball = sc_width/2
        y_ball = sc_height/2
        xd = 0

    # Collisions with the bricks
    for brick in brick_list:
        if ball.colliderect(brick):
            brick_list.remove(brick)
            yd = 1

    # Screen in loop
    frames.tick(300)
    pygame.display.update()
    screen.fill(black)
