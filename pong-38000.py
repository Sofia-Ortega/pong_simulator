import RPi.GPIO as GPIO
from RPLCD import CharLCD
import busio
import time
import digitalio
import adafruit_mcp3xxx.mcp3008 as MCP
from adafruit_mcp3xxx.analog_in import AnalogIn
import board


# --------------- GLOBAL CONSTANTS ---------------
SCREEN_WIDTH = 24
SCREEN_HEIGHT = 16
PADDLE_SIZE = 3


# --------------- PINS ---------------
dataPINs = [5, 6, 13, 19, 26]
latchPIN = 20
clockPIN = 21
lcdPINs = [4, 17, 27, 22]
selectPIN = 18


# --------------- VARIABLES ---------------
# Position of the ball
x = 10
y = 12

# Velocities of the ball
vel_x = 1
vel_y = 1

# Top y-value of the player paddles
paddle1_y = 0
paddle2_y = 0

# Score for each player
score1 = 0
score2 = 0

# Strings representing which rows and cloumns are on
xstring = "0" * SCREEN_WIDTH
ystring = "0" * SCREEN_HEIGHT


# --------------- SETUP ---------------
carryOn = True
GPIO.setmode(GPIO.BCM)
GPIO.setup((dataPINs[0], dataPINs[1], dataPINs[2], dataPINs[3], dataPINs[4],
    latchPIN, clockPIN), GPIO.OUT)

# Create LCD object
lcd = CharLCD(numbering_mode=GPIO.BCM, cols=16, rows=2, pin_rs=23, pin_e=24, pins_data=lcdPINs)

# Initialize SPI
spi = busio.SPI(clock=board.SCLK, MISO=board.MISO, MOSI = board.MOSI)

# Create chip select
cs = digitalio.DigitalInOut(board.D18)

# Create MCP object
mcp = MCP.MCP3008(spi, cs)

# Create analog input channels on pins 6 and 7
joystick1 = AnalogIn(mcp, MCP.P6)
joystick2 = AnalogIn(mcp, MCP.P7)


# --------------- FUNCTIONS ---------------

# Logic for loading the row and cloumn strings into the shift registers
def all_shift(xinput, yinput, data, clock, latch):
    # Put latch down to start data sending
    GPIO.output(clock, 0)
    GPIO.output(latch, 0)
    GPIO.output(clock, 1)

    # Load data in reverse order
    for i in range(7, -1, -1):
        GPIO.output(clock, 0)

        # Send data to the 5 registers (columns supply ground)
        # Load register x1
        GPIO.output(data[0], not int(xinput[i]))
        # Load register x2
        GPIO.output(data[1], not int(xinput[8 + i]))
        # Load register x3
        GPIO.output(data[2], not int(xinput[16 + i]))
        # Load register y1
        GPIO.output(data[3], int(yinput[i]))
        # Load register y2
        GPIO.output(data[4], int(yinput[8 + i]))

        # Send clock signal to shift the inputs
        GPIO.output(clock, 1)

    # Put latch up to store data on registers
    GPIO.output(clock, 0)
    GPIO.output(latch, 1)
    GPIO.output(clock, 1)


# Set the row and column strings to all 0s
def resetStrings():
    global xstring
    global ystring
    xstring = "0" * SCREEN_WIDTH
    ystring = "0" * SCREEN_HEIGHT


# Update the row and column strings to turn on a desired LED
def updateStrings(xCoord, yCoord):
    global xstring
    global ystring
    xstring = xstring[0:xCoord] + "1" + xstring[xCoord + 1:]
    ystring = ystring[0:yCoord] + "1" + ystring[yCoord + 1:]


# Set player1 paddle on
def paddle1():
    global xstring
    global ystring
    xstring = "1" + ("0" * (SCREEN_WIDTH - 1))
    ystring = ("0" * paddle1_y) + ("1" * PADDLE_SIZE) + ("0" * (SCREEN_HEIGHT - PADDLE_SIZE - paddle1_y))


# Set player2 paddle on
def paddle2():
    global xstring
    global ystring
    xstring = ("0" * (SCREEN_WIDTH - 1)) + "1"
    ystring = ("0" * paddle2_y) + ("1" * PADDLE_SIZE) + ("0" * (SCREEN_HEIGHT - PADDLE_SIZE - paddle2_y))


# Set ball on
def ball():
    global xstring
    global ystring
    xstring = ("0" * x) + "1" + ("0" * (SCREEN_WIDTH - x - 1))
    ystring = ("0" * y) + "1" + ("0" * (SCREEN_HEIGHT - y - 1))


# Check if player1 paddle was hit
def hit_paddle1(x, y):
    return x == 0 and (y >= paddle1_y and y < paddle1_y + PADDLE_SIZE)


# Check if player2 paddle was hit
def hit_paddle2(x, y):
    return x == SCREEN_WIDTH - 1 and (y >= paddle2_y and y < paddle2_y + PADDLE_SIZE)

# Check if any of the paddles were hit
def hit_paddle(x, y):
    return hit_paddle1(x, y) or hit_paddle2(x, y)


# Reset the game logic
def reset():
    global x
    global y
    global vel_x
    global vel_y

    x = 10
    y = 12
    vel_x = 1
    vel_y = 1


# --------------- MAIN ---------------

# Print starting scores on the LCD
p1_scoreString = "SCORE 1: 0"
p2_scoreString = "SCORE 2: 0"
lcd.write_string(p1_scoreString)
lcd.cursor_pos = (1, 0)
lcd.write_string(p2_scoreString)

while carryOn:
    # ----- GAME LOGIC -----
    if joystick1.value > 40000 and paddle1_y < SCREEN_HEIGHT - PADDLE_SIZE:
        paddle1_y += 1
    elif joystick1.value < 20000 and paddle1_y > 0:
        paddle1_y -= 1

    if joystick2.value > 40000 and paddle2_y < SCREEN_HEIGHT - PADDLE_SIZE:
        paddle2_y += 1
    elif joystick2.value < 20000 and paddle2_y > 0:
        paddle2_y -= 1


    # ----- AUTOMATIC BALL MOVEMENT -----
    if y == 0 or y == SCREEN_HEIGHT - 1:
        vel_y = -vel_y
    if hit_paddle(x + vel_x, y + vel_y):
        vel_x = -vel_x

    # ----- UPDATE SCORES -----
    if x <= 0:
        score2 += 1
        lcd.clear()
        p2_scoreString = "SCORE 2: " + str(score2)
        lcd.write_string(p1_scoreString)
        lcd.cursor_pos = (1, 0)
        lcd.write_string(p2_scoreString)
        reset()
    if x >= SCREEN_WIDTH - 1:
        score1 += 1
        lcd.clear()
        p1_scoreString = "SCORE 1: " + str(score1)
        lcd.write_string(p1_scoreString)
        lcd.cursor_pos = (1, 0)
        lcd.write_string(p2_scoreString)
        reset()

    x += vel_x
    y += vel_y


    # ----- DRAWING -----

    # Light up for "1 frame"
    for i in range(100):
        # Alternate between paddle1, paddle2, and ball
        paddle1()
        all_shift(xstring, ystring, dataPINs, clockPIN, latchPIN)
        paddle2()
        all_shift(xstring, ystring, dataPINs, clockPIN, latchPIN)
        ball()
        all_shift(xstring, ystring, dataPINs, clockPIN, latchPIN)

