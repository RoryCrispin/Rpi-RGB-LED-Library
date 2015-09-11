from __future__ import division
import time
import sys

import RPi.GPIO as GPIO
import pigpio

pi = None

# noinspection PyPep8Naming
from led_modes import find_delta


class rgbColour(object):
    red = 0
    green = 0
    blue = 0

    def __init__(self, red, green, blue, safe_brightness=False):
        # By default safe_brightness will block low duty cycles to keep fade
        # motions smooth

        if not safe_brightness:
            self.red = red
            self.green = green
            self.blue = blue
        else:
            self.safe_brightnessF(red, green, blue, safe_brightness)

    def with_brightness(self, multiplier):
        return rgbColour(
            self.red *
            multiplier,
            self.green *
            multiplier,
            self.blue *
            multiplier)

    def safe_brightnessF(self, red, green, blue, safe_b):
        def set_min(val, minimum):
            if val < minimum:
                return minimum
            else:
                return val

        self.red = set_min(red, safe_b)
        self.blue = set_min(blue, safe_b)
        self.green = set_min(green, safe_b)


def hex_rgb_to_colour(r, g, b):
    hex_constant = 0.3921568627
    return rgbColour(int(hex_constant * r),
                     int(hex_constant * g),
                     int(hex_constant * b))


def hex_to_colour(v):
    if v[0] == '#':
        v = v[1:]
    assert (len(v) == 6)
    # return int(v[:2], 16), int(v[2:4], 16), int(v[4:6], 16)
    return hex_rgb_to_colour(int(v[:2], 16), int(v[2:4], 16), int(v[4:6], 16))


def percentageToHex(percentage):
    return 2.55 * percentage

def hexToPercentage(hex):
    return hex/255*100

# Preset Colours
red = rgbColour(100, 0, 0)
green = rgbColour(0, 100, 0)
blue = rgbColour(0, 0, 100)
orange = hex_rgb_to_colour(255, 127, 0)
yellow = hex_rgb_to_colour(255, 255, 0)
indigo = hex_rgb_to_colour(75, 0, 130)
lime = hex_rgb_to_colour(125,255,0)
ocean = rgbColour(0,54,100)
purple = rgbColour(100, 0, 100)
violet = purple
hot_pink = hex_rgb_to_colour(255,0,125)
aqua = rgbColour(0, 100, 100)
turquoise = rgbColour(0, 100, 30)

namedColours = {
    "red": red,
    "green": green,
    "blue": blue,
    "orange": orange,
    "yellow": yellow,
    "indigo": indigo,
    "lime": lime,
    "ocean": ocean,
    "purple": purple,
    "violet":purple,
    "hot pink": hot_pink,
    "aqua": aqua,
    "turquoise": turquoise
}


# noinspection PyPep8Naming
class rbgLed(object):

    def __init__(self, RED, GREEN, BLUE):
        self.R_led = RED
        self.G_led = GREEN
        self.B_led = BLUE
        self.mode = None

    def set_colour(self, colour):
        self.R_led.set_ds(colour.red)
        self.G_led.set_ds(colour.green)
        self.B_led.set_ds(colour.blue)

    def verbose_get_colour(self):
        print ("COLOUR : " +
               str(self.R_led.duty_cycle) +
               " " +
               str(self.G_led.duty_cycle) +
               " " +
               str(self.B_led.duty_cycle))
        return rgbColour(
            self.R_led.duty_cycle,
            self.G_led.duty_cycle,
            self.B_led.duty_cycle)

    def blink(self, colour, hold_time):
        self.set_colour(colour)
        time.sleep(hold_time)
        self.turn_off()

    def get_colour(self):
        return rgbColour(
            self.R_led.duty_cycle,
            self.G_led.duty_cycle,
            self.B_led.duty_cycle)

    def turn_off(self):
        self.R_led.turn_off()
        self.G_led.turn_off()
        self.B_led.turn_off()

    def fade_to(self, destColour, length):
        steps = 100
        startColour = self.get_colour()
        redDelta = find_delta(startColour.red, destColour.red, steps)
        greenDelta = find_delta(startColour.green, destColour.green, steps)
        blueDelta = find_delta(startColour.blue, destColour.blue, steps)
        for i in range(0, steps + 1, 1):
            time.sleep(length)
            to = rgbColour(startColour.red + (i * redDelta),
                           startColour.green + (i * greenDelta),
                           startColour.blue + (i * blueDelta))
            self.set_colour(to)

    def bind_mode(self, mode, unbind=True, resume_thread=False):
        if not self.mode or not unbind:
            self.mode = mode
            mode.bind_led(self)
        else:
            print("Rebind")
            prev_mode = self.mode
            self.mode.unbind_led()
            # Wait for the thread to exit before starting a new one.
            self.mode.join()
            self.mode = mode
            if not resume_thread:
                self.mode.bind_led(self)
            else:
                self.mode.bind_led(self, start=False)
        print("tasked")

    def interruptMode(self, mode, pause=False, resume_thread=False):
        # self.mode.interrupt_func()
        previousMode = self.mode
        if pause:
            self.mode.request_pause(wait_until_paused=True)
        self.bind_mode(mode, unbind=False)
        if pause:
            self.mode.join()

        if resume_thread:
            self.mode.join()
            print("Joined #01")
            self.bind_mode(previousMode, resume_thread=True)
            previousMode.unpause()


class LED(object):

    def __init__(self, pin, bool_pwm, freq):
        self.pin = pin
        # GPIO.setup(self.pin, GPIO.OUT)
        self.duty_cycle = 0
        if bool_pwm:
            pass
            # self.pwm = GPIO.PWM(pin, freq)
            # self.pwm.start(self.duty_cycle)

    def set_ds(self, val, hexInput=False):
        if not hexInput:
            hex = int(percentageToHex(val))
            self.duty_cycle = val
        else:
            self.duty_cycle = None
        # print "Change LED: " + str(self.pin) + " to ds: " + str(hex) + " For
        # %: " + str(percentage)
        pi.set_PWM_dutycycle(self.pin, hex)

    def turn_off(self):
        self.set_ds(0)


def init():
    global pi
    pi = pigpio.pi()
    pass
    # GPIO.setmode(GPIO.BCM)
    # GPIO.setwarnings(False)


def exit(LED):
    LED.turn_off()
    pi.stop()
    # GPIO.cleanup()
