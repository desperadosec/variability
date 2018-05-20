#-*- coding: utf-8 -*-

import curses
import shelve

import traceback

from constants import *

def printStatusLine(stdscr, msg, colorpair=1):
    # Clip the message to console window size
    screen_y, screen_x = stdscr.getmaxyx()
    msg = msg[:screen_x]
    stdscr.move(screen_y-STATUS_LINE_SIZE, 0)
    stdscr.clrtoeol()
    try:
        stdscr.addstr(msg, colorpair)
    except curses.error:
        pass

def printHelpLine(stdscr, msg, colorpair=1):
    # Clip the message to console window size
    screen_y, screen_x = stdscr.getmaxyx()
    msg = msg[:screen_x]
    stdscr.move(screen_y-STATUS_LINE_SIZE-1, 0)
    stdscr.clrtoeol()
    try:
        stdscr.addstr(msg, colorpair)
    except curses.error:
        pass

def recalcWindowSizes():
    screen_y, screen_x = stdscr.getmaxyx()
    # TODO Finish this

