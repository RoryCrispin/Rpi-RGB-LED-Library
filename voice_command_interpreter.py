import rbgLib
import led_modes

# class breathe(object):
#    def __init__(self):
#     pass
#
# modes = {
#     "breathe": breathe,
#     "static": None,
#     "alert": None,
#     "strobe": None,
#     "rainbow": None,
#     "fadeto": None,
#     "kill": None}
#
# namedColours = {
#     "red": None,
#     "green": None,
#     "blue": None,
#     "orange": None,
#     "yellow": None,
#     "indigo": None,
#     "lime": None,
#     "ocean": None,
#     "purple": None,
#     "violet":None,
#     "hot pink": None,
#     "aqua": None,
#     "turquoise": None
# }



def findMode(cmd):
    for mode in led_modes.modes:

        if mode in cmd:
            return led_modes.modes[mode]
    return False

def findColours(cmd):
    colours = []
    for colour in rbgLib.namedColours:
        if colour in cmd:
            colours.append(rbgLib.namedColours[colour])
    return colours


def takeCommand(command):
    if "turn" in command:
        return led_modes.mode_static()
    mode = findMode(command)
    colours = findColours(command)
    if mode == led_modes.mode_breathe:
        md = led_modes.mode_breathe(colours,0.04)
        return md
    if mode == led_modes.mode_strobe:
        return led_modes.mode_strobe(colours,0.04)





