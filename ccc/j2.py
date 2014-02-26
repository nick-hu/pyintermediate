#!/usr/bin/env python

_ = raw_input()
votes = list(raw_input())
a, b = votes.count("A"), votes.count("B")

if a > b:
    print "A"
elif b > a:
    print "B"
else:
    print "Tie"