#!/usr/bin/python

import os

from fltk import *

def get_fname(wid):
    music = wid.value()

mpath = "/home/inter/music/"

fname = Fl_File_Chooser(mpath, "*.ogg", FL_SINGLE, "Pick a music file")
fname.callback(get_fname)

fname.show()

Fl.run()

os.system("ogg123 " + music)
