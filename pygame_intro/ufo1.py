#!/usr/bin/env python

import sys
from random import randint

import pygame


class UFO(object):
    def __init__(self, img="ufo.png", pos=[100, 100], size=[50, 50]):
        self.img = pygame.image.load(img)
        self.img = pygame.transform.scale(self.img, size)
        self.rect = pygame.Rect(pos, size)
        self.vel = [0, 0]


size = w, h = (500, 500)
screen = pygame.display.set_mode(size)
pygame.display.set_caption("UFO 1")

clock = pygame.time.Clock()

pygame.mouse.set_visible(0)

ship = UFO("ufo.png")

while True:

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit(0)

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RIGHT:
                ship.vel[0] = 5
            if event.key == pygame.K_LEFT:
                ship.vel[0] = -5
            if event.key == pygame.K_DOWN:
                ship.vel[1] = 5
            if event.key == pygame.K_UP:
                ship.vel[1] = -5

        if event.type == pygame.KEYUP:
            ship.vel = [0, 0]

    ship.rect = ship.rect.move(*ship.vel)
    ship.rect = ship.rect.clamp(pygame.Rect(0, 0, w, h))

    screen.fill((255, 255, 255))
    screen.blit(ship.img, ship.rect.topleft)
    pygame.display.flip()

    clock.tick(60)
