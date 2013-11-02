#!/usr/bin/env python

from fltk import *
import cglpatterns as cglp


class Cell(Fl_Button):
    def __init__(self, x, y, w, h, s=None):
        Fl_Button.__init__(self, x, y, w, h, s)
        self.state = False


def cell_cb(cell):
    if cell.state:
        cell.color(FL_WHITE)
    else:
        cell.color(fl_rgb_color(80, 150, 0))
    cell.state = not cell.state
    check.clear()


def but_cb(wid):
    name = wid.label()
    if name == "&Start" or name == "S&tep":
        update_grid(name)
    elif name == "Sto&p":
        Fl.remove_timeout(update_grid)
    elif name == "&Clear":
        for cell in cells:
            if cell.color() != FL_BLACK:
                cell.color(FL_WHITE)
                cell.state = False
                cell.redraw()
        genbox.value(0)
    else:
        pattern = fl_input("Pattern to paste:")
        if pattern not in cglp.patterns:
            fl_alert("Pattern name not found in cglpatterns!")
        else:
            patsize = cglp.size(cglp.patterns[pattern])
            posinp = fl_input("Coordinates to paste at (x,y):").split(",")
            posx, posy = int(posinp[0]), int(posinp[1])
            patx, paty = posx + patsize[0], posy + patsize[1]

            if posx <= 0 or patx >= 202 or posy <= 0 or paty >= 202:
                fl_alert("Pattern touches edges/does not fit!")
            else:
                cglp.paste(pattern, posy * 202 + posx, 202, cells)

    check.clear()


def update_grid(name="&Start"):
    neighbours, nalive = (-203, -202, -201, -1, 1, 201, 202, 203), []

    if not check:
        check.update(a for a in xrange(203, 40601) if cells[a].state)
    newcheck = check.copy()
    for cell in newcheck:
        for addr in neighbours:
            if cells[cell + addr].color() != FL_BLACK:
                check.add(cell + addr)
    for cell in sorted(check):
        n = [cells[cell + addr].state for addr in neighbours].count(1)
        nalive.append(n)

    for ci, cell in enumerate(sorted(check)):
        if nalive[ci] < 2 or nalive[ci] > 3:
            cells[cell].color(FL_WHITE)
            cells[cell].state = False
            cells[cell].redraw()
            newcheck.discard(cell)
        elif cells[cell].state is False and nalive[ci] == 3:
            cells[cell].color(fl_rgb_color(80, 150, 0))
            cells[cell].state = True
            cells[cell].redraw()
            newcheck.add(cell)

    check.clear()
    check.update(newcheck)

    if name == "&Start":
        Fl.repeat_timeout(speed.value(), update_grid)
    genbox.value(genbox.value() + 1)

cells, check = [], set([])

win = Fl_Window(200, 200, 940, 808, "Conway's Game of Life")
win.color(FL_WHITE)

win.begin()

for y in xrange(202):
    for x in xrange(202):
        but = Cell(x * 4, y * 4, 4, 4)
        but.box(FL_FLAT_BOX)
        but.color(FL_WHITE)
        if y == 0 or y == 201 or x == 0 or x == 201:
            but.color(FL_BLACK)
        else:
            but.callback(cell_cb)
        cells.append(but)

but_labels = ["&Start", "Sto&p", "S&tep", "&Clear", "&Load"]
for y in xrange(5):
    but = Fl_Button(825, 10 + y * 40, 100, 30)
    but.label(but_labels.pop(0))
    but.callback(but_cb)

speed = Fl_Value_Slider(825, 250, 100, 20, "Speed")
speed.type(FL_HOR_SLIDER)
speed.align(FL_ALIGN_TOP)
speed.value(0.05)
speed.minimum(0.05)
speed.step(0.05)

genbox = Fl_Value_Output(825, 325, 100, 30, "Generation")
genbox.color(FL_WHITE)
genbox.align(FL_ALIGN_TOP)

win.end()
win.show()
Fl.run()
