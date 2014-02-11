#!/usr/bin/env python

import sys

import pygame

BLACK = (0, 0, 0)  # RGB colors
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)

size = (700, 500)
screen = pygame.display.set_mode(size)
pygame.display.set_caption("Intro Game")

clock = pygame.time.Clock()
keys = (pygame.K_RIGHT, pygame.K_LEFT, pygame.K_UP, pygame.K_DOWN)
pos, speed = [100, 100], [0, 0]

while True:
    old_pos = pos[:]

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit(0)

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RIGHT:
                speed[0] = 10
            elif event.key == pygame.K_LEFT:
                speed[0] = -10
            elif event.key == pygame.K_DOWN:
                speed[1] = 10
            elif event.key == pygame.K_UP:
                speed[1] = -10

        if event.type == pygame.KEYUP:
            if event.key in keys:
                speed = [0, 0]

    pos = [sum(i) for i in zip(pos, speed)]

    if not (20 <= pos[0] <= 680) or not (20 <= pos[1] <= 480):
        pos = old_pos

    screen.fill(WHITE)

    circle = pygame.draw.circle(screen, RED, pos, 20)
    print pos, speed

    pygame.display.flip()  # Update display

    clock.tick(20)  # Frames per second (max. 60)
