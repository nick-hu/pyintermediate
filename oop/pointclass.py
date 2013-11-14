#!/usr/bin/env python

from math import atan, degrees


class Point(object):
    def __init__(self, x=0, y=0):
        self.coord = self.x, self.y = [x, y]

    def __str__(self):
        return str(tuple(self.coord))

    def __add__(self, other):
        return Point(self.x + other.x, self.y + other.y)

    def __sub__(self, other):
        return Point(self.x - other.x, self.y - other.y)

    def __mul__(self, other):
        return Point(self.x * other.x, self.y * other.y)

    def __div__(self, other):
        return Point(self.x / other.x, self.y / other.y)

    def __eq__(self, other):
        return (self.x == other.x) and (self.y == other.y)

    def __ne__(self, other):
        return not Point.__eq__(self, other)

    def __invert__(self):
        return Point(self.y, self.x)

    def __or__(self, other):
        dx, dy = other.x - self.x, other.y - self.y
        return (dx**2 + dy**2) ** 0.5

    def __xor__(self, other):
        dx, dy = other.x - self.x, other.y - self.y
        return degrees(atan(float(dy)/dx))
