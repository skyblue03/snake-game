import pygame
import random
import sys

# Initialize Pygame
pygame.init()

# Screen dimensions
width, height = 640, 480
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption('Fruit Effects Snake')

# Colors
black = (0, 0, 0)
white = (255, 255, 255)
red = (255, 0, 0)
green = (0, 255, 0)
blue = (0, 0, 255)
yellow = (255, 255, 0)  # For slow down food
orange = (255, 165, 0)  # For shrink food

# Snake initial position and body
snake_pos = [100, 50]
snake_body = [[100, 50], [90, 50], [80, 50]]

# Food initial random position
food_pos = [random.randrange(1, (width // 10)) * 10, random.randrange(1, (height // 10)) * 10]
food_spawn = True

# Special food variables
speed_boost_food_pos = []
slow_down_food_pos = []
shrink_food_pos = []

special_food_effect = False
effect_duration = 0

# Food spawn probabilities
speed_boost_chance = 10  # 10% chance
slow_down_chance = 10  # 10% chance
shrink_chance = 5  # 5% chance

# Direction and speed
direction = 'RIGHT'
change_to = direction
snake_speed = 15
clock = pygame.time.Clock()

# Score variable
score = 0

# Level variable
level = 1
level_up_score = 100  # Score threshold to level up

# High score variable
high_score = 0

# Pause flag
paused = False

# Load sound effects
food_sound = pygame.mixer.Sound('food.wav')
special_food_sound = pygame.mixer.Sound('special_food.wav')
game_over_sound = pygame.mixer.Sound('game_over.wav')

def show_score(color, font, size):
    score_font = pygame.font.SysFont(font, size)
    score_surface = score_font.render('Score: ' + str(score), True, color)
    score_rect = score_surface.get_rect()
    score_rect.midtop = (width / 2, 10)
    screen.blit(score_surface, score_rect)

def show_level(color, font, size):
    level_font = pygame.font.SysFont(font, size)
    level_surface = level_font.render('Level: ' + str(level), True, color)
    level_rect = level_surface.get_rect()
    level_rect.midtop = (width / 2, 40)
    screen.blit(level_surface, level_rect)

def game_over():
    global high_score, running, snake_pos, snake_body, food_pos, food_spawn, direction, change_to, score, level, snake_speed, paused
    pygame.mixer.Sound.play(game_over_sound)
    
    if score > high_score:
        high_score = score
    
    my_font = pygame.font.SysFont('times new roman', 50)
    game_over_surface = my_font.render('Your Score is: ' + str(score), True, red)
    high_score_surface = my_font.render('High Score: ' + str(high_score), True, red)
    restart_surface = my_font.render('Press R to Restart or Q to Quit', True, red)
    
    game_over_rect = game_over_surface.get_rect()
    high_score_rect = high_score_surface.get_rect()
    restart_rect = restart_surface.get_rect()
    
    game_over_rect.midtop = (width / 2, height / 4)
    high_score_rect.midtop = (width / 2, height / 3)
    restart_rect.midtop = (width / 2, height / 2)
    
    screen.fill(black)
    screen.blit(game_over_surface, game_over_rect)
    screen.blit(high_score_surface, high_score_rect)
    screen.blit(restart_surface, restart_rect)
    pygame.display.flip()
    
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:  # Restart game
                    # Reset game state
                    snake_pos = [100, 50]
                    snake_body = [[100, 50], [90, 50], [80, 50]]
                    food_pos = [random.randrange(1, (width // 10)) * 10, random.randrange(1, (height // 10)) * 10]
                    food_spawn = True
                    direction = 'RIGHT'
                    change_to = direction
                    score = 0
                    level = 1
                    snake_speed = 15
                    paused = False
                    return
                elif event.key == pygame.K_q:  # Quit game
                    pygame.quit()
                    sys.exit()

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
            elif event.key == pygame.K_p:  # Pause/Resume game
                paused = not paused
    
    direction = change_to

    if not paused:
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
            pygame.mixer.Sound.play(food_sound)
            food_spawn = False
            score += 10  # Increase score by 10 for normal food
        else:
            snake_body.pop()
        
        # Food spawn
        if not food_spawn:
            food_pos = [random.randrange(1, (width // 10)) * 10, random.randrange(1, (height // 10)) * 10]
            food_spawn = True

        # Spawn special food occasionally
        if not special_food_effect:
            if random.randint(1, 100) <= speed_boost_chance:  # Speed boost food
                speed_boost_food_pos = [random.randrange(1, (width // 10)) * 10, random.randrange(1, (height // 10)) * 10]
                special_food_effect = 'speed'
            elif random.randint(1, 100) <= slow_down_chance:  # Slow down food
                slow_down_food_pos = [random.randrange(1, (width // 10)) * 10, random.randrange(1, (height // 10)) * 10]
                special_food_effect = 'slow'
            elif random.randint(1, 100) <= shrink_chance:  # Shrink food
                shrink_food_pos = [random.randrange(1, (width // 10)) * 10, random.randrange(1, (height // 10)) * 10]
                special_food_effect = 'shrink'

        # Handle eating special food
        if special_food_effect == 'speed' and snake_pos == speed_boost_food_pos:
            pygame.mixer.Sound.play(special_food_sound)
            effect_duration = 50  # Number of frames the effect lasts
            speed_boost_food_pos = []
            snake_speed = 30  # Increased speed
            special_food_effect = False

        elif special_food_effect == 'slow' and snake_pos == slow_down_food_pos:
            pygame.mixer.Sound.play(special_food_sound)
            effect_duration = 50
            slow_down_food_pos = []
            snake_speed = 10  # Decreased speed
            special_food_effect = False

        elif special_food_effect == 'shrink' and snake_pos == shrink_food_pos:
            pygame.mixer.Sound.play(special_food_sound)
            effect_duration = 0  # No duration, instant effect
            shrink_food_pos = []
            if len(snake_body) > 3:  # Ensure the snake doesn't shrink below a minimum length
                snake_body.pop()
            special_food_effect = False

        # Apply effects
        if effect_duration > 0:
            effect_duration -= 1
        else:
            snake_speed = 15  # Normal speed

        # Update level based on score
        if score >= level * level_up_score:
            level += 1
            snake_speed += 5  # Increase speed as level increases

        # Game Over conditions
        if snake_pos[0] < 0 or snake_pos[0] >= width or snake_pos[1] < 0 or snake_pos[1] >= height:
            game_over()
        for block in snake_body[1:]:
            if snake_pos == block:
                game_over()

        # Refresh game screen
        screen.fill(black)

        # Draw snake
        for pos in snake_body:
            pygame.draw.rect(screen, green, pygame.Rect(pos[0], pos[1], 10, 10))
        
        # Draw food
        pygame.draw.rect(screen, red, pygame.Rect(food_pos[0], food_pos[1], 10, 10))
        
        # Draw special food
        if special_food_effect == 'speed':
            pygame.draw.rect(screen, blue, pygame.Rect(speed_boost_food_pos[0], speed_boost_food_pos[1], 10, 10))
        elif special_food_effect == 'slow':
            pygame.draw.rect(screen, yellow, pygame.Rect(slow_down_food_pos[0], slow_down_food_pos[1], 10, 10))
        elif special_food_effect == 'shrink':
            pygame.draw.rect(screen, orange, pygame.Rect(shrink_food_pos[0], shrink_food_pos[1], 10, 10))

        # Display score
        show_score(white, 'times new roman', 20)
        
        # Display level
        show_level(white, 'times new roman', 20)
    else:
        # Display pause message
        pause_font = pygame.font.SysFont('times new roman', 50)
        pause_surface = pause_font.render('Game Paused', True, red)
        pause_rect = pause_surface.get_rect()
        pause_rect.midtop = (width / 2, height / 2)
        screen.blit(pause_surface, pause_rect)
        pygame.display.flip()

    # Update display
    pygame.display.update()

    # Frame rate
    clock.tick(snake_speed)

# Quit Pygame
pygame.quit()
sys.exit()
