import rbgLib
import led_modes

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



#test commit revert back here
