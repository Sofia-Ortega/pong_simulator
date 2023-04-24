import RPi.GPIO as GPIO
import sys
import pygame

# --------------- GLOBAL CONSTANTS --------------
SCREEN_WIDTH = 24
SCREEN_HEIGHT = 16

PADDLE_SIZE  = 3

# -------------- PINS -----------------
dataPINs = [5, 6, 13, 19, 26]
latchPIN = 20
clockPIN = 21

# -------------- VARIABLES -----------------
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

# Strings representing which rows and columns are on
xstring = str("0") * 24
ystring = str("0") * 16

# ----------------- Setup ---------------------------
carryOn = True
GPIO.setmode(GPIO.BCM)
GPIO.setup(
  (
    dataPINs[0], 
    dataPINs[1], 
    dataPINs[2], 
    dataPINs[3], 
    dataPINs[4], 
    latchPIN, 
    clockPIN
  ), GPIO.OUT)

# ---------------- FUNCTIONS ------------------

# Logic for loading the row and column strings into the shift registers
def all_shift(xinput, yinput, data, clock, latch):
  # Put latch down to start data sending
  GPIO.output(clock,0)
  GPIO.output(latch,0)
  GPIO.output(clock,1)

  # Load data in reverse order
  for i in range(7, -1, -1):
    GPIO.output(clock, 0)

    # Load register x1
    GPIO.output(data[0], int(xinput[i]) ^ 1) # Negate because column supplies ground
    # Load register x2
    GPIO.output(data[1], int(xinput[8 + i]) ^ 1)
    # Load register x3
    GPIO.output(data[2], int(xinput[16 + i]) ^ 1)
    # Load register y1
    GPIO.output(data[3], int(yinput[i]))
    # Load register y2
    GPIO.output(data[4], int(yinput[8 + i]))

    # Send clock signal to shift the inputs
    GPIO.output(clock,1)

  # Put latch up to store data on register
  GPIO.output(clock,0)
  GPIO.output(latch,1)
  GPIO.output(clock,1)


# Set the row and column strings to all 0s
def resetStrings():
  global xstring 
  global ystring
  xstring = str("0") * 24
  ystring = str("0") * 16


# Update the row and column strings to turn on a desired LED
def updateStrings(xCoord, yCoord):
  global xstring
  global ystring
  xstring = xstring[0:xCoord] + "1" + xstring[xCoord + 1:]
  ystring = ystring[0:yCoord] + "1" + ystring[yCoord + 1:]


# Set player1 paddle on
def paddle1():
  for i in range(PADDLE_SIZE):
    updateStrings(0, paddle1_y + i)


# Set player2 paddle on
def paddle2():
  for i in range(PADDLE_SIZE):
    updateStrings(SCREEN_WIDTH - 1, paddle2_y + i)


# Set ball on
def ball():
  updateStrings(x, y)


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


# ---------------- MAIN ------------------
while carryOn:

  pygame.time.delay(100)
  for event in pygame.event.get(): # user did something
    if event.type == pygame.QUIT: # if closed click
      carryOn = False # exit while loop 

  # ---- Game logic ------
  keys = pygame.key.get_pressed()

  # left paddle 
  if keys[pygame.K_s] and paddle1_y < SCREEN_HEIGHT - PADDLE_SIZE:
    paddle1_y += 1
  elif keys[pygame.K_w] and paddle1_y > 0:
    paddle1_y -= 1

  # right paddle
  if keys[pygame.K_DOWN] and paddle2_y < SCREEN_HEIGHT - PADDLE_SIZE:
    paddle2_y += 1
  elif keys[pygame.K_UP] and paddle2_y > 0:
    paddle2_y -= 1


  # ---- automatic ball movement -----
  if y == 0 or y == SCREEN_HEIGHT - 1:
    vel_y = -vel_y
  if hit_paddle(x + vel_x, y + vel_y):
    vel_x = -vel_x
  
  if x <= 0:
    score2 += 1
    print("Player 2 scored!", score2)
    reset()
  if x >= SCREEN_WIDTH - 1:
    score1 += 1
    print("Player 1 scored!", score1)
    reset()


  x += vel_x
  y += vel_y




  # ----- Drawing --------

  # Reset strings
  resetStrings()

  for i in range(100):

    # Set LED encoding for paddles and ball
    paddle1()
    all_shift(xstring, ystring, dataPINs, clockPIN, latchPIN)
    resetStrings()
    paddle2()
    all_shift(xstring, ystring, dataPINs, clockPIN, latchPIN)
    resetStrings()
    ball()
    all_shift(xstring, ystring, dataPINs, clockPIN, latchPIN)

  if (hit_paddle1(x, y)):
    print("Hit paddle 1")
  if (hit_paddle2(x, y)):
    print("Hit paddle 2")

  # Load LED encoding into the shift registers
  all_shift(xstring, ystring, dataPINs, clockPIN, latchPIN)


pygame.quit()