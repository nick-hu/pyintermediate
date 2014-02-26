#!/usr/bin/env python

ant, david = 100, 100

rounds = int(raw_input())
for _ in xrange(rounds):
    r = a, d = [int(x) for x in raw_input().split()]
    if a < d:
        ant -= max(r)
    if d < a:
        david -= max(r)

print ant
print david