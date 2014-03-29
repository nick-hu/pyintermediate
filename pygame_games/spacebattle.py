#!/usr/bin/env python

import math
import sys
from random import randint, normalvariate

from serial import Serial
from serial.tools import list_ports
import pygame


class SpaceShip(object):
    def __init__(self, img, pos, size=[50, 75]):
        self.img = pygame.image.load(img)
        self.img = pygame.transform.scale(self.img, size)
        self.rect = pygame.Rect((0, 0), size)
        self.rect.center = pos
        self.vel, self.avel = [0, 0], 0
        self.angle = 0

        self.health, self.max_health = 100, 100
        self.bvel, self.bdmg = 10, 5


class UFO(SpaceShip):
    def __init__(self, img, pos, size=[120, 70]):
        super(self.__class__, self).__init__(img, pos, size)
        self.fire_rate, self.inacc = 50, 30

    def move(self):
        self.rect = self.rect.move(*self.vel)
        if (self.rect.left < 0) or (self.rect.right > w):
            self.vel[0] = -self.vel[0]
        if (self.rect.top < 0) or (self.rect.bottom > h):
            self.vel[1] = -self.vel[1]

    def fire(self, scenter):
        if (ticks % self.fire_rate) != 0:
            return
        oopsx = randint(-self.inacc, self.inacc)
        oopsy = randint(-self.inacc, self.inacc)

        ufo_x, ufo_y = self.rect.center
        dx, dy = scenter[0] - ufo_x + oopsx, ufo_y - scenter[1] + oopsy
        angle = math.atan2(dx, dy)

        bx_vel = self.bvel * math.sin(angle)
        by_vel = -self.bvel * math.cos(angle)
        b_vel = [bx_vel, by_vel]

        b = Bullet(self.rect.center, b_vel, color=(0, 200, 0))
        bullets.append(b)
        ufo_laser.play()
        return True  # Signal that a bullet has been fired


class Bullet(object):
    def __init__(self, pos, vel, size=[15, 15], color=(200, 0, 0)):
        self.rect = pygame.Rect((0, 0), size)
        self.rect.center = pos
        self.vel = vel
        self.color = color

        self.damage, self.enemy, self.homing = 5, True, False
        self.ptype = 0


class PowerUp(Bullet):
    def __init__(self, pos, size=[10, 10], ptype=1):
        vel = [0, 0]
        while vel == [0, 0]:
            vel = [randint(-1, 1), randint(-1, 1)]

        if ptype == 1:  # Scoreball
            color = (255, 255, 0)
        if ptype == 2:  # Healthball
            color = (255, 50, 255)
        if ptype == 3:  # Critball
            color = (0, 0, 255)
        if ptype == 4:  # Invulnball
            color = (125, 55, 215)
        if ptype == 5:  # Homingball
            color = (255, 125, 0)
        if ptype == 6:  # Speedball
            color = (0, 205, 255)

        super(self.__class__, self).__init__(pos, vel, size, color)
        self.ptype = ptype


def joystick_angle(x, y):
    x, y = x - 512, -y + 512
    if (abs(x) > 20) or (abs(y) > 20):  # Movement
        return math.degrees(math.atan2(x, y))


def render_text(font, text, pos, color):
    lines = text.split("\n")
    center_x, center_y = pos

    for l in lines:
        ftext = font.render(l, 1, color)
        frect = pygame.Rect((0, 0), ftext.get_rect().size)
        frect.center = center_x, center_y
        screen.blit(ftext, frect)
        center_y += font.get_linesize()


def draw_ebar(start, time, duration, botleft, color):
        effpercent = 100 - 100 * (time - start) / duration
        effrect = pygame.Rect(0, 0, effpercent, 10)
        effrect.bottomleft = botleft
        pygame.draw.rect(screen, color, effrect)


ports = [p for p in list_ports.grep(sys.argv[1])]
if not ports:
    raise IOError("Port " + sys.argv[1] + " not found!")
else:
    serial = Serial(ports[0][0], 19200)

pygame.init()

info = pygame.display.Info()
size = w, h = info.current_w, info.current_h
screen = pygame.display.set_mode(size, pygame.FULLSCREEN)
pygame.display.set_caption("Space Battle")
srect = screen.get_rect()

pygame.mouse.set_visible(0)

ship = SpaceShip("resources/img/ship.png", [randint(0, w), randint(0, h)])
ship.rect = ship.rect.clamp(srect)
enemies = []

ship_laser = pygame.mixer.Sound("resources/sound/laser.ogg")
ship_laser.set_volume(0.25)
ufo_laser = pygame.mixer.Sound("resources/sound/ulaser.ogg")
ship_laser.set_volume(0.5)
hitsound = pygame.mixer.Sound("resources/sound/hit.ogg")
hitsound.set_volume(0.25)
boom = pygame.mixer.Sound("resources/sound/explosion.ogg")
coinsound = pygame.mixer.Sound("resources/sound/coin.ogg")
pygame.mixer.music.load("resources/sound/space.ogg")
pygame.mixer.music.set_volume(0.5)
pygame.mixer.music.play(-1)

bullets = []
hits, shots = 0, 0
crit_start, invuln_start, homing_start, speedy_start = 0, 0, 0, 0
can_fire = False  # Cannot press and hold fire
score, wave = 0, 0

dfont = pygame.font.Font("resources/fonts/mc.ttf", 24)

clock = pygame.time.Clock()
ticks, paused, unpause = 0, False, False
while True:
    ### PAUSE/EXIT ###

    for event in pygame.event.get():
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                sys.exit(0)
            if event.key == pygame.K_p and ship.health > 0:
                paused = True

    while paused:
        unpause = False
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    sys.exit(0)
                if event.key == pygame.K_p:
                    unpause, paused = True, False

        pausetext = "GAME PAUSED\nPress p to resume"
        render_text(dfont, pausetext, srect.center, (255, 255, 255))
        pygame.display.flip()

        serial.readline()  # Keep serial port active
        if unpause:
            break

    ## WAVES ###

    if not enemies and ship.health > 0:
        wave, wstart = wave + 1, ticks
        ship.health = max(ship.max_health, ship.health)
        score += (wave - 1) * 100

        vbound = min(10, wave / 2)
        frate = max(1, 50 - wave)
        inacc = max(0, 50 - wave)
        uhealth = 100 + 10 * wave

        if wave % 10 == 0:  # Boss
            pos = [randint(0, w), randint(0, h)]
            ufoboss = UFO("resources/img/ufoboss.png", pos, [240, 140])
            ufoboss.rect = ufoboss.rect.clamp(srect)
            ufoboss.vel = [0, 0]
            while ufoboss.vel == [0, 0]:
                ufoboss.vel = [randint(-1, 1), randint(-1, 1)]
            ufoboss.fire_rate, ufoboss.inacc = frate * 2, 0
            ufoboss.health, ufoboss.max_health = uhealth * 5, uhealth * 5
            enemies.append(ufoboss)
            continue

        for _ in xrange(wave / 5 + 1):
            pos = [randint(0, w), randint(0, h)]
            v = [randint(-vbound, vbound), randint(-vbound, vbound)]
            ufo = UFO("resources/img/ufo.png", pos)
            ufo.rect = ufo.rect.clamp(srect)
            ufo.vel, ufo.fire_rate, ufo.inacc = v, frate, inacc
            ufo.health, ufo.max_health = uhealth, uhealth
            enemies.append(ufo)

    if ship.health > ship.max_health and ticks % 50 == 0:
        ship.health -= 1

    ### POWERUPS ###

    if randint(1, 500) == 1:
        bullets.append(PowerUp([randint(0, w), randint(0, h)], ptype=1))
    if randint(1, 1500) == 1:
        bullets.append(PowerUp([randint(0, w), randint(0, h)], ptype=2))
    if randint(1, 4000) == 1:
        bullets.append(PowerUp([randint(0, w), randint(0, h)], ptype=3))
    if randint(1, 5000) == 1:
        bullets.append(PowerUp([randint(0, w), randint(0, h)], ptype=4))
    if randint(1, 4500) == 1:
        bullets.append(PowerUp([randint(0, w), randint(0, h)], ptype=5))
    if randint(1, 3500) == 1:
        bullets.append(PowerUp([randint(0, w), randint(0, h)], ptype=6))

    if (ticks - crit_start) > 500:
        crit_start = 0
    if (ticks - invuln_start) > 700:
        invuln_start = 0
    if (ticks - homing_start) > 700:
        homing_start = 0
    if (ticks - speedy_start) > 1000:
        speedy_start = 0

    ### CONTROLLER ###

    try:
        joy = [int(n) for n in serial.readline().split()]
        assert len(joy) == 3
    except:
        joy = [512, 512, 0]
    angle = joystick_angle(joy[0], joy[1])

    if angle is not None:
        ship.avel = 10 if speedy_start else 5
        ship.angle = -angle
    else:
        ship.avel = 0

    if joy[2] and can_fire:
        bx_vel = ship.bvel * math.sin(math.radians(-ship.angle))
        by_vel = -ship.bvel * math.cos(math.radians(ship.angle))
        if crit_start and not homing_start:
            bx_vel, by_vel = 2 * bx_vel, 2 * by_vel

        b_vel = map(sum, zip([bx_vel, by_vel], ship.vel))
        b = Bullet(ship.rect.center, b_vel)
        if crit_start:
            b.color, b.damage = (0, 0, 200), 10 * ship.bdmg
        if homing_start:
            b.color, b.damage = (255, 125, 0), 2 * ship.bdmg
            b.homing, b.birth = True, ticks

        b.enemy = False
        bullets.append(b)
        ship_laser.play()
        shots += 1
        can_fire = False

    if not joy[2]:
        can_fire = True

    ### MOVEMENT ###

    for bullet in bullets:
        if bullet.homing:
            if (ticks - bullet.birth) > 700:
                bullets.remove(bullet)
            elif (ticks - bullet.birth) > 5:
                bx, by = bullet.rect.center
                min_ufo_dist = 0
                if not enemies:
                    bullets.remove(bullet)
                    continue
                for u in enemies:
                    dx = u.rect.center[0] - bx
                    dy = by - u.rect.center[1]
                    dist = math.hypot(dx, dy)
                    if (not min_ufo_dist) or (dist < min_ufo_dist):
                        min_ufo_dist, min_ufo = dist, u

                ucenter = min_ufo.rect.center
                dx, dy = ucenter[0] - bx, by - ucenter[1]
                angle = math.atan2(dx, dy)

                bx_vel = 5 * math.sin(angle)
                by_vel = -5 * math.cos(angle)
                bullet.vel = [bx_vel, by_vel]

        bullet.rect = bullet.rect.move(*bullet.vel)

    rotufo = pygame.transform.rotate(ship.img, ship.angle)
    rotrect = rotufo.get_rect()
    rotrect.center = ship.rect.center

    x_vel = ship.avel * math.sin(math.radians(-ship.angle))
    y_vel = -ship.avel * math.cos(math.radians(ship.angle))
    ship.vel = [x_vel, y_vel]

    ship.rect = ship.rect.move(*ship.vel)
    ship.rect = ship.rect.clamp(srect)

    for enemy in enemies:
        if ticks - wstart > 75:
            fired = enemy.fire(ship.rect.center)
            if fired and wave % 10 == 0:
                bullets[-1].rect.size = [20, 20]
                if randint(1, 20) == 1:
                    bullets[-1].damage = 2 * bullets[-1].damage
                    bullets[-1].color = (0, 200, 150)
                    enemy.health += bullets[-1].damage
        enemy.move()

    ### COLLISION ###

    del_bullets = []

    hit = ship.rect.collidelistall(bullets)
    for b in hit:
        bullet = bullets[b]
        if bullet.enemy and ship.health > 0:
            if bullet.ptype:  # Powerup
                ptype = bullet.ptype
                if ptype == 1:
                    score += 100
                elif ptype == 2:
                    mh = ship.max_health
                    ship.health += int(normalvariate(0.35 * mh, 0.05 * mh))
                    ship.health = min(ship.health, int(mh * 1.5))
                elif ptype == 3:
                    crit_start = ticks
                elif ptype == 4:
                    invuln_start = ticks
                elif ptype == 5:
                    homing_start = ticks
                elif ptype == 6:
                    speedy_start = ticks
                coinsound.play()
            else:  # Bullet
                if invuln_start:
                    bullet.vel = [-n for n in bullet.vel]
                    bullet.color = (200, 0, 0)
                    bullet.enemy = False
                    continue
                ship.health -= bullet.damage
                score = max(0, score - bullet.damage)
                hitsound.play()
                if ship.health <= 0:
                    ship.health, enemies = 0, []
                    boom.play()
                    pygame.mixer.music.fadeout(15000)
                    ship.img = pygame.image.load("resources/img/null.png")
            del_bullets.append(bullet)

    for enemy in enemies:
        hit = enemy.rect.collidelistall(bullets)
        for b in hit:
            bullet = bullets[b]
            if not bullet.enemy:
                del_bullets.append(bullet)
                enemy.health -= bullet.damage
                hits += 1
                score += bullet.damage
                hitsound.play()
                if enemy.health <= 0 and enemy in enemies:
                    enemies.remove(enemy)
                    sballs = wave if wave % 10 == 0 else wave / 10
                    for _ in xrange(randint(1, sballs + 1)):
                        bullets.append(PowerUp(enemy.rect.center, ptype=1))
                    for _ in xrange(randint(1, enemy.max_health / 100)):
                        bullets.append(PowerUp(enemy.rect.center, ptype=2))
                    if wave % 10 == 0:
                        for b in bullets:
                            b.vel = [0, 0]
                            while b.vel == [0, 0]:
                                b.vel = [randint(-3, 3), randint(-3, 3)]
                        ship.max_health += 50
                    boom.play()

    bullets = [b for b in bullets if b not in del_bullets]

    ### DRAWING ###

    screen.fill((0, 0, 0))

    screen.blit(rotufo, rotrect)

    for enemy in enemies:
        er = enemy.rect
        hpercent = (float(enemy.health) / enemy.max_health)
        hw = hpercent * er.width
        if 0.2 <= hpercent < 0.5:
            color = (255, 255, 50)
        elif 0 < hpercent < 0.2:
            color = (255, 0, 0)
        else:
            color = (0, 200, 0)
        hrect = pygame.Rect(er.left, er.top - 10, hw, 5)
        pygame.draw.rect(screen, color, hrect)
        screen.blit(enemy.img, enemy.rect)

    for bullet in bullets:
        rad = bullet.rect.width / 2
        if not srect.contains(bullet.rect):  # Bullet off-screen
            bullets.remove(bullet)
        pygame.draw.circle(screen, bullet.color, bullet.rect.center, rad)

    if crit_start:
        draw_ebar(crit_start, ticks, 500.0, [10, h - 55], (0, 0, 255))
    if invuln_start:
        draw_ebar(invuln_start, ticks, 700.0, [10, h - 40], (125, 55, 215))
    if homing_start:
        draw_ebar(homing_start, ticks, 700.0, [10, h - 25], (255, 125, 0))
    if speedy_start:
        draw_ebar(speedy_start, ticks, 1000.0, [10, h - 10], (0, 205, 255))

    hp = "HP: {0}/{1}".format(ship.health, ship.max_health)
    if ship.health > ship.max_health:
        dfont.set_bold(True)
    health = dfont.render(hp, 1, (255, 0, 0))
    hrect = health.get_rect()
    hrect.right = w - 20
    screen.blit(health, hrect)
    dfont.set_bold(False)

    if shots:
        p = min(round(100 * (float(hits) / shots), 1), 100.0)
    else:
        p = "---.-"
    acc = "ACC: {0}%".format(p)
    accuracy = dfont.render(acc, 1, (0, 255, 0))
    arect = accuracy.get_rect()
    arect.topright = [w - 20, 30]
    screen.blit(accuracy, arect)

    sc = "SCORE: {0}".format(score)
    stext = dfont.render(sc, 1, (255, 255, 0))
    screct = stext.get_rect()
    screct.left = 10
    screen.blit(stext, screct)

    wv = "WAVE {0}".format(wave)
    wtext = dfont.render(wv, 1, (255, 125, 0))
    wrect = wtext.get_rect()
    wrect.topright = [w - 20, 65]
    screen.blit(wtext, wrect)

    if not ship.health:
        endtext = "GAME OVER"
        render_text(dfont, endtext, srect.center, (255, 255, 255))
        can_fire = False

    pygame.display.flip()

    clock.tick(200)
    ticks += 1
