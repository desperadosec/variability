#!/usr/bin/python

import curses
import shelve
import sys
import locale
import traceback
import util
import subprocess
import os

from constants import *
import proc
import window
import g
#from g import *

import logging
logger = logging.getLogger('myapp')
hdlr = logging.FileHandler('/tmp/log.log')
formatter = logging.Formatter('%(asctime)s %(levelname)s %(message)s')
hdlr.setFormatter(formatter)
logger.addHandler(hdlr) 
logger.setLevel(logging.WARNING)

# TODO: Add searching for string in OutputWindow
# TODO: Add connscan, psscan, etc.
# TODO: Set up text output dir, temp dir for process dumps, vaddump dir

#def popupSelectionWindow(choices):

def openDumpfile(filename):
    proc.launchProcesses(filename)
    
def main(stdscr):
    curses.init_pair(1, curses.COLOR_CYAN, curses.COLOR_BLUE)

    screen_y, screen_x = stdscr.getmaxyx()

    menuWindowY = 12
    menu_window = window.MenuWindow(menuWindowY-STATUS_LINE_SIZE, screen_x, 0, 0)
    FOCUSED_WINDOW = menu_window

    output_window = window.OutputWindow(screen_y-menuWindowY-STATUS_LINE_SIZE, screen_x, begin_y=menuWindowY-STATUS_LINE_SIZE, begin_x=0)

    menu_window.populateEntries()
    output_window.populateEntries()

    if len(sys.argv) == 2:
        openDumpfile(sys.argv[1])

    while True:
        menu_window.populateEntries()
        output_window.populateEntries()

        proc.updateOutput()
        util.printStatusLine(stdscr, "Current pid: %s" % str(g.CURRENTPID))
        util.printHelpLine(stdscr, "p:set Pid\td:Dumpvmcore\te:procExedump\tm:procMemdump\tvV:Vaddump\tq:Quit")

        userinput = stdscr.getch()
        try:
            if userinput == curses.KEY_UP:
                if FOCUSED_WINDOW.keyUpEvent():
                    output_window.populateEntries()
            elif userinput == curses.KEY_DOWN:
                if FOCUSED_WINDOW.keyDownEvent():
                    output_window.populateEntries()
            elif chr(userinput) in 'qQ':
                break
            elif chr(userinput) in 'pP':                
                screen_y, screen_x = stdscr.getmaxyx()
                curses.echo()
                enterpidmsg = "Enter pid:"
                util.printStatusLine(stdscr, enterpidmsg)
                # Get a 6-character string
                s = stdscr.getstr(screen_y-1, len(enterpidmsg), 6)
                try:
                    g.CURRENTPID = int(s)
                except ValueError:
                    pass
                curses.noecho()
                proc.launchPidProcesses()
            elif chr(userinput) in 'dD':
                # Memory dump running VM

                # TODO: Make the program reload with this file
                try:
                    os.remove(g.MEMDUMP)
                except OSError as e:
                    pass
                process = subprocess.Popen(['VBoxManage', 'debugvm',  g.VMNAME, 'dumpvmcore', '--filename', g.MEMDUMP])
                out, err = process.communicate()

                # Now, open the dump we just created
                openDumpfile(g.MEMDUMP)

            elif chr(userinput) in 'mM':
                # Dump process memory 
                if g.CURRENTPID is None:
                    continue
                else:
                    cmd = proc.getPCmd('procmemdump')
                    print cmd
                    process = subprocess.Popen(cmd)
                    out, err = process.communicate()

            elif chr(userinput) in 'eE':
                if g.CURRENTPID is None:
                    continue
                else:
                    cmd = proc.getCmd('procexedump')
                    process = subprocess.Popen(cmd)
                    out, err = process.communicate()

            elif chr(userinput) in 'vV':
                if g.CURRENTPID is None:
                    continue
                else:
                    cmd = proc.getPCmd('vaddump')
                    process = subprocess.Popen(cmd)
                    out, err = process.communicate()


            elif chr(userinput) == '\t': 
                OUPUT_OFFSET = 0
                if FOCUSED_WINDOW == menu_window:
                    FOCUSED_WINDOW = output_window
                elif FOCUSED_WINDOW == output_window:
                    FOCUSED_WINDOW = menu_window
            else:
                pass
        except ValueError:
            continue


def updatePidEvent():
    pass

if __name__ == '__main__':
    locale.setlocale(locale.LC_ALL, "")

    curses.initscr()
    curses.curs_set(0)
    curses.wrapper(main)
    #  Random notes and things
    """
    curses.init_color(curses.COLOR_CYAN, 0x7a, 0xc5, 0xcd)
    curses.init_color(curses.COLOR_BLUE, 0x2f, 0x4f, 0x4f)
    #curses.init_color(2, 29, 216, 255)
    """
    """
    handlers = {
                curses.KEY_UP:      self.h_move_line_up,
                curses.KEY_LEFT:    self.h_move_cell_left,
                curses.KEY_DOWN:    self.h_move_line_down,
                curses.KEY_RIGHT:   self.h_move_cell_right,
                "k":                self.h_move_line_up,
                "h":                self.h_move_cell_left,
                "j":                self.h_move_line_down,
                "l":                self.h_move_cell_right,
                curses.KEY_NPAGE:   self.h_move_page_down,
                curses.KEY_PPAGE:   self.h_move_page_up,
                curses.KEY_HOME:    self.h_show_beginning,
                curses.KEY_END:     self.h_show_end,
                ord('g'):           self.h_show_beginning,
                ordrd('G'):           self.h_show_end,
                curses.ascii.TAB:   self.h_exit,
                '^P':               self.h_exit_up,
                '^N':               self.h_exit_down,
                #curses.ascii.NL:    self.h_exit,
                #curses.ascii.SP:    self.h_exit,
                #ord('x'):       self.h_exit,
                ord('q'):       self.h_exit,
                curses.ascii.ESC:   self.h_exit,
            }

        #self.win.addstr(msg, curses.color_pair(1) | curses.A_REVERSE)
    """


