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

#define PINs according to cabling
dataPINs =  [5, 6, 13, 19, 26]
latchPIN = [20]
clockPIN = [21]

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

    # Load x1
    GPIO.output(data[0], int(xinput[16 + i]))
    # Load x2
    GPIO.output(data[1], int(xinput[8 + i]))
    # Load x3
    GPIO.output(data[2], int(xinput[i]))
    # Load y1
    if i == 7:
      GPIO.output(data[3], 0)
    else:
      GPIO.output(data[3], int(yinput[8 + i]))
    # Load y2
    GPIO.output(data[4], int(yinput[i]))

    GPIO.output(clock,1)

  # Put latch up to store data on register
  GPIO.output(clock,0)
  GPIO.output(latch,1)
  GPIO.output(clock,1)


#main program, calling shift register function
#uses "sys.argv" to pass arguments from command line
xinput = sys.argv[1]
yinput = sys.argv[2]
all_shift(xinput, yinput, dataPINs, clockPIN, latchPIN)

#PINs final cleaning
GPIO.cleanup()
