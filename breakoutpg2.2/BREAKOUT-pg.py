import pygame
from pygame.locals import *
import math
from sys import exit


def verify_bricks():
    global brick_list, colors
    for b in brick_list:
            if b.top==250 or b.top==230:
                color = yellow
            elif b.top==210 or b.top==190:
                color = green
            elif b.top==170 or b.top==150:
                color = orange
            else:
                color = red
            bricks = pygame.draw.rect(screen, color, b)


def draw_bricks():
    for x in range(14):
        for y in range(8):
            bricks = pygame.Rect(x_list[x], y_list[y], 41, 14)
            brick_list.append(bricks)

pygame.init()
# score and balls
score = 0
balls = 1
end = False

# colors
white = (255, 255, 255)
black = (0, 0, 0)
gray = (180,180,180)
red = (210, 0, 0)
yellow = (230, 230, 0)
orange = (240, 110, 0)
green = (0, 100, 0)


# Screen
sc_width = 692
sc_height = 761
screen = pygame.display.set_mode((sc_width, sc_height))
border_y = 7
border_x = 19
frames = pygame.time.Clock()
font = pygame.font.SysFont('arial', 50, True, False)

# Draw paddle
pd_height = 20
pd_width = 100
x_pd = sc_width/2 - pd_width/2

# Draw ball
radius = 12
y_ball = sc_height/2
x_ball = sc_width/2 + radius
pygame.draw.rect(screen, white, (x_ball, y_ball, radius, radius))
yd = 1
xd = 0

# Bricks
x_list = [7, 56, 105, 154, 203, 252, 301, 350, 399, 448, 497, 546, 595, 644]
y_list = [250, 230, 210, 190, 170, 150, 130, 110]
brick_list = []
draw_bricks()

while True:

    if len(brick_list):
        # Text
        score_text = f'{score}'
        score_format = font.render(score_text, False, gray )
        screen.blit(score_format, (90, 30))
        balls_text = f'{balls}'
        balls_format = font.render(balls_text, False, gray)
        screen.blit(balls_format, (575,30))


        # User
        for event in pygame.event.get():
            # Quits if you close the window
            if event.type == QUIT:
                pygame.display.quit()
                exit()

        if pygame.key.get_pressed()[K_LEFT]:
            if x_pd > border_y:
                x_pd += -4
            else:
                x_pd = border_y
        if pygame.key.get_pressed()[K_RIGHT]:
            if x_pd < sc_width - pd_width - border_y:
                x_pd += 4
            else:
                x_pd = sc_width - pd_width - border_y

        # Draw
        paddle = pygame.draw.rect(screen, (0,0, 240), (x_pd, 700, pd_width, pd_height))
        ball = pygame.draw.rect(screen, white, (x_ball, y_ball, radius, radius))

        # Border
        # Gray
        pygame.draw.rect(screen, gray, (0, 0, sc_width, border_x))
        pygame.draw.rect(screen, gray, (0, 0, border_y, sc_height))
        pygame.draw.rect(screen, gray, (sc_width - border_y, 0, border_y, sc_height))
        # Blue
        pygame.draw.rect(screen, (0,0,240), (0,700, border_y, 30))
        pygame.draw.rect(screen, (0, 0, 240), (sc_width - border_y, 700, border_y, 30))
        # Yellow
        pygame.draw.rect(screen, yellow, (0, 227, border_y, 38))
        pygame.draw.rect(screen, yellow, (sc_width - border_y, 227, border_y, 38))
        # Green
        pygame.draw.rect(screen, green, (0, 187, border_y, 40))
        pygame.draw.rect(screen, green, (sc_width - border_y, 187, border_y, 40))
        # Orange
        pygame.draw.rect(screen, orange, (0, 147, border_y, 40))
        pygame.draw.rect(screen, orange, (sc_width - border_y, 147, border_y, 40))
        # Red
        pygame.draw.rect(screen, red, (0, 110, border_y, 40))
        pygame.draw.rect(screen, red, (sc_width - border_y, 110, border_y, 40))

        # Ball move
        y_ball += yd
        x_ball += xd

        verify_bricks()

        # Collision with the paddle
        if paddle.colliderect(ball):
            yd = -1 * abs(yd)
            if abs(x_pd - x_ball) <= 50:
                xd = -1.6 -  0.8 * math.sin(x_pd - x_ball)
            else:
                xd =  1.6 + 0.8* math.sin(x_pd - x_ball)
            pygame.mixer.music.load('beep.mp3')
            pygame.mixer.music.play()

        # Collision with the roof
        if y_ball <= border_x + radius:
            yd *= -1
            xd *= 1.2
            pygame.mixer.music.load('beep.mp3')
            pygame.mixer.music.play()

        # Collision with the left wall
        if x_ball <=  radius + border_y:
            xd *= -1
            pygame.mixer.music.load('beep.mp3')
            pygame.mixer.music.play()

        # Collision with the right wall
        if x_ball >= sc_width - radius - border_y:
            xd *= -1
            pygame.mixer.music.load('beep.mp3')
            pygame.mixer.music.play()

        # Collision with the flor
        if y_ball >= sc_height - radius:
            x_ball = sc_width/2
            y_ball = sc_height/2
            balls += 1
            xd = 0
            yd = 1

        # Collisions with the bricks
        for brick in brick_list:
            if ball.colliderect(brick):

                if brick.top==250 or brick.top==230:
                    score += 1
                    yd *= -1
                elif brick.top==210 or brick.top==190:
                    score += 3
                    yd *= -1.3
                elif brick.top==170 or brick.top==150:
                    score += 5
                    yd *= -1.5
                else:
                    score += 7
                    yd *= -1.6

                if not y_ball < brick.top +12 and y_ball > brick.top + 1:
                    xd = xd
                else:
                    if x_ball <= brick.left:
                        xd *= -1 * abs(xd)
                    elif x_ball >= brick.left + 20:
                        xd = abs(xd)

                brick_list.remove(brick)
                pygame.mixer.music.load('beep2.mp3')
                pygame.mixer.music.play()

        # Max velocity
        if yd < -1.9:
            yd = -1.9
        elif yd > 1.9:
            yd = 1.9

        if xd < -1.9:
            xd = -1.9
        elif xd > 1.9:
            xd = 1.9

        if balls == 4:
            end = True
            while end:
                screen.fill(black)
                lose_text = 'game over'
                lose_format = font.render(lose_text, False, gray)
                screen.blit(lose_format, (sc_width/2 - 135, sc_height / 2 - 40))
                for event in pygame.event.get():
                    if event.type == QUIT:
                        pygame.display.quit()
                        exit()
                pygame.display.update()

        # Screen in loop
        frames.tick(200)
        pygame.display.update()
        screen.fill(black)

    else:
        end = True
        while end:
            screen.fill(black)
            win_text = 'you win!!'
            win_format = font.render(win_text, False, gray)
            screen.blit(win_format, (sc_width/2 - 140, sc_height/2 - 40))
            for event in pygame.event.get():
                if event.type == QUIT:
                    pygame.display.quit()
                    exit()
            pygame.display.update()
