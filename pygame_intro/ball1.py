#!/usr/bin/env python

import sys

import pygame

WHITE   = (255, 255, 255)
RED     = (255, 0, 0)

size = w, h = (500, 500)
screen = pygame.display.set_mode(size)
pygame.display.set_caption("Ball 1")

clock = pygame.time.Clock()
pos, speed = [100, 100], [3, -4]

while True:

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit(0)

    pos = [sum(i) % 500 for i in zip(pos, speed)]

    screen.fill(WHITE)

    pygame.draw.circle(screen, RED, pos, 20)
    print pos, speed

    pygame.display.flip()  # Update display

    clock.tick(20)  # Frames per second (max. 60)