import pygame
import random

pygame.init()

width, height = 640, 480
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption('Fruit Snake')

black = (0, 0, 0)
white = (255, 255, 255)
red = (255, 0, 0)
green = (0, 255, 0)
blue = (0, 0, 255)  # Added blue color for special food

# Snake position and body
snake_pos = [100, 50]
snake_body = [[100, 50], [90, 50], [80, 50]]

# Food random position
food_pos = [random.randrange(1, (width // 10)) * 10, random.randrange(1, (height // 10)) * 10]
food_spawn = True

# Special food variables
special_food_pos = []
special_food_effect = False
effect_duration = 0

# Direction and speed
direction = 'RIGHT'
change_to = direction
snake_speed = 15
clock = pygame.time.Clock()

# Game loop flag
running = True

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP and direction != 'DOWN':
                change_to = 'UP'
            elif event.key == pygame.K_DOWN and direction != 'UP':
                change_to = 'DOWN'
            elif event.key == pygame.K_LEFT and direction != 'RIGHT':
                change_to = 'LEFT'
            elif event.key == pygame.K_RIGHT and direction != 'LEFT':
                change_to = 'RIGHT'
    
    direction = change_to

    # Move the snake
    if direction == 'UP':
        snake_pos[1] -= 10
    elif direction == 'DOWN':
        snake_pos[1] += 10
    elif direction == 'LEFT':
        snake_pos[0] -= 10
    elif direction == 'RIGHT':
        snake_pos[0] += 10

    # Snake body growing mechanism
    snake_body.insert(0, list(snake_pos))
    if snake_pos == food_pos:
        food_spawn = False
    else:
        snake_body.pop()
    
    # Food spawn
    if not food_spawn:
        food_pos = [random.randrange(1, (width // 10)) * 10, random.randrange(1, (height // 10)) * 10]
        food_spawn = True

    # Spawn special food occasionally
    if not special_food_effect and random.randint(1, 20) == 1:  # 5% chance of spawning special food
        special_food_pos = [random.randrange(1, (width // 10)) * 10, random.randrange(1, (height // 10)) * 10]
        special_food_effect = True

    # Handle eating special food
    if snake_pos == special_food_pos:
        effect_duration = 50  # Number of frames the effect lasts
        special_food_effect = False
        special_food_pos = []

    # Apply effects
    if effect_duration > 0:
        snake_speed = 30  # Increased speed
        effect_duration -= 1
    else:
        snake_speed = 15  # Normal speed

    # Game Over conditions
    if snake_pos[0] < 0 or snake_pos[0] >= width or snake_pos[1] < 0 or snake_pos[1] >= height:
        running = False
    for block in snake_body[1:]:
        if snake_pos == block:
            running = False

    # Refresh game screen
    screen.fill(black)

    # Draw snake
    for pos in snake_body:
        pygame.draw.rect(screen, green, pygame.Rect(pos[0], pos[1], 10, 10))
    
    # Draw food
    pygame.draw.rect(screen, red, pygame.Rect(food_pos[0], food_pos[1], 10, 10))
    
    # Draw special food
    if special_food_effect:
        pygame.draw.rect(screen, blue, pygame.Rect(special_food_pos[0], special_food_pos[1], 10, 10))

    # Update display
    pygame.display.update()

    # Frame rate
    clock.tick(snake_speed)

# Quit Pygame
pygame.quit()
