#!/usr/bin/env python

from fltk import *


def but_move_cb(wid):
    win_dim = [win2.x(), win2.y(), win2.w(), win2.h()]

    if wid == but_up:
        win2.resize(win_dim[0], win2.y() - 5, win_dim[2], win_dim[3])
    elif wid == but_down:
        win2.resize(win_dim[0], win2.y() + 5, win_dim[2], win_dim[3])
    elif wid == but_left:
        win2.resize(win2.x() - 5, win_dim[1], win_dim[2], win_dim[3])
    else:
        win2.resize(win2.x() + 5, win_dim[1], win_dim[2], win_dim[3])

    win2.label("(" + str(win2.x()) + ", " + str(win2.y()) + ")")


def but_hide_cb(wid):
    if win2.visible():
        win2.hide()
    else:
        win2.show()
    print win.take_focus()


def dimens_cb(wid):
    win_dim = [win2.x(), win2.y(), win2.w(), win2.h()]

    if wid == but_tall:
        win2.resize(win_dim[0], win_dim[1], win_dim[2], win2.h() + 5)
    elif wid == but_short and win2.h() > 5:
        win2.resize(win_dim[0], win_dim[1], win_dim[2], win2.h() - 5)
    elif wid == but_wide:
        win2.resize(win_dim[0], win_dim[1], win2.w() + 5, win_dim[3])
    elif wid == but_shrink and win2.w() > 5:
        win2.resize(win_dim[0], win_dim[1], win2.w() - 5, win_dim[3])

    dimbox.label(str(win2.w()) + ' x ' + str(win2.h()))


win = Fl_Window(200, 200, 80, 160)

win.begin()

but_up = Fl_Button(30, 10, 20, 20, "&W")
but_down = Fl_Button(30, 50, 20, 20, "&S")
but_left = Fl_Button(10, 30, 20, 20, "&A")
but_right = Fl_Button(50, 30, 20, 20, "&D")
but_hide = Fl_Button(30, 30, 20, 20, "&H")

but_tall = Fl_Button(30, 80, 20, 20, "&I")
but_short = Fl_Button(30, 120, 20, 20, "&K")
but_wide = Fl_Button(50, 100, 20, 20, "&L")
but_shrink = Fl_Button(10, 100, 20, 20, "&J")

win.end()

but_up.callback(but_move_cb)
but_down.callback(but_move_cb)
but_left.callback(but_move_cb)
but_right.callback(but_move_cb)
but_hide.callback(but_hide_cb)

but_tall.callback(dimens_cb)
but_short.callback(dimens_cb)
but_wide.callback(dimens_cb)
but_shrink.callback(dimens_cb)

win2 = Fl_Window(500, 500, 200, 200)
win2.label("(" + str(win2.x()) + ", " + str(win2.y()) + ")")

win2.begin()

dimbox = Fl_Box(5, 5, 100, 20, str(win2.w()) + ' x ' + str(win2.h()))

win2.end()

Fl.scheme("gtk+")
win2.show()
win.show()
Fl.run()
