import pygame
import random
from pygame.locals import (
    K_UP,
    K_ESCAPE,
    K_w,
    K_SPACE,
    QUIT
)
pygame.init()

# Setup variables
clock = pygame.time.Clock()
screen = pygame.display.set_mode((800, 600))
ACCEL = 0.15
PIPE_HEIGHTS = [0, 200, 400]
SPEED = 1
velocity = 0

# Create spawnpipe events
SPAWNPIPE = pygame.USEREVENT
pygame.time.set_timer(SPAWNPIPE, 3000)

# Rect takes a tuple, x-pos, y-pos, width, height
player = pygame.Rect((50, 250, 50, 50))


running = True

obstacles = []
def make_pipes():
    pos = random.choice(PIPE_HEIGHTS)

    if (pos == 0):
        bottom_height = 200
        top_height = 400

    elif (pos == 200):
        bottom_height = 400
        top_height = 0

    elif (pos == 400):
        bottom_height = 200
        top_height = 200

    
    bottom_pipe = pygame.Rect((725, pos, 75, bottom_height))
    top_pipe = pygame.Rect((725, 0, 75, top_height))
    obstacles.append((bottom_pipe, top_pipe))


def render_pipes():
    for pipe in obstacles:
        pygame.draw.rect(screen, (255, 0, 0), pipe[0])
        pygame.draw.rect(screen, (255, 0, 0), pipe[1])

def move_pipes():
    for pipe in obstacles:
        # Move in-place
        pipe[0].move_ip(-SPEED, 0)
        pipe[1].move_ip(-SPEED, 0)

def delete_pipes():
    # Reversed important here
    for index in reversed(range(0, len(obstacles))):
        if obstacles[index][0].x <= 0:
            obstacles.pop(index)


def check_collisions():
    for pipe in obstacles:
        if (player.colliderect(pipe[0])) or (player.colliderect(pipe[1])):
            return True
        else:
            return False


while running: 
    screen.fill((0, 0, 0))
    pygame.draw.rect(screen, (0, 0, 255), player)
    render_pipes()
    move_pipes()
    is_hit = check_collisions()
    if is_hit == True:
        running = False
    delete_pipes() 


    key = pygame.key.get_pressed() # Check if keys are pressed
    if (key[K_w] == True) or (key[K_UP] == True) or (key[K_SPACE] == True): # If W, Up arrow, or space bars are pressed
            player.move_ip(0, -5) # Then move up
            velocity = 0 # Set downwards velocity to 0
    else:
        if (player.y >= 550):
            # This is the floor, if the player is 
            player.move_ip(0, 0)
            velocity = 0
        else: 
            # Fall
            player.move_ip(0, velocity) 
            velocity += ACCEL
    
    if (key[K_ESCAPE] == True): # Key hit was escape key
        running = False


    
    
    for event in pygame.event.get():
        if event.type == QUIT:
            running = False
        if event.type == SPAWNPIPE:
            make_pipes()

    pygame.display.update()
    clock.tick(120)


pygame.quit()