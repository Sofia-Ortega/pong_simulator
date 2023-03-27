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

paddle_y = 0

def paddleCoordinates():
  arr = []
  for i in range(PADDLE_SIZE):
    arr.append(paddle_y + i)

  print(arr)
  return arr 




while carryOn:

  # pygame.time.delay(150)
  for event in pygame.event.get(): # user did something
    if event.type == pygame.QUIT: # if closed click
      carryOn = False # exit while loop 

  # ---- Game logic ------
  keys = pygame.key.get_pressed()

  if keys[pygame.K_DOWN] and paddle_y < SCREEN_HEIGHT - PADDLE_SIZE - 1:
    paddle_y += 1
  elif keys[pygame.K_UP] and paddle_y > 0:
    paddle_y -= 1
  # ----- Move box with KEYS -------------
  # if keys[pygame.K_RIGHT]:
  #   color = change_color(color)
  #   x += 1
  # elif keys[pygame.K_LEFT]:
  #   color = change_color(color)
  #   x -= 1
  # elif keys[pygame.K_UP]:
  #   color = change_color(color)
  #   y -= 1
  # elif keys[pygame.K_DOWN]:
  #   color = change_color(color)
  #   y += 1


  # drawing paddle
  if y not in paddleCoordinates():
    y = paddle_y
  else:
    y += 1

  # ----- Drawing --------

  # background black
  screen.fill(BLACK)

  #  only one rect per refresh
  rect(x, y, color)

  pygame.display.update()

  # 60 frames per second
  clock.tick(90)


pygame.quit()