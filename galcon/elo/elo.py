#!/usr/bin/env python


class ELODict(dict):
    def __init__(self, players=[], startrating=1500, k=24):
        """Initialize an Elo dictionary.

        Keyword arguments:
        players -- player name strings (default [])
        startrating -- initial player rating (default 1500)
        k -- K-value for Elo algorithm (default 24)
        """
        super(self.__class__, self).__init__()
        for p in players:
            self[p] = startrating
        self.k = k

    def win_prob(self, pA, pB):
        """Calculate win probability of two players against each other."""
        eA = 1 / (1 + 10**((self[pB] - self[pA]) / 400.0))
        eB = 1 / (1 + 10**((self[pA] - self[pB]) / 400.0))
        return eA, eB

    def update_games(self, pA, pB, winsA, winsB, draws=0):
        """Update Elo ratings of two players.

        Keyword arguments:
        pA -- player A's name string
        pB -- player B's name string
        winsA -- number of wins by player A
        winsB -- number of wins by player B
        draws -- number of draws (default 0)
        """
        eA, eB = self.win_prob(pA, pB)
        g = sum((winsA, winsB, draws))

        self[pA] += int(self.k * ((winsA + 0.5*draws) - eA*g))
        self[pB] += int(self.k * ((winsB + 0.5*draws) - eB*g))
