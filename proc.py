import subprocess
import g

import logging

"""
The job of the proc module is to: 
    * launch processes given a dumpfile
    * monitor the processes running in the
        global proc dict, and...
    * ...update the global output dict once they're done
"""

def getCmd(cmdname, dumpfile=g.MEMDUMP):
    # Gets a list corresponding to a command that subprocess.Popen can use
    cmd = ['python', g.VOLPATH, '-f', dumpfile, g.PROFILE, cmdname]
    return cmd

def getPCmd(cmdname, dumpfile=g.MEMDUMP):
    # Gets a list corresponding to a process-context command that subprocess.Popen can use
    #cmd = ['python', g.VOLPATH, '-f', dumpfile, '--profile=WinXPSP3x86', cmdname,'-D', '/tmp/', '-p', str(g.CURRENTPID)]
    cmd = ['python', g.VOLPATH, '-f', dumpfile, g.PROFILE, cmdname,'-D', '/tmp/', '-p', str(g.CURRENTPID)]
    logger = logging.getLogger('myapp')
    return cmd

def launchProcesses(dumpfile=g.MEMDUMP):
    # Launch all PID independent processes
    for cmd in g.CMDINDEX:
        if cmd not in g.PCMDINDEX:
            # A regular command not using PID
            process = subprocess.Popen(getCmd(cmd, dumpfile), stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        elif g.CURRENTPID is not None:
            # A command that needs PID and it is set
            process = subprocess.Popen(getPCmd(cmd, dumpfile), stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        else:
            # A command that needs PID and it isn't set
            continue
        # Create an entry in the process dictionary under key COMMAND
        g.PROC_DICT[cmd] = process

def updateOutput():
    # Go through the list of running commands
    # Create/Update the output dictionary entry
    for cmd in g.PROC_DICT:
        proc = g.PROC_DICT[cmd]
        if proc and proc.poll() is not None:
            out, err = proc.communicate()
            g.OUTPUT_DICT[cmd] = out
            g.PROC_DICT[cmd] = None
            with open("/tmp/"+cmd+".txt",'w') as f:
                f.write(out)

def launchPidProcesses(dumpfile=g.MEMDUMP):
    # Launch all PID dependent processes
    for cmd in g.PCMDINDEX:
        if g.CURRENTPID is not None:
            # A command that needs PID and it is set
            process = subprocess.Popen(getPCmd(cmd, dumpfile), stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        else:
            # A command that needs PID and it isn't set
            continue
        # Create an entry in the process dictionary under key COMMAND
        g.PROC_DICT[cmd] = process

