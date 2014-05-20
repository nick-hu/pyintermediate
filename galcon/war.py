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

for m in maps:
    proc = sub.Popen(["java", "-jar", "tools/PlayGame.jar", m,
                     "1000", "1000", "log.txt", b1arg, b2arg],
                     stdout=sub.PIPE, stderr=sub.PIPE)

    out, err = proc.communicate()

    if "Player 1 Wins!" in err:
        win1 += 1
    elif "Player 2 Wins!" in err:
        win2 += 1
    elif "Draw!" in err:
        draw += 1
    else:
        err += 1

    msg = """P1 Wins: {0}\tP2 Wins: {1}\tDraws: {2}\tOther: {3}"""
    sys.stdout.write("\r" + msg.format(win1, win2, draw, other))
    sys.stdout.flush()

print "\n"
