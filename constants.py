#-*- coding: utf-8 -*-

import curses
import shelve

import sys
import locale

import traceback

# =============== Constants =================================

# These color pairs are actually initialized in main due to
#   other curses init needing to be done first.
HIGHLIGHTED_TEXT = 1

# Widget size constants
STATUS_LINE_SIZE = 1
BORDER_HEIGHT = 1

# Unicode symbols
UNICODE_CHECKMARK = u"\u2713"
UNICODE_HEAVY_CHECKMARK = u"\u2714"
UNICODE_BLACK_SQUARE = u"\u25a0"
UNICODE_WHITE_SQUARE = u"\u25a1"
UNICODE_WHITE_ROUNDED_SQUARE = u"\u25a2"
UNICODE_WHITE_FILLED_SQUARE = u"\u25a3"

# ==========================================================
