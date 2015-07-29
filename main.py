import rbgLib
import time

__author__ = 'Rory'
rbgLib.init()
redLED = rbgLib.LED(18, True, 200)
greenLED = rbgLib.LED(24, True, 200)
blueLED = rbgLib.LED(23, True, 200)

rgbLEDx = rbgLib.rbgLed(redLED, greenLED, blueLED)
#rgbLEDx.set_colour((rbgLib.rgbColour(100, 10, 10)))
#rbgLib.ledAlert(rbgLib.rgbColour(10, 100, 10), rgbLEDx, 50)
#rbgLib.ledAlert(rbgLib.orange, rgbLEDx, 100)
#rgbLEDx.fade_to(rbgLib.rgbColour(0, 0, 0), 100)

pass
rbgLib.mode_breathe(False,rgbLEDx,rbgLib.yellow,100).start()


rbgLib.exit(rgbLEDx)
