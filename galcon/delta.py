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
    base_pop = int(enemy_avg ** 0.5) + 1

    enemy_power, stable_pops = {}, {}
    for ep in enemy_planets:
        enemy_power[ep.PlanetID()] = ep.NumShips() * ep.GrowthRate()

    for p in pw.Planets():
        pID = p.PlanetID()
        highestD, dID = None, None
        for eID in enemy_power:
            if eID != pID:
                D = enemy_power[eID] / pw.Distance(pID, eID)
                if highestD is None or D > highestD:
                    highestD, dID = D, eID

        if highestD is None:
            stable_pops[pID] = base_pop
        else:
            dplanet = pw.GetPlanet(dID)
            dd = pw.Distance(pID, dplanet.PlanetID())
            stp = dplanet.NumShips() - p.GrowthRate() * dd
            stable_pops[pID] = max(stp / 2, base_pop)

    values = {}
    for p in pw.NotMyPlanets():
        value = p.GrowthRate() ** 2 - p.NumShips()
        if p.Owner() == 2:
            value += 50
        values[p.PlanetID()] = value

    under_attack = [ef.DestinationPlanet() for ef in pw.EnemyFleets()]
    #print [p for p in under_attack]

    forces = {}
    for p in pw.MyPlanets():
        pID = p.PlanetID()
        force = p.NumShips() - stable_pops[pID]
        if force > p.GrowthRate() and (pID not in under_attack):
            forces[pID] = force
        else:
            forces[pID] = 0

    dests = (f.DestinationPlanet() for f in pw.MyFleets())
    for target in sorted(values, key=lambda p: values[p], reverse=True):
        if target in dests:
            continue
        tp = pw.GetPlanet(target)
        dists = {}
        for p in forces:
            dists[p] = pw.Distance(p, target)

        for move in getforces(tp, forces, dists, stable_pops):
            pw.IssueOrder(*move)

    pw.FinishTurn()


def getforces(tp, forces, dists, sps):
    tID = tp.PlanetID()
    needed = tp.NumShips() + sps[tID]

    moves = []
    for p in sorted(dists, key=lambda p: dists[p]):
        force = forces[p]
        if not force:
            continue
        if force >= needed:
            moves.append((p, tID, needed))
            forces[p] -= needed
            break
        else:
            moves.append((p, tID, force))
            needed -= force
            forces[p] -= force

    return moves


def main():
    sys.stdout = os.fdopen(1, "w", 0)  # Unbuffer stdout

    tee = sub.Popen(["tee", "log2.txt"], stdin=sub.PIPE)
    """Redirect and close stdout and sterr. tee will allow
    them to be passed out to the viewer."""
    os.dup2(tee.stdin.fileno(), sys.stdout.fileno())
    os.dup2(tee.stdin.fileno(), sys.stderr.fileno())

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
