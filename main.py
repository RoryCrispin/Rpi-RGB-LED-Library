import rbgLib
import time
import led_modes

__author__ = 'Rory'
rbgLib.init()
frequency = 1000
redLED = rbgLib.LED(18, True, frequency)
greenLED = rbgLib.LED(24, True, frequency)
blueLED = rbgLib.LED(23, True, frequency)

rgbLEDx = rbgLib.rbgLed(redLED, greenLED, blueLED)
# rgbLEDx.set_colour((rbgLib.rgbColour(100, 10, 10)))
# time.sleep(2)
# rgbLEDx.set_colour((rbgLib.rgbColour(40, 1, 1)))
# time.sleep(2)
# print "start"
# led_modes.ledAlert(rbgLib.rgbColour(10, 100, 10), rgbLEDx, 0.004)
# print "done"
# time.sleep(1)
#led_modes.ledAlert(rbgLib.orange, rgbLEDx, 0.004)
#rgbLEDx.fade_to(rbgLib.rgbColour(0, 0, 0), 0.004)
md = led_modes.mode_breathe(rbgLib.blue, 0.04)
rgbLEDx.bind_mode(md)


rbgLib.exit(rgbLEDx)
