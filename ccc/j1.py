#!/usr/bin/env python

a, b, c = int(raw_input()), int(raw_input()), int(raw_input())
unique = len(set([a, b, c]))
s = sum([a, b, c])

if unique == 1 and s == 180:
    print "Equilateral"
elif unique == 2 and s == 180:
    print "Isosceles"
elif unique == 3 and s == 180:
    print "Scalene"
else:
    print "Error"