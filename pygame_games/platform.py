#!/usr/bin/env python

import sys

import pygame


class Player(object):
    def __init__(self, pos, size):
        self.rect = pygame.Rect(pos, size)
        self.vel, self.acc = [0, 0], [0, GRAVITY]

        self.duck = False

    def draw(self):
        self.rect = self.rect.clamp(pygame.Rect(0, 0, w, h))
        pygame.draw.rect(screen, BLACK, self.rect)


class Chunk(object):
    def __init__(self, pos, size):
        self.rect = pygame.Rect(pos, size)
        self.vel, self.acc = [0, 0], [0, 0]

    def draw(self):
        self.rect = self.rect.clamp(pygame.Rect(0, 0, w, h))
        pygame.draw.rect(screen, BROWN, self.rect)

WHITE = (255, 255, 255)
BROWN = (60, 30, 0)
BLACK = (0, 0, 0)

GRAVITY = 2

ents = {"player": Player((0, 700), (20, 50))}
ents["block"] = Chunk((100, 680), (200, 10))

size = w, h = (750, 750)
screen = pygame.display.set_mode(size)
pygame.display.set_caption("Platform")

clock = pygame.time.Clock()

while True:
    pl = ents["player"]

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit(0)

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                if pl.rect.bottom == h and not pl.duck:
                    pl.vel[1] = -20
            if event.key == pygame.K_DOWN:
                pl.rect.height -= 20
                pl.vel[0] = 0
                pl.duck = True
            if event.key == pygame.K_RIGHT:
                if pl.duck:
                    pl.vel[0] = 1
                else:
                    pl.vel[0] = 3
            if event.key == pygame.K_LEFT:
                if pl.duck:
                    pl.vel[0] = -1
                else:
                    pl.vel[0] = -3

        if event.type == pygame.KEYUP:
            if event.key == pygame.K_DOWN:
                pl.rect.height += 20
                pl.duck = False
            if event.key == pygame.K_RIGHT:
                pl.vel[0] = 0
            if event.key == pygame.K_LEFT:
                pl.vel[0] = 0


    screen.fill(WHITE)

    for ent in ents.itervalues():
        r = ent.rect

        c = r.collidelistall([e.rect for e in ents.values()])
        r.left = r.left + ent.vel[0] + 0.5 * ent.acc[0]
        r.top = r.top + ent.vel[1] + 0.5 * ent.acc[1]
        ent.vel[0] += ent.acc[0]
        ent.vel[1] += ent.acc[1]
        ent.draw()

    pygame.display.flip()
    clock.tick(60)
