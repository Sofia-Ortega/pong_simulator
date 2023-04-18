#              .';:cc;.
#            .,',;lol::c.
#            ;';lddddlclo
#            lcloxxoddodxdool:,.
#            cxdddxdodxdkOkkkkkkkd:.
#          .ldxkkOOOOkkOO000Okkxkkkkx:.
#        .lddxkkOkOOO0OOO0000Okxxxxkkkk:
#       'ooddkkkxxkO0000KK00Okxdoodxkkkko
#      .ooodxkkxxxOO000kkkO0KOxolooxkkxxkl
#      lolodxkkxxkOx,.      .lkdolodkkxxxO.
#      doloodxkkkOk           ....   .,cxO;
#      ddoodddxkkkk:         ,oxxxkOdc'..o'
#      :kdddxxxxd,  ,lolccldxxxkkOOOkkkko,
#       lOkxkkk;  :xkkkkkkkkOOO000OOkkOOk.
#        ;00Ok' 'O000OO0000000000OOOO0Od.
#         .l0l.;OOO000000OOOOOO000000x,
#            .'OKKKK00000000000000kc.
#               .:ox0KKKKKKK0kdc,.
#                      ...
#
# Author: peppe8o
# Blog: https://peppe8o.com
# Date: Nov 8th, 2020
# Version: 1.0

import RPi.GPIO as GPIO
import sys

# Define PINs according to cabling
dataPINs = [5, 6, 13, 19, 26]
latchPIN = [20]
clockPIN = [21]

# Strings that represent the row and column drivers
xstring = "000000000000000000000000"
ystring = "0000000000000000"

#set pins to putput
GPIO.setmode(GPIO.BCM)
GPIO.setup((dataPINs[0], dataPINs[1], dataPINs[2], dataPINs[3], dataPINs[4],latchPIN,clockPIN),GPIO.OUT)

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
    GPIO.output(data[0], int(xinput[i]))
    # Load x2
    GPIO.output(data[1], int(xinput[8 + i]))
    # Load x3
    GPIO.output(data[2], int(xinput[16 + i]))
    # Load y1
    GPIO.output(data[3], int(yinput[i]))
    # Load y2
    if i == 7:
      GPIO.output(data[4], 0)
    else:
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

# Main program, calling shift register function
# Uses "sys.argv" to pass arguments from command line
xinput = sys.argv[1]
yinput = sys.argv[2]
all_shift(xinput, yinput, dataPINs, clockPIN, latchPIN)

#PINs final cleaning
GPIO.cleanup()
