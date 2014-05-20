#!/usr/bin/env python

from PlanetWars import PlanetWars


def DoTurn(pw):

    if len(pw.MyFleets()) >= 1:
        return

    source = -1
    source_score = -999999.0
    source_num_ships = 0
    my_planets = pw.MyPlanets()
    for p in my_planets:
        score = float(p.NumShips())
        if score > source_score:
            source_score = score
            source = p.PlanetID()
            source_num_ships = p.NumShips()

    dest = -1
    dest_score = -999999.0
    not_my_planets = pw.NotMyPlanets()
    for p in not_my_planets:
        score = 1.0 / (1 + p.NumShips())
        if score > dest_score:
            dest_score = score
            dest = p.PlanetID()

    if source >= 0 and dest >= 0:
        num_ships = source_num_ships / 2
        pw.IssueOrder(source, dest, num_ships)


def main():
    map_data = ""
    while True:
        current_line = raw_input()
        if len(current_line) >= 2 and current_line.startswith("go"):
            pw = PlanetWars(map_data)
            DoTurn(pw)
            pw.FinishTurn()
            map_data = ""
        else:
            map_data += current_line + '\n'


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        pass
