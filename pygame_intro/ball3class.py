#!/usr/bin/env python

import sys
from random import randrange

import pygame

class Ball(object):
    def __init__(self):
        self.pos = [randrange(20, 481), 20]
        self.vel = [randrange(1, 16), randrange(1, 16)]
        self.acc = [0, 5]
        self.color = (randrange(256), randrange(256), randrange(256))

size = w, h = (500, 500)
screen = pygame.display.set_mode(size)
pygame.display.set_caption("Ball 3 Class")

clock = pygame.time.Clock()

balls = []
for ball in xrange(20):
    balls.append(Ball())

while True:

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit(0)

    for ball in balls:
        ball.vel = [sum(i) for i in zip(ball.vel, ball.acc)]
        ball.pos = [sum(i) for i in zip(ball.pos, ball.vel)]

        if ball.pos[0] <= 20 or ball.pos[0] >= 480:
            ball.vel[0] = -ball.vel[0]
        if ball.pos[1] <= 20 or ball.pos[1] >= 480:
            ball.vel[1] = -ball.vel[1]

    screen.fill((255, 255, 255))

    for ball in balls:
        ballrect = pygame.draw.circle(screen, ball.color, ball.pos, 20)

    pygame.display.flip()  # Update display

    clock.tick(20)  # Frames per second (max. 60)