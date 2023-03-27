import pygame
pygame.init()


# --------------- GLOBAL CONSTANTS --------------
# Define some colors
BLACK = ( 0, 0, 0)
WHITE = ( 255, 255, 255)
GREEN = ( 0, 255, 0)
RED = ( 255, 0, 0)

SQUARE_SIZE = 30
SCREEN_WIDTH = 24
SCREEN_HEIGHT = 15

PADDLE_SIZE  = 3

# ----------------- Setup ---------------------------
size = (SCREEN_WIDTH*SQUARE_SIZE, SCREEN_HEIGHT*SQUARE_SIZE)
screen = pygame.display.set_mode(size)
pygame.display.set_caption("Pong simulator")

carryOn = True
clock = pygame.time.Clock()


color = RED

# ---------------- functions ------------------
def rect(x, y, color):
  pygame.draw.rect(screen, color, [x*SQUARE_SIZE, y*SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE], 0)
  
def change_color(color):
  if color == RED:
    return GREEN
  else:
    return RED


# -------------- VARIABLES -----------------
x = 0
y = 0

paddle1_y = 0
paddle2_y = 0


def paddle1():
  for i in range(PADDLE_SIZE):
    rect(0, paddle1_y + i, RED)


def paddle2():
  for i in range(PADDLE_SIZE):
    rect(SCREEN_WIDTH - 1, paddle2_y + i, RED)


def ball():
  rect(x, y, GREEN)


while carryOn:

  # pygame.time.delay(150)
  for event in pygame.event.get(): # user did something
    if event.type == pygame.QUIT: # if closed click
      carryOn = False # exit while loop 

  # ---- Game logic ------
  keys = pygame.key.get_pressed()

  # up and down keys control RED paddle
  if keys[pygame.K_s] and paddle1_y < SCREEN_HEIGHT - PADDLE_SIZE:
    paddle1_y += 1
  elif keys[pygame.K_w] and paddle1_y > 0:
    paddle1_y -= 1

  if keys[pygame.K_DOWN] and paddle2_y < SCREEN_HEIGHT - PADDLE_SIZE:
    paddle2_y += 1
  elif keys[pygame.K_UP] and paddle2_y > 0:
    paddle2_y -= 1

  # ----- Drawing --------

  # background black
  screen.fill(BLACK)

  #  only one rect per refresh
  # rect(x, y, color)

  paddle1()
  paddle2()

  ball()


  pygame.display.update()

  # 60 frames per second
  clock.tick(90)


pygame.quit()