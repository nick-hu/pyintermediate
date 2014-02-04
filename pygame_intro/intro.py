#!/usr/bin/env python

import sys

import pygame

BLACK   = (0, 0, 0)
WHITE   = (255, 255, 255)
RED     = (255, 0, 0)
GREEN   = (0, 255, 0)
BLUE    = (0, 0, 255)

size = (700, 500)
screen = pygame.display.set_mode(size)
pygame.display.set_caption("Intro Game")

clock = pygame.time.Clock()
keys = (pygame.K_RIGHT, pygame.K_LEFT, pygame.K_UP, pygame.K_DOWN)
xpos, ypos = 100, 100
speed = 0

while True:
    old_xpos, old_ypos = xpos, ypos

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit(0)

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RIGHT:
                xpos += 10
            elif event.key == pygame.K_LEFT:
                xpos -= 10
            elif event.key == pygame.K_DOWN:
                ypos += 10
            elif event.key == pygame.K_UP:
                ypos -= 10

        if event.type == pygame.KEYUP:
            if event.key in keys:
                speed = 0

    if not (20 <= xpos <= 680):
        xpos = old_xpos
    if not (20 <= ypos <= 480):
        ypos = old_ypos

    screen.fill(BLACK)

    rec = pygame.draw.circle(screen, BLUE, (xpos, ypos), 20)
    print rec, xpos, ypos

    pygame.display.flip()  # Update display

    clock.tick(20)  # Frames per second (max. 60)
