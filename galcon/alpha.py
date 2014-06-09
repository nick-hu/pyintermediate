#!/usr/bin/env python

import sys
import os
import subprocess as sub

from PlanetWars import PlanetWars


def turn(pw):

    enemy_planets = pw.EnemyPlanets()
    if not enemy_planets:
        pw.FinishTurn()
        return

    enemy_pop = sum(p.NumShips() for p in enemy_planets)
    enemy_avg = enemy_pop / len(enemy_planets)

    stable_pop = 0.02 * enemy_avg + 2.4

    moves = {}

    for m in pw.MyPlanets():
        mID = m.PlanetID()
        best_move, best_value = None, None
        danger = False

        for p in pw.NotMyPlanets():
            pID = p.PlanetID()

            d, g, n = pw.Distance(mID, pID), p.GrowthRate(), p.NumShips()
            force = n + stable_pop
            blitz = False

            if p.Owner() == 2:
                force += d * g
                begin = len(enemy_planets) == 1 and len(pw.MyPlanets()) <= 3
                if (m.NumShips() >= enemy_pop - 10) and begin and 5 <= d <= 21:
                    new_sp = (enemy_avg ** 0.33) / 2
                    force = m.NumShips() - new_sp
                    blitz = True

            if (m.NumShips() - int(force) + 1 < stable_pop) and not blitz:
                continue

            value = 3*g**2 + 10.0/(n + 1) - d**2
            if blitz:
                value += 5000
            #print (mID, pID, force), value
            if (best_move is None) or (value > best_value):
                best_move, best_value = (mID, pID, force), value

        for ef in pw.EnemyFleets():
            if ef.NumShips() <= p.GrowthRate():
                continue

            dest = pw.GetPlanet(ef.DestinationPlanet())
            dID = dest.PlanetID()
            d, g, n = pw.Distance(mID, dID), dest.GrowthRate(), dest.NumShips()
            future_pop = (n + d * g) - ef.NumShips()

            if dID == mID and future_pop < stable_pop:
                danger = True
                break

            if dest.Owner() == 1:
                if d < ef.TurnsRemaining() and future_pop < stable_pop:
                    force = int(stable_pop - future_pop) + 1
                    if m.NumShips() - force < stable_pop:
                        continue

                    value = g**2 - d
                    if (best_move is None) or (value > best_value):
                        best_move, best_value = (mID, dID, force), value
        if danger:
            continue

        if best_move:
            moves[best_move] = best_value

    #print moves

    dests = [f.DestinationPlanet() for f in pw.MyFleets()]
    for move in sorted(moves, key=lambda mv: moves[mv], reverse=True):
        if move[1] not in dests:
            pw.IssueOrder(*move)
            dests.append(move[1])

    pw.FinishTurn()


def main():
    """
    sys.stdout = os.fdopen(sys.stdout.fileno(), "w", 0)  # Unbuffer stdout

    tee = sub.Popen(["tee", "log2.txt"], stdin=sub.PIPE)
    os.dup2(tee.stdin.fileno(), sys.stdout.fileno())
    os.dup2(tee.stdin.fileno(), sys.stderr.fileno())
    """
    map_data = ""
    while True:
        current_line = raw_input()
        if len(current_line) >= 2 and current_line.startswith("go"):
            pw = PlanetWars(map_data)
            turn(pw)
            map_data = ""
        else:
            map_data += current_line + "\n"

if __name__ == "__main__":
    main()
