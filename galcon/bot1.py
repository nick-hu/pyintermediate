#!/usr/bin/env python

from PlanetWars import PlanetWars


def turn(pw):

    enemy_planets = pw.EnemyPlanets()
    if not enemy_planets:
        pw.FinishTurn()
        return

    enemy_pop = sum(p.NumShips() for p in enemy_planets)
    enemy_avg = enemy_pop / len(enemy_planets)

    stable_pop = enemy_avg ** 0.33

    moves = {}

    for m in pw.MyPlanets():
        mID = m.PlanetID()

        for p in pw.NotMyPlanets():
            pID = p.PlanetID()

            #pw.IssueOrder(pw.MyPlanets()[0].PlanetID(), 10, 1)
            #pw.FinishTurn()
            #return

            d, g, n = pw.Distance(mID, pID), p.GrowthRate(), p.NumShips()
            force = n + stable_pop

            if m.NumShips() - (n + stable_pop) < stable_pop:
                continue

            value = g**2 - n - d**2
            if p.Owner() == 2:
                value *= 1
            moves[(mID, pID, force)] = value

    #with open("log2.txt", "a") as f:
    #    f.write("{0}: {1}\r\n".format(n, str(value)))

    moved, dests = [], []
    for move in sorted(moves, key=lambda mv: moves[mv], reverse=True):
        if (move[0] not in moved) and (move[1] not in dests):
            pw.IssueOrder(*move)
            moved.append(move[0])
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
