#!/usr/bin/env python

import sys
from random import randint

import pygame


class Ball(object):
    def __init__(self, pos, rad=20):
        self.rad = rad  # Rects drawn from top-left (c- rad)
        self.rect = pygame.Rect([c - rad for c in pos], (2 * rad, 2 * rad))
        self.vel = [randint(-2, 2), randint(-2, 2)]

        self.color = pygame.Color(0, 0, 0)
        self.color.hsva = (randint(0, 359), randint(50, 100), 100, 1)


size = w, h = (500, 500)
screen = pygame.display.set_mode(size)
pygame.display.set_caption("Ball Collision 1")

clock = pygame.time.Clock()

balls = []
for ball in xrange(20):
    balls.append(Ball([randint(40, 460), randint(40, 460)]))

while True:

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit(0)

    rectlist = [b.rect for b in balls]
    rmlist = set([])

    for bn, ball in enumerate(balls):  # Find all collisions
        collidelist = set(ball.rect.collidelistall(rectlist))
        collidelist.remove(bn)
        rmlist |= (collidelist)  # Union of sets

    liveballs = [balls[bn] for bn in xrange(len(balls)) if bn not in rmlist]
    balls = liveballs

    for ball in balls:  # Move balls
        ball.rect = ball.rect.move(*ball.vel)

        if ball.rect.left <= 20 or ball.rect.right >= 480:
            ball.vel[0] = -ball.vel[0]
        if ball.rect.top <= 20 or ball.rect.bottom >= 480:
            ball.vel[1] = -ball.vel[1]

    screen.fill((255, 255, 255))

    for ball in balls:
        pos, rad = ball.rect.center, ball.rad  # Circles are drawn from center
        pygame.draw.circle(screen, ball.color, pos, rad)

    pygame.display.flip()  # Update display

    clock.tick(25)  # Frames per second (max. 60)
