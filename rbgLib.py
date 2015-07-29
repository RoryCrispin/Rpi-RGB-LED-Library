from __future__ import division
import time
import RPi.GPIO as GPIO


# noinspection PyPep8Naming
class rgbColour(object):
    red = 0
    green = 0
    blue = 0

    def __init__(self, red, green, blue, safe_brightness=False):
        # By default safe_brightness will block low duty cycles to keep fade motions smooth
        if not safe_brightness:
            self.red = red
            self.green = green
            self.blue = blue
        else:
            self.safe_brightnessF(red, green, blue, safe_brightness)

    def with_brightness(self, multiplier):
        return rgbColour(self.red * multiplier, self.green * multiplier, self.blue * multiplier)

    def safe_brightnessF(self, red, green, blue, safe_b):
        def set_min(val, minimum):
            if val < minimum:
                return minimum
            else:
                return val
        self.red = set_min(red, safe_b)
        self.blue = set_min(blue, safe_b)
        self.green = set_min(green, safe_b)


def hexToColour(r, g, b):
    hex_constant = 0.3921568627
    return rgbColour(hex_constant * r, hex_constant * g, hex_constant * b)


red = rgbColour(100, 0, 0)
green = rgbColour(0, 100, 0)
blue = rgbColour(0, 0, 100)
orange = hexToColour(255, 127, 0)
yellow = hexToColour(255, 255, 0)
indigo = hexToColour(75, 0, 130)
purple = rgbColour(100, 0, 100)
aqua = rgbColour(0, 100, 100)
turquoise = rgbColour(0, 100, 30)


# noinspection PyPep8Naming
class rbgLed(object):
    def __init__(self, RED, GREEN, BLUE):
        self.R_led = RED
        self.G_led = GREEN
        self.B_led = BLUE

    def set_colour(self, colour):
        self.R_led.set_ds(colour.red)
        self.G_led.set_ds(colour.green)
        self.B_led.set_ds(colour.blue)

    def verbose_get_colour(self):
        print (
            "COLOUR : " + str(self.R_led.duty_cycle) + " " + str(self.G_led.duty_cycle) + " " + str(
                self.B_led.duty_cycle))
        return rgbColour(self.R_led.duty_cycle, self.G_led.duty_cycle, self.B_led.duty_cycle)

    def blink(self, colour, hold_time):
        self.set_colour(colour)
        time.sleep(hold_time)
        self.turn_off()

    def get_colour(self):
        return rgbColour(self.R_led.duty_cycle, self.G_led.duty_cycle, self.B_led.duty_cycle)

    def turn_off(self):
        self.R_led.turn_off()
        self.G_led.turn_off()
        self.B_led.turn_off()

    def fade_to(self, destColour, length):
        startColour = self.get_colour()
        redDelta = find_delta(startColour.red, destColour.red, length)
        greenDelta = find_delta(startColour.green, destColour.green, length)
        blueDelta = find_delta(startColour.blue, destColour.blue, length)
        for i in range(0, length + 1, 1):
            time.sleep(0.004)
            to = rgbColour(startColour.red + (i * redDelta),
                           startColour.green + (i * greenDelta),
                           startColour.blue + (i * blueDelta))
            self.set_colour(to)


class RGBFunctionParent(object):
    interrupt = False
    func_name = None
    run_time = 0
    run_infinite = False
    rgbled = None

    def __init__(self, func_name, run_time, rgbled):
        self.func_name = func_name
        self.rgbled = rgbled
        # Set run_time to False to run indefinitely
        if not run_time:
            self.run_infinite = True
        else:
            self.run_time = run_time

    def start(self):
        self.main_func()

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

    def __init__(self, run_time, rgbLed, colour, pulse_time):
        super(mode_breathe, self).__init__("breathe", run_time, rgbLed)
        self.colour = colour
        self.pulse_time = pulse_time

    def main_func(self):
        while 1:
            if self.interrupt:
                break
            self.rgbled.fade_to(self.colour, int(self.pulse_time / 2))
            self.rgbled.fade_to(yellow.with_brightness(0.2), int(self.pulse_time / 2))


class LED(object):
    def __init__(self, pin, bool_pwm, freq):
        self.pin = pin
        GPIO.setup(self.pin, GPIO.OUT)
        self.duty_cycle = 0
        if bool_pwm:
            self.pwm = GPIO.PWM(pin, freq)
            self.pwm.start(self.duty_cycle)

    def set_ds(self, duty_cycle):
        self.duty_cycle = duty_cycle
        self.pwm.ChangeDutyCycle(duty_cycle)

    def turn_off(self):
        self.set_ds(0)


def find_delta(start_val, finish_val, steps):
    return (finish_val - start_val) / steps


def ledAlert(destColour, rgbLEDy, length):
    startColour = rgbLEDy.get_colour()
    rgbLEDy.fade_to(destColour, length)
    time.sleep(0.5)
    rgbLEDy.fade_to(startColour, length)


def init():
    GPIO.setmode(GPIO.BCM)
    GPIO.setwarnings(False)


def exit(LED):
    LED.turn_off()
    GPIO.cleanup()
