
class breathe(object):
   def __init__(self):
    pass

modes = {
    "breathe": breathe,
    "static": None,
    "alert": None,
    "strobe": None,
    "rainbow": None,
    "fadeto": None,
    "kill": None}



def findMode(cmd):
    for mode in modes:
       if mode in cmd:
           return mode
    return False

def takeCommand(command):
    findMode(command)


takeCommand("breathe blue")