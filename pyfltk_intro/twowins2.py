#!/usr/bin/env python

from fltk import *


def buttons_cb(wid, name):
    win_dim = (win2.x(), win2.y(), win2.w(), win2.h())

    if name == "W":
        win2.position(win_dim[0], win_dim[1] - 5)  # Shorthand
    elif name == "S":
        win2.position(win_dim[0], win_dim[1] + 5)
    elif name == "A":
        win2.position(win_dim[0] - 5, win_dim[1])
    elif name == "D":
        win2.position(win_dim[0] + 5, win_dim[1])
    elif name == "I":
        win2.resize(win_dim[0], win_dim[1] - 5, win_dim[2], win_dim[3] + 10)
    elif name == "K" and win_dim[3] > 10:
        win2.resize(win_dim[0], win_dim[1] + 5, win_dim[2], win_dim[3] - 10)
    elif name == "L":
        win2.resize(win_dim[0] - 5, win_dim[1], win_dim[2] + 10, win_dim[3])
    elif name == "J" and win_dim[2] > 10:
        win2.resize(win_dim[0] + 5, win_dim[1], win_dim[2] - 10, win_dim[3])
    elif name == "G":
        color = fl_color_chooser("Pick a color", 255, 255, 255)[1:]
        win2.color(fl_rgb_color(color[0], color[1], color[2]))
        win2.redraw()
    elif name == 'H':
        if win2.visible():
            win2.hide()
        else:
            win2.show()

    win2.label("(" + str(win2.x()) + ", " + str(win2.y()) + ")")
    dimbox.label(str(win2.w()) + " x " + str(win2.h()))


labels = ["H", "K", "L", "J", "I", "G", "S", "D", "A", "W"]
but_pos = [(30, 10), (10, 30), (50, 30), (30, 50), (30, 30)]
for p in xrange(5):
    but_pos.append((but_pos[p][0], but_pos[p][1] + 70))

win = Fl_Window(200, 200, 80, 160)

win.begin()

for pos in but_pos:
    name = labels.pop()
    button = Fl_Button(pos[0], pos[1], 20, 20, name)
    button.shortcut(name.lower())
    button.callback(buttons_cb, name)

win.end()

win2 = Fl_Window(500, 500, 200, 200, "(500, 500)")

win2.begin()
dimbox = Fl_Box(5, 5, 80, 20, "200 x 200")
win2.end()

Fl.scheme("gtk+")
win2.show()
win.show()
Fl.run()
