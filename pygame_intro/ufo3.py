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
        self.vel, self.avel = [0, 0], 0
        self.angle, self.rotation = 0, 0


class Bullet(object):
    def __init__(self, pos, vel, size=[20, 20], color=(200, 0, 0)):
        self.rect = pygame.Rect((0, 0), size)
        self.rect.center = pos
        self.vel = vel
        self.color = color

        special = randint(1, 20)
        if special == 1:
            self.vel = [2 * v for v in self.vel]
            self.color = (0, 50, 125)


size = w, h = (750, 750)
screen = pygame.display.set_mode(size)
pygame.display.set_caption("UFO 3")

clock = pygame.time.Clock()

pygame.mouse.set_visible(0)

ship = SpaceShip("ship.png")
bullets, b_avel = [], 10

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit(0)

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                ship.avel = -5
            if event.key == pygame.K_DOWN:
                ship.avel = 5
            if event.key == pygame.K_RIGHT:
                ship.rotation = -2
            if event.key == pygame.K_LEFT:
                ship.rotation = 2

        if event.type == pygame.KEYUP:
            if event.key == pygame.K_UP:
                ship.avel = 0
            if event.key == pygame.K_DOWN:
                ship.avel = 0
            if event.key == pygame.K_RIGHT:
                ship.rotation = 0
            if event.key == pygame.K_LEFT:
                ship.rotation = 0
            if event.key == pygame.K_SPACE:
                angle = -ship.angle
                bx_vel = b_avel * math.sin(math.radians(angle))
                by_vel = -b_avel * math.cos(math.radians(angle))

                b_vel = map(sum, zip([bx_vel, by_vel], ship.vel))
                b = Bullet(ship.rect.center, b_vel)
                bullets.append(b)

    for bullet in bullets:
        bullet.rect = r = bullet.rect.move(*bullet.vel)

    x_vel = ship.avel * math.sin(math.radians(ship.angle))
    y_vel = ship.avel * math.cos(math.radians(ship.angle))
    ship.vel = [x_vel, y_vel]

    ship.rect = ship.rect.move(*ship.vel)
    ship.rect = ship.rect.clamp(pygame.Rect(0, 0, w, h))

    ship.angle += ship.rotation
    rotufo = pygame.transform.rotate(ship.img, ship.angle)
    rotrect = rotufo.get_rect()
    rotrect.center = ship.rect.center

    screen.fill((0, 0, 0))

    for bullet in bullets:
        r, rad = bullet.rect, r.width / 2
        if r.center[0] < -rad or r.center[0] > w + rad:
            bullet.vel = [0, 0]
            continue
        if r.center[1] < -rad or r.center[1] > h + rad:
            bullet.vel = [0, 0]
            continue
        pygame.draw.circle(screen, bullet.color, r.center, rad)

    screen.blit(rotufo, rotrect)

    pygame.display.flip()

    clock.tick(60)
