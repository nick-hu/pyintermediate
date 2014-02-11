#!/usr/bin/env python

import sys
from random import randrange
from argparse import ArgumentParser

import pygame


class Ball(object):
    def __init__(self, world):
        self.pos = []
        self.pos.append(randrange(20, world.size[0] - 20 + 1))
        self.pos.append(randrange(20, world.size[1] - 20 + 1))
        self.vel = [0, 0]
        self.acc = [0, 0]
        self.bounce = world.bounce

        self.color = pygame.Color(0, 0, 0)
        self.color.hsva = (randrange(360), randrange(50, 101), 100, 1)


parser = ArgumentParser()
parser.add_argument("-size", default=[500, 500], nargs=2, type=int)
parser.add_argument("-gravity", default=2.0, type=float)
parser.add_argument("-numballs", default=20, type=int)
parser.add_argument("-bounce", default=0.9, type=float)
parser.add_argument("-fps", default=25, type=int)
world = parser.parse_args()

world.size[0] = max(150, world.size[0])
world.size[1] = max(40, world.size[1])
world.bounce = max(0, min(world.bounce, 1))
world.fps = max(1, min(world.fps, 60))
GRAVITY = world.gravity

screen = pygame.display.set_mode(world.size)
pygame.display.set_caption("Ball Physics")

clock = pygame.time.Clock()

balls = []
for ball in xrange(world.numballs):
    ball_inst = Ball(world)
    ball_inst.acc[1] += GRAVITY
    balls.append(ball_inst)

world.size = [d - 20 for d in world.size]

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit(0)

    for ball in balls:
        for d in xrange(2):  # For each direction
            if abs(ball.vel[d]) < 1 or world.size[d] == 20:  # Landing
                if d == 0:
                    d_left = ball.pos[d] - 20
                    d_right = world.size[d] - ball.pos[d]
                    if (d_left <= 1) or (d_right <= 1):
                        ball.vel[d], ball.acc[d] = 0, 0
                else:
                    bottom = world.size[d] if GRAVITY >= 0 else 20
                    if abs(ball.pos[d] - bottom) <= 1:
                        ball.vel[d], ball.acc[d] = 0, 0

            new_pos = ball.pos[d] + ball.vel[d] + 0.5 * ball.acc[d]

            if (new_pos < 20) or (new_pos > world.size[d]):  # Wall collision
                wall = max(20, min(new_pos, world.size[d]))
                d_wall = wall - ball.pos[d]

                if ball.acc[d]:  # If accelerating
                    vb = ((ball.vel[d]) ** 2 + 2 * ball.acc[d] * d_wall) ** 0.5
                    direct = -cmp(d_wall, 0)  # Account for direction
                    vb = direct * vb if direct else -cmp(ball.acc[d], 0) * vb
                    t = 1 - ((-vb - ball.vel[d]) / ball.acc[d])
                else:  # Constant velocity
                    vb = -ball.vel[d]
                    t = 1 - (d_wall / -vb)

                if vb:
                    ball.vel[d] = (vb * ball.bounce) + ball.acc[d] * t
                    ball.pos[d] = wall + vb * t + 0.5 * ball.acc[d] * t ** 2
            else:
                ball.vel[d] += ball.acc[d]
                ball.pos[d] = new_pos

    screen.fill((255, 255, 255))

    for ball in balls:
        pos = [int(round(d)) for d in ball.pos]  # Round position for display
        ballrect = pygame.draw.circle(screen, ball.color, pos, 20)

    pygame.display.flip()

    clock.tick(world.fps)
