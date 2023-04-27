#
# Reference code was used from https://peppe8o.com
#

import RPi.GPIO as GPIO
import sys
import time

# Define PINs according to cabling
dataPINs = [5, 6, 13, 19, 26]
latchPIN = [20]
clockPIN = [21]

# Strings that represent the row and column drivers
xstring = "000000000000000000000000"
ystring = "0000000000000000"

LEDs = [[0 for i in range(16)] for j in range(24)]

rowON = [0 for i in range(24)]
columnOn = [0 for i in range(16)]

#set pins to putput
GPIO.setmode(GPIO.BCM)
GPIO.setup((dataPINs[0], dataPINs[1], dataPINs[2], dataPINs[3], dataPINs[4],latchPIN,clockPIN), GPIO.OUT)

def all_shift(xinput, yinput, data, clock, latch):
  # Put latch down to start data sending
  GPIO.output(clock,0)
  GPIO.output(latch,0)
  GPIO.output(clock,1)

  # Load data in reverse order
  for i in range(7, -1, -1):
    GPIO.output(clock,0)

    # These may need to be changed based on how they are shifted

    # Load x1
    GPIO.output(data[0], int(xinput[i]) ^ 1) # Negate because column supplies ground
    # Load x2
    GPIO.output(data[1], int(xinput[8 + i]) ^ 1)
    # Load x3
    GPIO.output(data[2], int(xinput[16 + i]) ^ 1)
    # Load y1
    GPIO.output(data[3], int(yinput[i]))
    # Load y2
    GPIO.output(data[4], int(yinput[8 + i]))

    GPIO.output(clock,1)

  # Put latch up to store data on register
  GPIO.output(clock,0)
  GPIO.output(latch,1)
  GPIO.output(clock,1)


# Set the row and column strings to all 0s
def resetStrings():
  global xstring 
  global ystring
  xstring = "000000000000000000000000"
  ystring = "0000000000000000"

# Update the row and column strings to turn on a desired LED
def updateStrings(xCoord, yCoord):
  global xstring
  global ystring
  xstring[xCoord] = '1'
  ystring[yCoord] = '1'

# Main program, tests that shift registers can light all LEDs in sequential order
all_shift(xstring, ystring, dataPINs, clockPIN, latchPIN)

# for i in range(24):
#   for j in range(16):
#     updateStrings(i, j)
#     all_shift(xstring, ystring, dataPINs, clockPIN, latchPIN)
#     time.sleep(2)
#     resetStrings()
  
for i in range(8):
  for j in range(8):
    updateStrings(i, j)
    all_shift(xstring, ystring, dataPINs, clockPIN, latchPIN)
    time.sleep(2)
    resetStrings()

#PINs final cleaning
GPIO.cleanup()
