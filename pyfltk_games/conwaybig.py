#!/usr/bin/env python

from fltk import *


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


def but_cb(wid):
    name = wid.label()
    if name == "&Start" or name == "S&tep":
        update_grid(name)
    elif name == "Sto&p":
        Fl.remove_timeout(update_grid)
    else:
        for cell in cells:
            if cell.color() != FL_BLACK:
                cell.color(FL_WHITE)
                cell.state = False
                cell.redraw()
        genbox.value(0)


def update_grid(name="&Start"):
    nalive, neighbours = [0] * 203, (-203, -202, -201, -1, 1, 201, 202, 203)
    check = set([])
    for cell in xrange(203, 40601):
        n = [cells[cell + addr].state for addr in neighbours].count(True)
        nalive.append(n)
        if n > 0:
            check.update(set([cell + addr for addr in neighbours]))
    nalive = nalive + [0] * 203

    for cell in check:
        if cells[cell].color() != FL_BLACK:
            if nalive[cell] < 2 or nalive[cell] > 3:
                cells[cell].color(FL_WHITE)
                cells[cell].state = False
                cells[cell].redraw()
            elif cells[cell].state is False and nalive[cell] == 3:
                cells[cell].color(fl_rgb_color(80, 150, 0))
                cells[cell].state = True
                cells[cell].redraw()

    if name == "&Start":
        Fl.repeat_timeout(speed.value(), update_grid)
    genbox.value(genbox.value() + 1)

cells = []

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

but_labels = ["&Start", "Sto&p", "S&tep", "&Clear"]
for y in xrange(4):
    but = Fl_Button(830, 10 + y * 40, 100, 30)
    but.label(but_labels.pop(0))
    but.callback(but_cb)

speed = Fl_Value_Slider(830, 195, 100, 20, "Speed")
speed.type(FL_HOR_SLIDER)
speed.align(FL_ALIGN_TOP)
speed.value(0.10)
speed.minimum(0.10)
speed.step(0.05)

genbox = Fl_Value_Output(830, 270, 100, 30, "Generation")
genbox.color(FL_WHITE)
genbox.align(FL_ALIGN_TOP)

win.end()
win.show()
Fl.run()
