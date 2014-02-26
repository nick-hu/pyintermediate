#!/usr/bin/env python

mount, branch, lake = [], [], []

t = int(raw_input())
for _ in xrange(t):
    mount.append([])
    branch.append([0])
    lake.append([0])
    n = int(raw_input())
    for _ in xrange(n):
        mount[-1].append(int(raw_input()))

for mi, m in enumerate(mount):
    m.reverse()
    while m:
        stuck = True

        if m[0] > m[1]:
            branch[mi].insert(0, m.pop(0))
            stuck = False

        if m[0] == lake[mi][0] + 1:
            lake[mi].insert(0, m.pop(0))
            stuck = False

        if not m:
            for c in xrange(len(branch[mi]) - 1):
                lake[mi].insert(0, branch[mi].pop(0))

        if stuck:
            break

    lake[mi].reverse()
    if not stuck:
        ideal_lake = range(max(lake[mi]) + 1)
        if lake[mi] == ideal_lake:
            print "Y"
            continue
    print "N"
