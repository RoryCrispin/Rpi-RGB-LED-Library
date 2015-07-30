from __future__ import division

__author__ = 'Rory'
import time


class RGBFunctionParent(object):
    interrupt = False
    func_name = None
    run_time = 0
    run_infinite = False
    rgbled = None

    def __init__(self, func_name, run_time=False):
        self.func_name = func_name
        # self.rgbled = rgbled
        # Set run_time to False to run indefinitely
        if not run_time:
            self.run_infinite = True
        else:
            self.run_time = run_time

    def start(self):
        self.main_func()

    def bind_led(self, rgbled, start=True):
        self.rgbled = rgbled
        if start:
            self.start()

    def unbind_led(self):
        self.interrupt_func()

    def main_func(self):
        pass

    def pause(self):
        pass

    def main_func(self):
        pass

    def interrupt_func(self):
        self.interrupt = True
        self.pause()


class mode_breathe(RGBFunctionParent):
    colour = None
    pulse_time = 0

    def __init__(self, colour, pulse_time, run_time=False):
        super(mode_breathe, self).__init__("breathe", run_time)
        self.colour = colour
        self.pulse_time = pulse_time

    def main_func(self):
        while 1:
            if self.interrupt:
                break
            # self.rgbled.fade_to(self.colour, int(self.pulse_time / 2))
            # self.rgbled.fade_to(self.colour.with_brightness(0.2), int(self.pulse_time / 2))
            self.rgbled.fade_to(self.colour, self.pulse_time)
            self.rgbled.fade_to(self.colour.with_brightness(0.2), self.pulse_time)


class mode_static(RGBFunctionParent):
    colour = None

    def __init__(self, rgbLed, colour):
        super(mode_breathe, self).__init__("static", rgbLed)
        self.colour = colour

    def main_func(self):
        self.rgbled.setcolour(self.colour)


def find_delta(start_val, finish_val, steps):
    return (finish_val - start_val) / steps


def ledAlert(destColour, rgbLEDy, length):
    startColour = rgbLEDy.get_colour()
    rgbLEDy.fade_to(destColour, length)
    time.sleep(0.5)
    rgbLEDy.fade_to(startColour, length)
