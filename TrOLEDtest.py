#----------------------------------------------------------------------
# ssd1351.py from https://github.com/boxysean/py-gaugette
# ported by boxysean
#
# This library works with 
#   Adafruit's 128x128 SPI RGB OLED   https://www.adafruit.com/products/1431
#
# The code is based heavily on Adafruit's Arduino library
#   https://github.com/adafruit/Adafruit-SSD1351-library
# written by Limor Fried/Ladyada for Adafruit Industries.
#
# Some important things to know about this device and SPI:
#
# SPI and GPIO calls are made through an abstraction library that calls
# the appropriate library for the platform.
# For the RaspberryPi:
#     wiring2
#     spidev
#
# Presently untested / not supported for BBBlack
#

# This is a test example for the Adafruit Trellis w/HT16K33
#
#   Designed specifically to work with the Adafruit Trellis 
#   ----> https://www.adafruit.com/products/1616
#   ----> https://www.adafruit.com/products/1611
#
#   These displays use I2C to communicate, 2 pins are required to  
#   interface
#   Adafruit invests time and resources providing this open source code, 
#   please support Adafruit and open-source hardware by purchasing 
#   products from Adafruit!
#
#   Written by Limor Fried/Ladyada for Adafruit Industries.  
#   MIT license, all text above must be included in any redistribution
#
#   Python port created by Tony DiCola (tony@tonydicola.com).

# This example shows reading buttons and setting/clearing buttons in a loop
#   "momentary" mode has the LED light up only when a button is pressed
#   "latching" mode lets you turn the LED on/off when pressed
#
#   Up to 8 matrices per I2C bus can be used but this example will show 4 or 1

#----------------------------------------------------------------------

import ssd1351 as ssd
import time
import Adafruit_Trellis
# Color definitions
BLACK    = 0x0000
BLUE     = 0x001F
RED      = 0xF800
GREEN    = 0x07E0
CYAN     = 0x07FF
MAGENTA  = 0xF81F
YELLOW   = 0xFFE0 
WHITE    = 0xFFFF

disp = ssd.SSD1351()
disp.begin()
c = 0

MOMENTARY = 0
LATCHING = 1
# Set the mode here:
MODE = MOMENTARY

matrix0 = Adafruit_Trellis.Adafruit_Trellis()

trellis = Adafruit_Trellis.Adafruit_TrellisSet(matrix0)

NUMTRELLIS = 1

numKeys = NUMTRELLIS * 16

# Connect Trellis Vin to 5V and Ground to ground.
# Connect Trellis INT wire to a digital input (optional)
# Connect Trellis I2C SDA pin to your board's SDA line
# Connect Trellis I2C SCL pin to your board's SCL line
# All Trellises on an I2C bus share the SDA, SCL and INT pin! 
# Even 8 tiles use only 3 wires max

# Set this to the number of the I2C bus that the Trellises are attached to:
I2C_BUS = 1

# Setup
print 'Trellis + OLED testing'

# TODO: Setup the INT input

# begin() with the I2C addresses and bus numbers of each panel in order
# I find it easiest if the addresses are in order
trellis.begin((0x70, I2C_BUS))   # only one
# trellis.begin((0x70,  I2C_BUS), (0x71, I2C_BUS), (0x72, I2C_BUS), (0x73, I2C_BUS))  # or four!

# light up all the LEDs in order
for i in range(numKeys):
        trellis.setLED(i)
        trellis.writeDisplay()
        time.sleep(0.05)
# then turn them off
for i in range(numKeys):
        trellis.clrLED(i)
        trellis.writeDisplay()
        time.sleep(0.05)

# Loop
print 'Press Ctrl-C to quit.'
while True:
        time.sleep(0.03)

        if MODE == MOMENTARY:
                # If a button was just pressed or released...
                if trellis.readSwitches():
                        # go through every button
                        for i in range(numKeys):
                                # if it was pressed, turn it on
                                if trellis.justPressed(i):
                                        print 'v{0}'.format(i)
                                        trellis.setLED(i)
                                        disp.clear_display()
                                        disp.fillScreen(0x000000)
                                        disp.draw_text(32,32,'button{0}'.format(i),0xFFFFFF)
                                        # disp.dump_buffer()
                                        # print 'black'
                                # if it was released, turn it off
                                if trellis.justReleased(i):
                                        print '^{0}'.format(i)
                                        trellis.clrLED(i)
                                        disp.clear_display()
                                        disp.fillScreen(0x000000)
                                        disp.draw_text(32,32,'OFFOFF',0xFF00FF)
                                        # print 'red'
                                        # disp.fillScreen(0xFF0000) # this really is red
                        # tell the trellis to set the LEDs we requested
                        trellis.writeDisplay()

        if MODE == LATCHING:
                # If a button was just pressed or released...
                if trellis.readSwitches():
                        # go through every button
                        for i in range(numKeys):
                                # if it was pressed...
                                if trellis.justPressed(i):
                                        print 'v{0}'.format(i)
                                        # Alternate the LED
                                        if trellis.isLED(i):
                                                trellis.clrLED(i)
                                        else:
                                                trellis.setLED(i)
                        # tell the trellis to set the LEDs we requested
                        trellis.writeDisplay()


