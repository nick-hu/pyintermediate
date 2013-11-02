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
    if name == "Start" or name == "Step":
        update_grid(name)
    elif name == "Stop":
        Fl.remove_timeout(update_grid)
    elif name == "Clear":
        for cell in cells:
            if cell.color() != FL_BLACK:
                cell.color(FL_WHITE)
                cell.state = False
                cell.redraw()
        genbox.value(0)
    else:
        boxtype = FL_THIN_DOWN_BOX if wid.value() else FL_FLAT_BOX
        for cell in cells:
            if cell.color() != FL_BLACK:
                cell.box(boxtype)
                cell.redraw()


def update_grid(name="Start"):
    nalive, neighbours = [0] * 83, (-83, -82, -81, -1, 1, 81, 82, 83)
    for cell in xrange(83, 6641):
        n = [cells[cell + addr].state for addr in neighbours].count(True)
        nalive.append(n)
    nalive = nalive + [0] * 83

    for cell in xrange(83, 6641):
        if cells[cell].color() != FL_BLACK:
            if nalive[cell] < 2 or nalive[cell] > 3:
                cells[cell].color(FL_WHITE)
                cells[cell].state = False
                cells[cell].redraw()
            elif cells[cell].state is False and nalive[cell] == 3:
                cells[cell].color(fl_rgb_color(80, 150, 0))
                cells[cell].state = True
                cells[cell].redraw()

    if name == "Start":
        Fl.repeat_timeout(0, update_grid)
    genbox.value(genbox.value() + 1)

cells = []

win = Fl_Window(200, 200, 940, 820, "Conway's Game of Life")
win.color(FL_WHITE)

win.begin()

for y in xrange(82):
    for x in xrange(82):
        but = Cell(x * 10, y * 10, 10, 10)
        but.box(FL_FLAT_BOX)
        but.color(FL_WHITE)
        if y == 0 or y == 81 or x == 0 or x == 81:
            but.color(FL_BLACK)
        else:
            but.callback(cell_cb)
        cells.append(but)

but_labels = ["Start", "Stop", "Step", "Clear", "Show grid"]
for y in xrange(5):
    but = Fl_Button(830, 10 + y * 40, 100, 30)
    but.label(but_labels.pop(0))
    if but.label() == "Show grid":
        but.type(FL_TOGGLE_BUTTON)
    but.callback(but_cb)

genbox = Fl_Value_Output(830, 250, 100, 30, "Generation")
genbox.color(FL_WHITE)
genbox.align(FL_ALIGN_TOP)

win.end()

win.show()
Fl.run()
