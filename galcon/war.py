#!/usr/bin/env python

from os import listdir
from os.path import abspath
import sys
import subprocess as sub

maps = sorted([p for p in listdir(sys.argv[1])], key=lambda s: int(s[3:-4]))
maps = [sys.argv[1] + p for p in maps]

b1input, b2input = sys.argv[2].split(), sys.argv[3].split()
b1com, b1arg = b1input[:-1], b1input[-1]
b2com, b2arg = b2input[:-1], b2input[-1]

b1arg = " ".join(b1com) + " " + abspath(b1arg)
b2arg = " ".join(b2com) + " " + abspath(b2arg)

win1, win2, draw, other = 0, 0, 0, 0
if len(sys.argv) >= 5:
    logfile = open(sys.argv[4], "w")
    logging = True
else:
    logging = False

for m in maps:
    proc = sub.Popen(["java", "-jar", "tools/PlayGame.jar", m,
                     "1000", "1000", "log.txt", b1arg, b2arg],
                     stdout=sub.PIPE, stderr=sub.PIPE)

    out, err = proc.communicate()

    if "Player 1 Wins!" in err:
        win1 += 1
        winner = "P1"
    elif "Player 2 Wins!" in err:
        win2 += 1
        winner = "P2"
    elif "Draw!" in err:
        draw += 1
        winner = "Draw"
    else:
        other += 1
        winner = "Unknown"

    msg = """P1 Wins: {0}\tP2 Wins: {1}\tDraws: {2}\tOther: {3}"""
    sys.stdout.write("\r" + msg.format(win1, win2, draw, other))
    sys.stdout.flush()

    if logging:
        turns = [l.strip() for l in err.split("\n")][-3][5:]
        msg = "Map {0}: {1} after {2} turns\n"
        logfile.write(msg.format(m, winner, turns))

print "\n"
if logging:
    logfile.close()
