import pygame
pygame.init()


# --------------- GLOBAL CONSTANTS --------------
# Define some colors
BLACK = ( 0, 0, 0)
WHITE = ( 255, 255, 255)
GREEN = ( 0, 255, 0)
RED = ( 255, 0, 0)

SQUARE_SIZE = 30
SCREEN_WIDTH = 20 # 24
SCREEN_HEIGHT = 15 # 15

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
x = 10
y = 12

vel_x = 1
vel_y = 1

paddle1_y = 0
paddle2_y = 0

score1 = 0
score2 = 0


def paddle1():
  for i in range(PADDLE_SIZE):
    rect(0, paddle1_y + i, RED)


def paddle2():
  for i in range(PADDLE_SIZE):
    rect(SCREEN_WIDTH - 1, paddle2_y + i, RED)


def ball():
  rect(x, y, GREEN)


def hit_paddle1(x, y):

  if x != 0:
    return False
  
  for i in range(PADDLE_SIZE):
    if y == paddle1_y + i:
      return True
    
  return False

def hit_paddle2(x, y):
  if  x != SCREEN_WIDTH - 1:
    return False

  for i in range(PADDLE_SIZE):
    if y == paddle2_y + i:
      return True
    
  return False


def hit_paddle(x, y):
  return hit_paddle1(x, y) or hit_paddle2(x, y)

def reset():
  global x
  global y
  global vel_x
  global vel_y

  x = 10
  y = 12

  vel_x = 1
  vel_y = 1


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

  
  # ball

  # --- control ball with keys ---
  # if keys[pygame.K_i] and y > 0:
  #   y -= 1
  # elif keys[pygame.K_k] and y < SCREEN_HEIGHT - 1:
  #   y += 1
  
  # if keys[pygame.K_l] and x < SCREEN_WIDTH - 1:
  #   x += 1
  # elif keys[pygame.K_j] and x > 0:
  #   x -= 1
  
  # ---- automatic ball movement -----
  if y == 0 or y == SCREEN_HEIGHT - 1:
    vel_y = -vel_y
  if hit_paddle(x + vel_x, y + vel_y):
    vel_x = -vel_x
  
  if x <= 0:
    print("Lose 1", score1)
    score1 -= 1
    reset()
  if x >= SCREEN_WIDTH - 1:
    print("Lose 2", score2)
    score2 -= 1
    reset()


  x += vel_x
  y += vel_y




  # ----- Drawing --------

  # background black
  screen.fill(BLACK)

  #  only one rect per refresh
  # rect(x, y, color)

  paddle1()
  paddle2()

  ball()

  if (hit_paddle1(x, y)):
    print("Hit paddle 1")
  if (hit_paddle2(x, y)):
    print("Hit paddle 2")

  pygame.display.update()

  # 60 frames per second
  clock.tick(60)


pygame.quit()