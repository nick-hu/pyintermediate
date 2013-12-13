#!/usr/bin/env python


def padzeros(L):
    padw = int(len(L) ** 0.5) + 2
    queue, new_L = L[:], []

    for n in xrange(padw**2):
        if (n <= padw-1) or (n >= padw**2 - padw):
            new_L.append(0)
        elif (n % padw == 0) or (n % padw == padw-1):
            new_L.append(0)
        else:
            new_L.append(queue.pop(0))

    return new_L


def sumaround(L, i):
    gridw = int(len(L) ** 0.5)
    padw, padded = gridw + 2, padzeros(L)

    true_i = padw * ((i // gridw) + 1) + 1 + (i % gridw)
    nbrs = (-1, -padw+1, -padw, -padw-1, 1, padw-1, padw, padw+1)

    return sum(padded[true_i + n] for n in nbrs)
