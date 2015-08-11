from __future__ import division
import random

__author__ = 'Rory'
import time
from threading import Thread
import rbgLib


class RGBFunctionParent(Thread):
    interrupt = False
    func_name = None
    run_time = 0
    run_infinite = False
    rgbled = None
    prev_mode = None
    pause = False
    pause_ready = False

    def __init__(self, func_name, run_time=False):
        self.uuid = random.getrandbits(30)
        print "INIT MODE -- UUID: "
        print self.uuid
        Thread.__init__(self)
        if not run_time:
            self.run_infinite = True
        else:
            self.run_time = run_time
        self.func_name = func_name
        self.daemon = True
        # self.start()
        # self.rgbled = rgbled
        # Set run_time to False to run indefinitely

    def run(self):
        self.interrupt = False
        self.main_func()

    def bind_led(self, rgbled, prev_mode=None, start=True):
        self.prev_mode = prev_mode
        self.rgbled = rgbled
        if start:
            self.start()

    def unbind_led(self):
        self.interrupt_func()

    def main_func(self):
        pass

    def unpause(self):
        self.pause = False

    def request_pause(self, wait_until_paused=False):
        self.pause = True
        if wait_until_paused:
            while not self.pause_ready:
                pass
        pass

    def main_func(self):
        pass

    def interrupt_func(self):
        self.interrupt = True
        # self.request_pause()

    def mode_finished(self, resumePrev):
        pass

    def check_loop(self):
        if self.pause:
            self.pause_ready = True
            while self.pause:
                pass
            self.pause_ready = False


class mode_breathe(RGBFunctionParent):
    colours = None
    pulse_time = 0
    fade_to_black = False

    def __init__(self, colours, pulse_time, run_time=False, fade_to_black = False):
        super(mode_breathe, self).__init__("breathe", run_time)
        self.colours = colours
        self.pulse_time = float(pulse_time)
        self.fade_to_black = fade_to_black
        if len(colours) == 1:
            self.fade_to_black = True
        print colours


    def main_func(self):
        self.pause = False
        while True:
            for colour in self.colours:
                self.check_loop()
                if self.interrupt:
                    break
                self.rgbled.fade_to(colour, self.pulse_time)
                time.sleep(self.pulse_time*10)

                if self.fade_to_black:
                    self.rgbled.fade_to(
                        colour.with_brightness(0.05),
                        self.pulse_time)
                    time.sleep(self.pulse_time)
            if self.interrupt:
                break


class mode_static(RGBFunctionParent):
    colour = None

    def __init__(self, rgbLed, colour, func_name):
        super(mode_static, self).__init__("static", rgbLed)
        self.colour = colour

    def main_func(self):
        self.rgbled.setcolour(self.colour)


class mode_alert(RGBFunctionParent):
    colour = None

    def __init__(self, colour):
        super(mode_alert, self).__init__("alert")
        self.colour = colour

    def main_func(self):
        ledAlert(self.colour, self.rgbled, 0.01)
        # self.mode_finished(True)


class mode_strobe(RGBFunctionParent):
    colour = None
    period = None
    through_black = False

    def __init__(self, colours, period, through_black=False):
        super(mode_strobe, self).__init__("strobe")
        self.colours = colours
        self.period = float(period)
        self.through_black = through_black
        if len(colours) == 1:
            self.through_black = True

    def main_func(self):

        self.pause = False
        # off = rbgLib.rgbColour(0,0,0)
        pOn = self.period
        pOff = self.period * 15
        print pOn
        print pOff
        while True:
            for colour in self.colours:
                self.check_loop()
                if self.interrupt:
                    break
                self.check_loop()
                self.rgbled.set_colour(colour)
                time.sleep(pOn)
                if self.through_black:
                    self.rgbled.turn_off()
                    time.sleep(pOff)
            if self.interrupt:
                break



class mode_rainbow(RGBFunctionParent):
    period = None

    def __init__(self, period, brightness=1):
        super(mode_rainbow, self).__init__("rainbow")
        self.period = float(period)

    def main_func(self):
        self.pause = False
        rainbowColours = [rbgLib.red, rbgLib.orange, rbgLib.yellow, rbgLib.green, rbgLib.blue, rbgLib.indigo,
                          rbgLib.purple]

        while True:
            self.check_loop()
            if self.interrupt:
                break
            # self.rgbled.fade_to(self.colour, int(self.pulse_time / 2))
            # self.rgbled.fade_to(self.colour.with_brightness(0.2), int(self.pulse_time / 2)
            for colour in rainbowColours:
                self.rgbled.fade_to(colour, self.period)
                time.sleep(self.period)
                self.check_loop()


class mode_fadeto(RGBFunctionParent):
    colour = None
    period = None

    def __init__(self, colour, period):
        super(mode_fadeto, self).__init__("fadeto")
        self.colour = colour
        self.period = float(period)

    def main_func(self):
        self.rgbled.fade_to(self.colour, self.period)


def find_delta(start_val, finish_val, steps):
    return (finish_val - start_val) / steps


def ledAlert(destColour, rgbLEDy, length):
    startColour = rgbLEDy.get_colour()
    rgbLEDy.fade_to(destColour, length)
    time.sleep(0.5)
    rgbLEDy.fade_to(startColour, length)


# All modes must be listed here
modes = {
    "breathe": mode_breathe,
    "fade": mode_breathe,

    "static": mode_static,
    "alert": mode_alert,

    "strobe": mode_strobe,
    "flash": mode_strobe,

    "rainbow": mode_rainbow,
    "fadeto": mode_fadeto,

    "kill": None}
