import rbgLib
import time
__author__ = 'Rory'
rbgLib.init()
redLED = rbgLib.LED(18, True, 200)
greenLED = rbgLib.LED(24, True, 200)
blueLED = rbgLib.LED(23, True, 200)

rgbLEDx = rbgLib.rbgLed(redLED, greenLED, blueLED)
rgbLEDx.set_colour((rbgLib.rgbColour(100, 10, 10)))
time.sleep(1)
rbgLib.ledAlert(rbgLib.rgbColour(10, 100, 10), rgbLEDx, 50)
time.sleep(1)
rbgLib.ledAlert(rbgLib.orange,rgbLEDx,100)
rbgLib.ledAlert(rbgLib.violet,rgbLEDx,100)
rbgLib.exit(rgbLEDx)
