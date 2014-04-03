#!/usr/bin/env python

import sys

import pygame


class Ship(pygame.sprite.Sprite):
    def __init__(self, img="resources/img/ship.png",
                 pos=[0, 0], size=[50, 75]):
        super(self.__class__, self).__init__()

        self.image = pygame.image.load(img)
        self.image = pygame.transform.scale(self.image, size)

        self.rect = pygame.Rect(pos, self.image.get_size())

        self.vel = [0, 0]


size = w, h = (800, 800)
screen = pygame.display.set_mode(size)
srect = screen.get_rect()
pygame.display.set_caption("2 player UFO")

clock = pygame.time.Clock()

pygame.mouse.set_visible(0)

ents = pygame.sprite.Group()
p1, p2 = Ship(), Ship("resources/img/ufo.png", [100, 100], [120, 70])
ents.add(p1, p2)
maskcol = pygame.sprite.collide_mask

p1_kmove = {pygame.K_RIGHT: [0, 5], pygame.K_LEFT: [0, -5],
            pygame.K_DOWN: [1, 5], pygame.K_UP: [1, -5]}

p2_kmove = {pygame.K_d: [0, 5], pygame.K_a: [0, -5],
            pygame.K_s: [1, 5], pygame.K_w: [1, -5]}

while True:

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit(0)

        if event.type == pygame.KEYDOWN:
            if event.key in p1_kmove:
                d, v = p1_kmove[event.key]
                p1.vel[d] = v

            if event.key in p2_kmove:
                d, v = p2_kmove[event.key]
                p2.vel[d] = v

        if event.type == pygame.KEYUP:
            if event.key in p1_kmove.iterkeys():
                p1.vel = [0, 0]
            else:
                p2.vel = [0, 0]

    for ent in ents:
        oldrect = ent.rect

        ent.rect = ent.rect.move(*ent.vel)
        ent.rect = ent.rect.clamp(srect)

        col = pygame.sprite.spritecollide(ent, ents, False, maskcol)
        col.remove(ent)
        if col:
            ent.rect = oldrect

    screen.fill((0, 0, 0))
    ents.draw(screen)
    pygame.display.flip()

    clock.tick(60)
