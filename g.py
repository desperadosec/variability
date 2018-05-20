import ConfigParser

cfg = ConfigParser.ConfigParser()
cfg.read('config.ini')
VOLPATH = cfg.get('Global','VOLPATH')
DUMPDIR = cfg.get('Global','DUMPDIR')
PROFILE = cfg.get('Global','PROFILE')
VMNAME = cfg.get('Global','VMNAME')

# This list is used to populate the upper "commands" window list
# TODO Add back connscan
CMDINDEX = ['vboxinfo', 'pslist', 'pstree', 'connections', 'sockets','dlllist','psxview', 'psscan', 'connscan', 'netscan', 'malfind','apihooks']

PCMDINDEX = ['procmemdump','procexedump','vaddump']

# =============== Globals =================================
# We'll need globals to determine things like cursor focus
FOCUSED_WINDOW = None

# Item selection globals
SELECTED = 0
OUTPUT_OFFSET = 0

CURRENTPID = None

MEMDUMP = '/tmp/dump333.elf'

# Dictionary containing cmd:Popen object
PROC_DICT = {}
PROC_DICT.setdefault(None)
# Dictionary containing cmd:
OUTPUT_DICT = {}
OUTPUT_DICT.setdefault(None)

