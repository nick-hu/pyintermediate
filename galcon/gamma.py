#!/usr/bin/env python

from PlanetWars import PlanetWars


def turn(pw):

    enemy_planets = pw.EnemyPlanets()
    if not enemy_planets:
        pw.FinishTurn()
        return

    enemy_pop = sum(p.NumShips() for p in enemy_planets)
    enemy_avg = enemy_pop / len(enemy_planets)

    enemy_power, stable_pops = {}, {}
    for ep in pw.EnemyPlanets():
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
            stable_pops[pID] = 0
        else:
            dplanet = pw.GetPlanet(dID)
            dd = pw.Distance(pID, dplanet.PlanetID())
            stp = dplanet.NumShips() - p.GrowthRate() * dd
            stable_pops[pID] = max(stp, 0)

    with open("log2.txt", "a") as f:
        f.write(str(stable_pops) + "\n")

    moves = {}

    for m in pw.MyPlanets():
        mID = m.PlanetID()
        best_move, best_value = None, None
        danger = False

        if p.NumShips() < stable_pops[mID]:
            continue

        for p in pw.NotMyPlanets():
            pID = p.PlanetID()

            d, g, n = pw.Distance(mID, pID), p.GrowthRate(), p.NumShips()
            force = n + stable_pops[pID]
            blitz = False

            if p.Owner() == 2:
                force += d * g
                early_game = len(enemy_planets) <= 3
                if (m.NumShips() >= enemy_pop) and early_game:
                    new_sp = stable_pops[mID] / 2
                    force = m.NumShips() - new_sp
                    blitz = True

            if (m.NumShips() - int(force) + 1 < stable_pops[mID]) and not blitz:
                continue

            value = g**2 - n - d**2
            if blitz:
                value += 5000
            if (best_move is None) or (value > best_value):
                best_move, best_value = (mID, pID, force), value

        for ef in pw.EnemyFleets():
            dest = pw.GetPlanet(ef.DestinationPlanet())
            dID = dest.PlanetID()
            if dID == mID:
                danger = True
                break
            d, g, n = pw.Distance(mID, dID), dest.GrowthRate(), dest.NumShips()

            if dest.Owner() == 1:
                future_pop = (n + d * g) - ef.NumShips()
                if d < ef.TurnsRemaining() and future_pop < stable_pops[dID]:
                    force = int(stable_pops[dID] - future_pop) + 1
                    if m.NumShips() - force < stable_pops[mID]:
                        continue

                    value = g**2 + n - d**2
                    if (best_move is None) or (value > best_value):
                        best_move, best_value = (mID, dID, force), value
        if danger:
            continue

        if best_move:
            moves[best_move] = value

    #with open("log2.txt", "a") as f:
    #    f.write(str(moves) + "\n")

    dests = [f.DestinationPlanet() for f in pw.MyFleets()]
    for move in sorted(moves, key=lambda mv: moves[mv], reverse=True):
        if move[1] not in dests:
            pw.IssueOrder(*move)
            dests.append(move[1])

    pw.FinishTurn()


def main():
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
