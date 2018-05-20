import curses

from constants import *
from g import *

class Window(object):
    def __init__(self, height, width, begin_y, begin_x):
        # Perform init for things common to all windows
        self.begin_y = begin_y
        self.begin_x =  begin_x
        self.border_width = 2
        self.border_height = 1
        self.height = height
        self.width = width
        # Every window has this "win" which is an ncurses window object
        self.win = curses.newwin(self.height, self.width, self.begin_y, self.begin_x)
        self.win.box()

    def addLine(self, msg, color_pair=None):
        msg = msg.encode("utf-8")
        msg = msg[:self.width-self.border_width*2]

        if color_pair is not None:
            self.win.addstr(msg, curses.color_pair(1))
        else:
            self.win.addstr(msg)

        currenty, currentx =  self.win.getyx()
        self.win.move(currenty+1, self.begin_x+self.border_width)

    def keyUpEvent(self):
        raise NotImplementedError

    def keyDownEvent(self):
        raise NotImplementedError

    def drawBorder(self):
        raise NotImplementedError

class MenuWindow(Window):
    def __init__(self, height, width, begin_y, begin_x):
        super(MenuWindow, self).__init__(height, width, begin_y, begin_x)
        # This is the selected item in the list
        self.selectedItem = 0
        self.minVisible = 0
        #self.maxVisible = 10 # TODO: Base this on the size of window
        self.maxVisible = height-self.border_height*2

        # Move the cursor to the top of window area so we can start drawing
        self.win.move(self.begin_y+self.border_height, self.begin_x+self.border_width)

    def selectLine(self):
        pass

    def unselectLine(self):
        pass

    def populateEntries(self):
        self.win.clear()
        self.win.box()
        self.win.move(self.begin_y+self.border_height, self.begin_x+self.border_width)
        
        global SELECTED

        for n in range(self.minVisible, min(self.maxVisible, len(CMDINDEX))):
            if n != SELECTED:
                self.addLine(CMDINDEX[n])
            else:
                self.addLine(CMDINDEX[n], HIGHLIGHTED_TEXT)
        self.win.refresh()

    def keyAEvent(self):
        pass

    def keyUpEvent(self):
        """
        Returns True if other windows need refreshing
        Returns False otherwise
        """
        needRefresh = False
        global SELECTED
        if SELECTED == 0:
            pass
        else:
            # Let's see if complicated redraw logic is even worth it
            SELECTED -= 1
            if SELECTED < self.minVisible:
                self.minVisible -= 1
                self.maxVisible -= 1
            needRefresh = True
            self.populateEntries()
        return needRefresh
            
    def keyDownEvent(self):
        """
        Returns True if other windows need refreshing
        Returns False otherwise
        """
        needRefresh = False
        global SELECTED
        if SELECTED == len(CMDINDEX)-1:
            pass
        else:
            SELECTED += 1
            if SELECTED > self.maxVisible-1:
                self.minVisible += 1
                self.maxVisible += 1
            needRefresh = True
            self.populateEntries()
        return needRefresh

class OutputWindow(Window):
    def __init__(self, height, width, begin_y, begin_x):
        super(OutputWindow, self).__init__(height, width, begin_y, begin_x)
        self.minVisible = 0
        self.maxVisible = self.height-self.border_height*2

    def keyUpEvent(self):
        global OUTPUT_OFFSET
        # TODO move common login to populate Entries
        try:
            output = OUTPUT_DICT[CMDINDEX[SELECTED]]
        except KeyError as e:
            return

        if (OUTPUT_OFFSET == 0):
            pass
        else:
            OUTPUT_OFFSET -= 1
            self.populateEntries()

        self.populateEntries()

    def keyDownEvent(self):
        global OUTPUT_OFFSET

        try:
            output = OUTPUT_DICT[CMDINDEX[SELECTED]]
        except KeyError as e:
            return

        if OUTPUT_OFFSET == len(output.split('\n')):
            pass
        else:
            OUTPUT_OFFSET += 1
            self.populateEntries()

    def addText(self, string, offset):
        # Print as much of the text as will fit in the usable
        #  portion of the window, starting at line <offset>
        count = 0
        lines = string.split('\n')[offset:]
        for line in lines:
            self.addLine(line[:self.width-5])
            count += 1
            if count == self.height-self.border_height*2:
                return

    def populateEntries(self):
        self.win.clear()
        self.win.box()
        self.win.move(self.border_height, self.border_width)
        self.addText(OUTPUT_DICT.get(CMDINDEX[SELECTED],"Now Loading..."), OUTPUT_OFFSET)
        self.win.refresh()

