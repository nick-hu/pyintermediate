#!/usr/bin/env python

from os import listdir
import sys
import socket
import cPickle
import math

import pygame


class Entity(pygame.sprite.Sprite):

    entcount = 0

    def __init__(self, sprite="ship.png",
                 pos=[0, 0], size=[50, 75]):
        super(self.__class__, self).__init__()
        self.entid = self.__class__.entcount
        self.__class__.entcount += 1

        self.spname, self.spsize = sprite, size
        self.original = pygame.transform.scale(img[self.spname], self.spsize)
        self.image = self.original

        self.rect = pygame.Rect(pos, self.image.get_size())

        self.vel, self.avel = [0, 0], 0
        self.angle, self.rotation = 0, 0

        self.kmove = [pygame.K_UP, pygame.K_DOWN,
                      pygame.K_LEFT, pygame.K_RIGHT]

    def info(self):
        idict = self.__dict__.copy()

        ignore = ["original", "image", "_Sprite__g", "kmove"]
        for attr in ignore:
            del idict[attr]

        return idict

    def update_sprite(self, imgname, size):
        if (self.spname != imgname) or (self.spsize != size):
            self.original = pygame.transform.scale(img[imgname], size)
            self.image = pygame.transform.rotate(self.original, self.angle)
            pos = self.rect.center
            self.rect = self.image.get_rect()
            self.rect.center = pos

    def control(self, etype, key):
        if etype == pygame.KEYDOWN:
            if key == self.kmove[0]:
                self.avel = -5
            if key == self.kmove[1]:
                self.avel = 5
            if key == self.kmove[2]:
                self.rotation = 2
            if key == self.kmove[3]:
                self.rotation = -2

        if etype == pygame.KEYUP:
            if key in self.kmove[:2]:
                self.avel = 0
            if key in self.kmove[2:]:
                self.rotation = 0

    def move(self):
        x_vel = self.avel * math.sin(math.radians(self.angle))
        y_vel = self.avel * math.cos(math.radians(self.angle))
        self.vel = [x_vel, y_vel]

        oldrect, oldangle, oldimage = self.rect, self.angle, self.image
        self.rect = self.rect.move(*self.vel)
        self.rect = self.rect.clamp(srect)

        self.angle += self.rotation
        self.image = pygame.transform.rotate(self.original, self.angle)
        pos = self.rect.center
        self.rect = self.image.get_rect()
        self.rect.center = pos

        if self.collide(ents):
            self.rect, self.angle, self.image = oldrect, oldangle, oldimage

    def collide(self, entgroup):
        col = pygame.sprite.spritecollide(self, entgroup, False, maskcol)
        col.remove(self)
        if col:
            return True


size = w, h = (500, 500)
screen = pygame.display.set_mode(size)
srect = screen.get_rect()
sidetext = {"s": "Server", "c": "Client"}[sys.argv[1]]
pygame.display.set_caption("Network UFO ({0})".format(sidetext))

clock = pygame.time.Clock()

pygame.mouse.set_visible(0)

img, imgdir = {}, "resources/img"
for img_file in listdir(imgdir):
    img[img_file] = pygame.image.load(imgdir + "/" + img_file)

ents = pygame.sprite.Group()
p1, p2 = Entity(), Entity("ship2.png", [100, 100])
ents.add(p1, p2)
maskcol = pygame.sprite.collide_mask

side = sys.argv[1]
conn = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
conn.setblocking(0)
if side == "s":
    conn.bind(("192.168.1.84", int(sys.argv[2])))
    addr = ()
elif side == "c":
    addr = (sys.argv[2], int(sys.argv[3]))

while True:

    try:
        data, addr = conn.recvfrom(2048)
        data = cPickle.loads(data)
        imgname, size = data.pop("spname"), data.pop("spsize")

        for ent in ents:
            if ent.entid == data["entid"]:
                ent.__dict__.update(data)
                ent.update_sprite(imgname, size)

    except socket.error:
        pass

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit(0)

        if (event.type == pygame.KEYDOWN) or (event.type == pygame.KEYUP):
            if side == "s" and event.key in p1.kmove:
                p1.control(event.type, event.key)
            elif side == "c" and event.key in p2.kmove:
                p2.control(event.type, event.key)

    for ent in ents:
        ent.move()

    if addr:
        try:
            if side == "s":
                conn.sendto(cPickle.dumps(p1.info()), addr)
            elif side == "c":
                conn.sendto(cPickle.dumps(p2.info()), addr)
        except socket.error:
            pass

    screen.fill((0, 0, 0))
    ents.draw(screen)
    pygame.display.flip()

    clock.tick(60)

conn.close()
