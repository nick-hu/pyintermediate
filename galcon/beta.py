#!/usr/bin/env python

from PlanetWars import PlanetWars


def turn(pw):

    enemy_planets = pw.EnemyPlanets()
    if not enemy_planets:
        pw.FinishTurn()
        return

    enemy_pop = sum(p.NumShips() for p in enemy_planets)
    enemy_avg = enemy_pop / len(enemy_planets)

    moves, mypop = {}, {}
    for m in pw.MyPlanets():
        mypop[m.PlanetID()] = m.NumShips()

    sway = (float(enemy_pop) / sum(mypop.itervalues()))

    stable_pop = enemy_avg ** 0.33
    #stable_pop = max(0.5, -(sway ** 2) + enemy_avg ** 0.33)
    #import pprint
    #with open("log2.txt", "a") as f:
    #    f.write(pprint.pformat(stable_pop) + "\n")

    for mID, mships in mypop.iteritems():
        danger = False

        for ef in pw.EnemyFleets():
            dest = pw.GetPlanet(ef.DestinationPlanet())
            dID = dest.PlanetID()
            if dID == mID:
                danger = True
                break
            d, g, n = pw.Distance(mID, dID), dest.GrowthRate(), dest.NumShips()
            efn = ef.NumShips()

            if dest.Owner() == 1:  # Defend
                future_pop = (n + d * g) - efn
                if d < ef.TurnsRemaining() and future_pop < stable_pop:
                    force = int(stable_pop - future_pop) + 1
                    if mships - force < stable_pop:
                        force = int(mships - stable_pop) + 1

                    value = (g**2 + n**0.5 - d**1.5 + 10000) / force
                    moves[(mID, dID, force)] = value
        if danger:
            continue

        for p in pw.Planets():
            pID, own = p.PlanetID(), p.Owner()
            d, g, n = pw.Distance(mID, pID), p.GrowthRate(), p.NumShips()
            fut_n = n + d * g

            if own == 1 and mID != pID and (fut_n < stable_pop):  # Reinforce
                force = int(stable_pop - fut_n) + 1
                value = g**2 + 10000
                moves[(mID, pID, force)] = value

            else:  # Attack
                force = (int(n + stable_pop) + 1)

                if own == 2:
                    force += int(d * g)
                if mships - force < stable_pop:
                    force = int(mships - stable_pop) + 1

                value = float(g**2 - n**0.5 - d**1.5 + 10000) / force
                if own == 2:
                    value *= 1.5
                moves[(mID, pID, force)] = value

    #import pprint
    #with open("log2.txt", "a") as f:
    #    f.write(pprint.pformat(moves) + "\n")

    dests = [f.DestinationPlanet() for f in pw.MyFleets()]
    for move in sorted(moves, key=lambda mv: moves[mv], reverse=True):
        mID, pID, force = move
        if pID not in dests:
            newpop = mypop[mID] - force
            if newpop >= stable_pop:
                pw.IssueOrder(*move)
                dests.append(pID)
                mypop[mID] = newpop

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
