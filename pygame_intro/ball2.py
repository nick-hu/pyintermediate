#!/usr/bin/env python

import sys

import pygame

WHITE = (255, 255, 255)
RED = (255, 0, 0)

size = w, h = (500, 500)
screen = pygame.display.set_mode(size)
pygame.display.set_caption("Ball 2")

clock = pygame.time.Clock()
pos, speed = [100, 100], [6, -8]

while True:

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit(0)

    pos = [sum(i) for i in zip(pos, speed)]
    if pos[0] <= 20 or pos[0] >= 480:
        speed[0] = -speed[0]
    if pos[1] <= 20 or pos[1] >= 480:
        speed[1] = -speed[1]

    screen.fill(WHITE)

    pygame.draw.circle(screen, RED, pos, 20)
    print pos, speed

    pygame.display.flip()  # Update display

    clock.tick(20)  # Frames per second (max. 60)
