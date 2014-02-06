#!/usr/bin/env python

import sys
from random import randrange

import pygame

size = w, h = (500, 500)
screen = pygame.display.set_mode(size)
pygame.display.set_caption("Ball 3")

clock = pygame.time.Clock()

balls = []
for ball in xrange(20):
    pos = [randrange(20, 481), randrange(20, 481)]
    speed = [randrange(1, 16), randrange(1, 16)]
    color = (randrange(256), randrange(256), randrange(256))
    balls.append([pos, speed, color])

while True:

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit(0)

    for ball in balls:
        ball[0] = [sum(i) for i in zip(ball[0], ball[1])]
        if ball[0][0] <= 20 or ball[0][0] >= 480:
            ball[1][0] = -ball[1][0]
        if ball[0][1] <= 20 or ball[0][1] >= 480:
            ball[1][1] = -ball[1][1]

    screen.fill((255, 255, 255))

    for ball in balls:
        pygame.draw.circle(screen, ball[2], ball[0], 20)

    pygame.display.flip()  # Update display

    clock.tick(20)  # Frames per second (max. 60)