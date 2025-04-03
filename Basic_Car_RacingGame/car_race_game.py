import pygame
import random
import time

# Initialize pygame
pygame.init()

# Define colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (213, 50, 80)
GREEN = (0, 255, 0)
BLUE = (50, 153, 213)

# Set up the screen
WIDTH = 400
HEIGHT = 200
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Car Racing Game")

# Define car properties
car_width = 30
car_height = 15

# Load the car image (replace 'car.png' with your car image path)
car_img = pygame.image.load('car.jpg')
car_img = pygame.transform.scale(car_img, (car_width, car_height))  # Scale it to fit the car size

# Set up the clock
clock = pygame.time.Clock()

# Load background music
pygame.mixer.music.load('background_music.mp3')
pygame.mixer.music.play(-1, 0.0)  # Loop indefinitely

# Load sound effects
collision_sound = pygame.mixer.Sound('collision_sound.wav')
score_sound = pygame.mixer.Sound('score_sound.wav')

# Define font for scoring
font_style = pygame.font.SysFont("bahnschrift", 25)

# Game variables
score = 0
game_over = False

# Function to display the score
def display_score(score):
    value = font_style.render("Score: " + str(score), True, BLACK)
    screen.blit(value, [10, 10])

# Function to display the game over screen
def display_game_over():
    game_over_text = font_style.render("You Lost! Press Q-Quit or C-Play Again", True, RED)
    screen.blit(game_over_text, [WIDTH / 6, HEIGHT / 3])

# Function to move the car
def move_car(x, y, car_width, car_height):
    screen.blit(car_img, (x, y))

# Function to create obstacles
def create_obstacles():
    obstacle_width = 50
    obstacle_height = 60
    obstacle_x = random.randrange(0, WIDTH - obstacle_width)
    obstacle_y = -600
    return [obstacle_x, obstacle_y, obstacle_width, obstacle_height]

# Main game loop
def game_loop():
    global score
    global game_over
    x = WIDTH / 2 - car_width / 2
    y = HEIGHT - car_height - 10
    x_change = 0
    speed = 20
    obstacles = []
    obstacle_speed = 4

    # Game loop
    while not game_over:
        screen.fill(BLUE)
        
        # Handle events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_over = True
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    x_change = -speed
                if event.key == pygame.K_RIGHT:
                    x_change = speed
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                    x_change = 0
        
        # Move the car
        x += x_change

        # Check boundaries for car movement
        if x < 0:
            x = 0
        if x > WIDTH - car_width:
            x = WIDTH - car_width

        # Add obstacles
        if len(obstacles) < 1:
            obstacles.append(create_obstacles())

        # Move obstacles and check for collision
        for obstacle in obstacles:
            obstacle[1] += obstacle_speed
            pygame.draw.rect(screen, RED, (obstacle[0], obstacle[1], obstacle[2], obstacle[3]))

            # Check for collision
            if y < obstacle[1] + obstacle[3]:
                if x > obstacle[0] and x < obstacle[0] + obstacle[2] or \
                   x + car_width > obstacle[0] and x + car_width < obstacle[0] + obstacle[2]:
                    collision_sound.play()  # Play collision sound
                    game_over = True

            if obstacle[1] > HEIGHT:
                obstacles.remove(obstacle)
                score += 1  # Increase score for every obstacle avoided
                score_sound.play()  # Play score sound

        move_car(x, y, car_width, car_height)

        # Increase obstacle speed based on score
        obstacle_speed = 4 + (score // 5)  # Increase speed for every 5 points

        # Display score
        display_score(score)

        # Game Over screen
        if game_over:
            display_game_over()
            pygame.display.update()
            time.sleep(2)  # Show game over message for 2 seconds

        pygame.display.update()
        clock.tick(60)  # 60 frames per second

# Start the game loop
game_loop()

# Quit the game
pygame.quit()
quit()
