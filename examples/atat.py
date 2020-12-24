#!/usr/bin/env python3
# AT AT lights
# Author: Ben Skiff
#

import time
from rpi_ws281x import PixelStrip, Color
import random

# LED strip configuration:
LED_COUNT = 120        # Number of LED pixels.
LED_PIN = 18          # GPIO pin connected to the pixels (18 uses PWM!).
# LED_PIN = 10        # GPIO pin connected to the pixels (10 uses SPI /dev/spidev0.0).
LED_FREQ_HZ = 800000  # LED signal frequency in hertz (usually 800khz)
LED_DMA = 10          # DMA channel to use for generating signal (try 10)
LED_BRIGHTNESS = 80  # Set to 0 for darkest and 255 for brightest
LED_INVERT = False    # True to invert the signal (when using NPN transistor level shift)
LED_CHANNEL = 0       # set to '1' for GPIOs 13, 19, 41, 45 or 53

COCKPIT_LEDS = 2      # Number of leds per strip that are in the AT-AT cockpit, and should always remain lit
BEAM_START = 4        # Number of led on each strip that marks the start of the beam
BEAM_LENGTH = 3       # Number of leds in each blaster beam

# Define functions which animate LEDs in various ways.
def shootBeam(strip, wait_ms=50):
    for i in range(strip.numPixels() - BEAM_START):
        leading_led = i + BEAM_START
        trailing_led = leading_led - BEAM_LENGTH

        strip.setPixelColor(leading_led, Color(255, 0, 0))
        if trailing_led >= BEAM_START:
            strip.setPixelColor(trailing_led, Color(0, 0, 0))
        
        strip.show()
        time.sleep(wait_ms / 1000.0)

def turnOnCockpit(strip):
    for i in range(COCKPIT_LEDS):
        strip.setPixelColor(i, Color(255, 0, 0))
    strip.show()

def turnOffAll(strip):
    for i in range(LED_COUNT):
        strip.setPixelColor(i, Color(0, 0, 0))
    strip.show()

if __name__ == '__main__':
    strip = PixelStrip(LED_COUNT, LED_PIN, LED_FREQ_HZ, LED_DMA, LED_INVERT, LED_BRIGHTNESS, LED_CHANNEL)
    strip.begin()

    print('Press Ctrl-C to quit.')

    try:
        turnOnCockpit(strip)
        while True:
            shootBeam(strip)
            time.sleep(1 + random.random() * 5)

    except KeyboardInterrupt:
        turnOffAll(strip)
