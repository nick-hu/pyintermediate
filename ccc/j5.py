#!/usr/bin/env python

names = int(raw_input())
a, b = raw_input().split(), raw_input().split()
parts = set([tuple(set(p)) for p in zip(a, b)])

if len(parts) == names / 2:
    print "good"
else:
    print "bad"