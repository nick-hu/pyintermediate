#!/usr/bin/env python


def validate(word, p):
    puzz = p[:]
    if len(word) < 4:
        return False
    if puzz[4] not in word:
        return False

    for char in word:
        if char not in puzz:
            return False
        puzz.remove(char)
    return True

puzzwords = []

with open('A.in') as infile:
    while True:
        pword = infile.readline()
        if pword == '\n':
            break
        puzzword = list(pword[:-1])
        numguess = int(infile.readline()[:-1])
        guesses = [list(infile.readline()[:-1]) for _ in xrange(numguess)]

        puzzwords.append((puzzword, guesses))

for puzzleword in puzzwords:
    for guess in puzzleword[1]:
        valid = validate(guess, puzzleword[0])
        if valid:
            print ''.join(guess), 'is valid'
        else:
            print ''.join(guess), 'is invalid'
