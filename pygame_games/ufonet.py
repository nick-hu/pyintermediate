#!/usr/bin/env python

import sys
import socket
import cPickle

import pygame


class Ship(pygame.sprite.Sprite):
    def __init__(self, img="resources/img/ship.png",
                 pos=[0, 0], size=[50, 75]):
        super(self.__class__, self).__init__()

        self.image = pygame.image.load(img)
        self.image = pygame.transform.scale(self.image, size)

        self.rect = pygame.Rect(pos, self.image.get_size())

        self.vel = [0, 0]

        self.kmove = {pygame.K_RIGHT: [0, 5], pygame.K_LEFT: [0, -5],
                      pygame.K_DOWN: [1, 5], pygame.K_UP: [1, -5]}

    def process_event(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit(0)

            if event.type == pygame.KEYDOWN:
                if event.key in self.kmove:
                    d, v = self.kmove[event.key]
                    self.vel[d] = v

            if event.type == pygame.KEYUP:
                if event.key in self.kmove.iterkeys():
                    self.vel = [0, 0]

    def collide_ents(self):
        oldrect = self.rect

        self.rect = self.rect.move(*ent.vel)
        self.rect = self.rect.clamp(srect)

        col = pygame.sprite.spritecollide(self, ents, False, maskcol)
        col.remove(self)
        if col:
            self.rect = oldrect


size = w, h = (800, 800)
screen = pygame.display.set_mode(size)
srect = screen.get_rect()
pygame.display.set_caption("Network UFO")

clock = pygame.time.Clock()

pygame.mouse.set_visible(0)

ents = pygame.sprite.Group()
p1, p2 = Ship(), Ship("resources/img/ufo.png", [100, 100], [120, 70])
ents.add(p1, p2)
maskcol = pygame.sprite.collide_mask

conn = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
conn.setblocking(False)
if sys.argv[1] == "s":
    conn.bind(("0.0.0.0", int(sys.argv[2])))

while True:

    try:
        data, addr = conn.recvfrom(1024)
        ents = cPickle.loads(data)
    except socket.error:
        pass

    if sys.argv[1] == "s":
        p1.process_event()
    else:
        p2.process_event()


    screen.fill((0, 0, 0))
    ents.draw(screen)
    pygame.display.flip()

    try:
        print [type(i) for i in list(ents)]
        conn.sendto(cPickle.dumps(list(ents)), addr)
    except socket.error:
        pass

    clock.tick(60)
