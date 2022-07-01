import pygame
import random

pygame.init()

width, height = 640, 480
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption('Fruit Effects Snake')

black = (0, 0, 0)
white = (255, 255, 255)
red = (255, 0, 0)
green = (0, 255, 0)

# Snake position and body
snake_pos = [100, 50]
snake_body = [[100, 50], [90, 50], [80, 50]]

# Food random position
food_pos = [random.randrange(1, (width // 10)) * 10, random.randrange(1, (height // 10)) * 10]
food_spawn = True
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    
    # Refresh game screen
    screen.fill(black)
    pygame.display.flip()

    # Frame rate
    pygame.time.Clock().tick(30)  # 30 frames per second
