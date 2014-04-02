#!/usr/bin/env python

from itertools import product

rects = []
checkpoints = {}

g = int(raw_input())
tf = int(raw_input())
for _ in xrange(g):
    rects.append([int(x) for x in raw_input().split()])

for r in rects:
    prod = product(xrange(r[0], r[2]), xrange(r[1], r[3]))
    for i in prod:
        if i in checkpoints:
            checkpoints[i] += r[4]
        else:
            checkpoints[i] = r[4]

tinted = 0
for v in checkpoints.itervalues():
    if v >= tf:
        tinted += 1
print tinted
