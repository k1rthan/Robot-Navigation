import pygame
import math
import random


pygame.init()

# Screen Setup
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Robot Navigation")

# Robot Specifications
robot_pos = [100, 100]  
robot_radius = 10        
LINEAR_VELOCITY = 3      
SENSOR_RANGE = 20        

# Directions: Right, Down, Left, Up
DIRECTIONS = [(1, 0), (0, 1), (-1, 0), (0, -1)]

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
VIOLET = (138, 43, 226)  
BUTTON_COLOR = (0, 128, 0)
BUTTON_HOVER_COLOR = (0, 180, 0)
TEXT_COLOR = (255, 255, 255)

# Generate 10 Obstacles
def generate_obstacles():
    return [(random.randint(50, WIDTH - 50), random.randint(50, HEIGHT - 50)) for _ in range(10)]

obstacles = generate_obstacles()

def draw_robot(pos, direction):
    
    pygame.draw.circle(screen, RED, (int(pos[0]), int(pos[1])), robot_radius)

    
    end_x = pos[0] + (robot_radius + 10) * direction[0]
    end_y = pos[1] + (robot_radius + 10) * direction[1]
    pygame.draw.line(screen, VIOLET, pos, (end_x, end_y), 3)

def draw_obstacles():
    
    for obs in obstacles:
        pygame.draw.circle(screen, BLACK, obs, 15)

# Check if an obstacle is within sensor range.
def detect_obstacle_in_direction(pos, direction):
    
    dx, dy = direction
    check_x = pos[0] + SENSOR_RANGE * dx
    check_y = pos[1] + SENSOR_RANGE * dy

    # Ensure the robot doesn't leave boundary
    if not (0 <= check_x <= WIDTH and 0 <= check_y <= HEIGHT):
        return True  # Treat out-of-bounds as an obstacle

    # Check if any obstacle is within sensor range in that direction
    for obs in obstacles:
        distance = math.hypot(obs[0] - check_x, obs[1] - check_y)
        if distance <= SENSOR_RANGE:
            return True 
    return False  

def get_free_direction(pos):
    
    free_directions = [d for d in DIRECTIONS if not detect_obstacle_in_direction(pos, d)]
    return random.choice(free_directions) if free_directions else None

def move_robot(pos, direction):
    
    dx, dy = direction
    pos[0] = (pos[0] + LINEAR_VELOCITY * dx) % WIDTH
    pos[1] = (pos[1] + LINEAR_VELOCITY * dy) % HEIGHT

def reset_button(x, y, width, height, text, hover):
    
    color = BUTTON_HOVER_COLOR if hover else BUTTON_COLOR
    pygame.draw.rect(screen, color, (x, y, width, height))
    font = pygame.font.Font(None, 36)
    text_surface = font.render(text, True, TEXT_COLOR)
    text_rect = text_surface.get_rect(center=(x + width / 2, y + height / 2))
    screen.blit(text_surface, text_rect)

# Reset robot to starting position
def reset_simulation():
    
    global robot_pos, obstacles, current_direction
    robot_pos = [100, 100]  
    obstacles = generate_obstacles() 
    current_direction = (1, 0)  


running = True
clock = pygame.time.Clock()  
current_direction = (1, 0)  

while running:
    screen.fill(WHITE)

    
    mouse_pos = pygame.mouse.get_pos()
    mouse_click = pygame.mouse.get_pressed()

    
    draw_obstacles()
    draw_robot(robot_pos, current_direction)


    button_hover = 650 <= mouse_pos[0] <= 750 and 10 <= mouse_pos[1] <= 50
    reset_button(650, 10, 100, 40, "Reset", button_hover)

    
    if button_hover and mouse_click[0]:
        reset_simulation()

    
    if detect_obstacle_in_direction(robot_pos, current_direction):
        new_direction = get_free_direction(robot_pos)
        if new_direction:
            current_direction = new_direction  
        else:
            print("Robot is stuck! Game over.")
            running = False  
    
    move_robot(robot_pos, current_direction)

    pygame.display.flip()  

    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    clock.tick(30)  

pygame.quit()
