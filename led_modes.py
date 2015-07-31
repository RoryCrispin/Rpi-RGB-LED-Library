from __future__ import division

__author__ = 'Rory'
import time
from threading import Thread


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

    def pause(self, wait_until_paused=False):
        self.pause = True
        if wait_until_paused:
            while not self.pause_ready:
                pass
        pass

    def main_func(self):
        pass

    def interrupt_func(self):
        self.interrupt = True
        self.pause()

    def mode_finished(self, resumePrev):
        pass



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
            if self.pause:
                self.pause_ready = True
                while self.pause:
                    pass
                self.pause_ready = False
            # self.rgbled.fade_to(self.colour, int(self.pulse_time / 2))
            # self.rgbled.fade_to(self.colour.with_brightness(0.2), int(self.pulse_time / 2))
            self.rgbled.fade_to(self.colour, self.pulse_time)
            time.sleep(self.pulse_time)
            self.rgbled.fade_to(self.colour.with_brightness(0.05), self.pulse_time)
            time.sleep(self.pulse_time)


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


def find_delta(start_val, finish_val, steps):
    return (finish_val - start_val) / steps


def ledAlert(destColour, rgbLEDy, length):
    startColour = rgbLEDy.get_colour()
    rgbLEDy.fade_to(destColour, length)
    time.sleep(0.5)
    rgbLEDy.fade_to(startColour, length)


# All modes must be listed here
modes = {"breathe": mode_breathe, "static": mode_static, "alert": mode_alert}
