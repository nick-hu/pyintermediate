#!/usr/bin/env python

import math
import sys
from random import randint

import pygame


class SpaceShip(object):
    def __init__(self, img="ufo.png", pos=[100, 100], size=[50, 75]):
        self.img = pygame.image.load(img)
        self.img = pygame.transform.scale(self.img, size)
        self.rect = pygame.Rect((0, 0), size)
        self.rect.center = pos
        self.vel, self.avel = [0, 0], 5
        self.angle, self.rotation = 0, 0


size = w, h = (500, 500)
screen = pygame.display.set_mode(size)
pygame.display.set_caption("UFO 2")

clock = pygame.time.Clock()

pygame.mouse.set_visible(0)

ship = SpaceShip("ship.png")

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit(0)

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                x_vel = -ship.avel * math.sin(math.radians(ship.angle))
                y_vel = -ship.avel * math.cos(math.radians(ship.angle))
                ship.vel = [x_vel, y_vel]
            if event.key == pygame.K_DOWN:
                x_vel = ship.avel * math.sin(math.radians(ship.angle))
                y_vel = ship.avel * math.cos(math.radians(ship.angle))
                ship.vel = [x_vel, y_vel]

            if event.key == pygame.K_RIGHT:
                ship.rotation = -2
            if event.key == pygame.K_LEFT:
                ship.rotation = 2

        if event.type == pygame.KEYUP:
            ship.vel = [0, 0]
            ship.rotation = 0

    ship.rect = ship.rect.move(*ship.vel)
    ship.rect = ship.rect.clamp(pygame.Rect(0, 0, w, h))
    ship.angle += ship.rotation
    rotufo = pygame.transform.rotate(ship.img, ship.angle)
    rotrect = rotufo.get_rect()
    rotrect.center = ship.rect.center

    screen.fill((0, 0, 0))
    screen.blit(rotufo, rotrect)
    pygame.display.flip()

    clock.tick(60)
