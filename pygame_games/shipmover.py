#!/usr/bin/env python

import math
import sys
from random import randint

from serial import Serial
from serial.tools import list_ports
import pygame


class SpaceShip(object):
    def __init__(self, img, pos=[100, 100], size=[50, 75]):
        self.img = pygame.image.load(img)
        self.img = pygame.transform.scale(self.img, size)
        self.rect = pygame.Rect((0, 0), size)
        self.rect.center = pos
        self.vel, self.avel = [0, 0], 0
        self.angle, self.rotation = 0, 0


class UFO(SpaceShip):
    def __init__(self, img=0, pos=[50, 50], size=[100, 100]):
        img = ufo_pics[img]
        super(self.__class__, self).__init__(img, pos, size)


class Bullet(object):
    def __init__(self, pos, vel, size=[15, 15], color=(200, 0, 0)):
        self.rect = pygame.Rect((0, 0), size)
        self.rect.center = pos
        self.vel = vel
        self.color = color


def joystick_angle(x, y):
    x, y = x - 512, -y + 512
    if (abs(x) > 20) or (abs(y) > 20):  # Movement
        return math.degrees(math.atan2(x, y))


ports = [p for p in list_ports.grep(sys.argv[1])]
if not ports:
    raise IOError("Port " + sys.argv[1] + " not found!")
else:
    serial = Serial(ports[0][0], 19200)

pygame.display.init()
info = pygame.display.Info()
size = w, h = info.current_w, info.current_h
screen = pygame.display.set_mode(size, pygame.FULLSCREEN)
pygame.display.set_caption("Ship Mover")

clock = pygame.time.Clock()

pygame.mouse.set_visible(0)

ship = SpaceShip("resources/img/ship.png")
ufo_pics = []
for n in xrange(2):
    ufo_pics.append("resources/img/ufo{0}.png".format(n))
enemies = [UFO()]

pygame.mixer.init()
ship_laser = pygame.mixer.Sound("resources/sound/laser.ogg")
bullets = []
can_fire = False  # Cannot press and hold fire

while True:
    joy = [int(n) for n in serial.readline().split()]
    if not joy or len(joy) != 3:
        joy = [512, 512, 0]
    angle = joystick_angle(joy[0], joy[1])

    if angle is not None:
        ship.avel = 5
        ship.angle = -angle
    else:
        ship.avel = 0

    if joy[2] and can_fire:
        bx_vel = 10 * math.sin(math.radians(-ship.angle))
        by_vel = -10 * math.cos(math.radians(ship.angle))

        b_vel = map(sum, zip([bx_vel, by_vel], ship.vel))
        b = Bullet(ship.rect.center, b_vel)
        bullets.append(b)
        ship_laser.play()
        can_fire = False

    if not joy[2]:
        can_fire = True

    for event in pygame.event.get():
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                sys.exit(0)

    for bullet in bullets:
        bullet.rect = bullet.rect.move(*bullet.vel)

    ship.angle += ship.rotation
    rotufo = pygame.transform.rotate(ship.img, ship.angle)
    rotrect = rotufo.get_rect()
    rotrect.center = ship.rect.center

    x_vel = ship.avel * math.sin(math.radians(-ship.angle))
    y_vel = -ship.avel * math.cos(math.radians(ship.angle))
    ship.vel = [x_vel, y_vel]

    ship.rect = ship.rect.move(*ship.vel)
    ship.rect = ship.rect.clamp(pygame.Rect(0, 0, w, h))

    screen.fill((0, 0, 0))

    for bullet in bullets:
        r, rad = bullet.rect, bullet.rect.width / 2
        if r.center[0] < -rad or r.center[0] > w + rad:
            bullet.vel = [0, 0]
            continue
        if r.center[1] < -rad or r.center[1] > h + rad:
            bullet.vel = [0, 0]
            continue
        pygame.draw.circle(screen, bullet.color, r.center, rad)

    screen.blit(rotufo, rotrect)

    for enemy in enemies:
        screen.blit(enemy.img, enemy.rect)

    pygame.display.flip()

    clock.tick(200)
