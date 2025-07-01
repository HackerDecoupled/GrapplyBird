# GRAPPLY HOOK V6
import pygame
import sys
import math
import random as rand

# Initialize Pygame
pygame.init()

# Constants
WIDTH, HEIGHT = 800, 600
GRAVITY = 0.5
HOOK_SPEED = 20
GROUND_HEIGHT = HEIGHT - 100  # Raised ground level

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN = (0, 128, 0)
RED = (255, 0, 0)
ORANGE = (235, 125, 52)
SOFT_RED = (181, 43, 43)

# Set up the display
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Grapply Bird")
clock = pygame.time.Clock()

# Player
player = pygame.Rect(WIDTH // 2, HEIGHT // 2, 40, 40)
player_speed_y = 0
hooked = False
hook_pos = (0, 0)
hook_direction = (0, 0)

# Player surface for rotation
player_surface = pygame.Surface((40, 40), pygame.SRCALPHA)
pygame.draw.rect(player_surface, RED, (5, 5, 40, 40))

# Start button
start_button_width, start_button_height = 100, 50
start_button = pygame.Rect((WIDTH - start_button_width) // 2, HEIGHT // 3, start_button_width, start_button_height)
start_button_color = GREEN
start_button_text = pygame.font.SysFont(None, 36).render("Start", True, BLACK)
start_button_text_rect = start_button_text.get_rect(center=start_button.center)

# Barrier setup
top_barrier = pygame.Rect(WIDTH, 0, 40, 0)
bottom_barrier = pygame.Rect(WIDTH, 0, 40, 0)
check_point = pygame.Rect(WIDTH, 0, 40, 0)
top_barrier_height = 50
bottom_barrier_height = 50
check_point_height = 50
total_barrier = 600

# Constants for barrier types
TOP_BARRIER = 0
BOTTOM_BARRIER = 1
CHECKPOINT_BARRIER = 2

#Barrier movement setup
iteration = 1
barrier_num = 0
barriers = []
increment = 20
current_top_barrier = []
current_bottom_barrier = []
current_checkpoint = []
current_bottom_barrier_height = 0
current_top_barrier_height = 0
current_checkpoint_height = 0

# Score setup
collided_top = False
collided_bottom = False
collided_checkpoint = False
score = 0
current_score = ""
score_font = pygame.font.SysFont(None, 36)
score_text = score_font.render(current_score, True, BLACK)
score_display_font = pygame.font.SysFont(None, 36).render("Score: ", True, BLACK)
scored = False

# Difficulty setup
speed = 15
easy_button_width, easy_button_height = 100, 50
easy_button = pygame.Rect((WIDTH - easy_button_width) // 3, HEIGHT // 2, easy_button_width, easy_button_height)
easy_button_color = GREEN
easy_button_text = pygame.font.SysFont(None, 36).render("Easy", True, BLACK)
easy_button_text_rect = easy_button_text.get_rect(center=easy_button.center)

medium_button_width, medium_button_height = 100, 50
medium_button = pygame.Rect((WIDTH - medium_button_width) // 2, HEIGHT // 2, medium_button_width, medium_button_height)
medium_button_color = ORANGE
medium_button_text = pygame.font.SysFont(None, 36).render("Medium", True, BLACK)
medium_button_text_rect = medium_button_text.get_rect(center=medium_button.center)

hard_button_width, hard_button_height = 100, 50
hard_button = pygame.Rect((WIDTH - hard_button_width) // 1.5, HEIGHT // 2, hard_button_width, hard_button_height)
hard_button_color = SOFT_RED
hard_button_text = pygame.font.SysFont(None, 36).render("Hard", True, BLACK)
hard_button_text_rect = hard_button_text.get_rect(center=hard_button.center)

select_button_text = pygame.font.SysFont(None, 36).render("Select a difficulty above", True, WHITE)
select_button_text_rect = select_button_text.get_rect()
select_button_text_rect.center = (WIDTH // 2, HEIGHT // 1.5)

current_mode = "Easy"  # Default mode

#Game is started as false so the start button and difficulty buttons show up
game_started = False

############ FUNCTIONS ##################

class Barrier:
    def __init__(self, rect, barrier_type):
        self.rect = rect
        self.type = barrier_type

# grappling hook logic
def hook():
    global hooked, hook_direction, player_speed_y
    direction = [hook_pos[0] - player.centerx, hook_pos[1] - player.centery]
    distance = math.sqrt(direction[0] ** 2 + direction[1] ** 2)

    # Normalize direction
    if distance != 0:
        direction = [direction[0] / distance, direction[1] / distance]

    # Update player position towards the cursor
    player.x += direction[0] * HOOK_SPEED
    player.y += direction[1] * HOOK_SPEED

    # Update hook direction for momentum
    hook_direction = (direction[0], direction[1])
        

# draw the hook line
def draw_hook():
    pygame.draw.line(screen, WHITE, player.center, hook_pos, 5)
    pygame.draw.circle(screen, WHITE, hook_pos, 5)

# Resets the game when the player "dies"
def reset(speedend, scoreend):
    global game_started, player_speed_y, hooked, hook_direction, increment, barrier_num, iteration, score, speed
    game_started = False
    hooked = False
    player_speed_y = 0
    hook_direction = (0, 0)
    player.x = WIDTH // 2 
    player.y = HEIGHT // 2
    increment = 20
    barriers.clear()
    barrier_num = 0
    iteration = 1
    score = 0
    if scoreend > 40 and speedend == 35:
        print("Amazing! You are a master of the hook! Final score:" + str(scoreend))
    elif scoreend > 30 and speedend == 25:
        print("Wow! You got a score of " + str(scoreend))
    elif scoreend > 20 and speedend == 15:
        print("Nice! Score of:" + str(scoreend))
    elif scoreend < 20:
        print("Score: " + str(scoreend))


# Initializes the top barrier
def draw_top_barrier():
    global top_barrier_height
    top_barrier_height = rand.randint(100, 250)
    top_barrier.x = WIDTH
    top_barrier.y = 0
    top_barrier.height = top_barrier_height
    barriers.append(Barrier(top_barrier.copy(), TOP_BARRIER))

# Initializes the bottom barrier
def draw_bottom_barrier():
    global bottom_barrier_height
    bottom_barrier_height = rand.randint(100, 250)
    bottom_barrier.x = WIDTH
    bottom_barrier.y = HEIGHT - bottom_barrier_height
    bottom_barrier.height = bottom_barrier_height
    barriers.append(Barrier(bottom_barrier.copy(), BOTTOM_BARRIER))

# Initializes the checkpoint
def draw_checkpoint_barrier():
    global check_point_height, bottom_barrier_height, top_barrier_height
    check_point_height = total_barrier - (top_barrier_height + bottom_barrier_height)
    check_point.x = WIDTH
    check_point.y = top_barrier_height
    check_point.height = check_point_height
    barriers.append(Barrier(check_point.copy(), CHECKPOINT_BARRIER))


# Moves all the barriers
def move_barriers(pos):
    global increment, barrier_num, iteration, score, current_score, score_text, score_font, scored
    for barrier_obj in barriers:
        barrier = barrier_obj.rect
        barrier.x = pos[0]
        if barrier_obj.type == TOP_BARRIER:
            pygame.draw.rect(screen, RED, barrier)
        elif barrier_obj.type == BOTTOM_BARRIER:
            pygame.draw.rect(screen, RED, barrier)
        elif barrier_obj.type == CHECKPOINT_BARRIER:
            pygame.draw.rect(screen, GREEN, barrier)
        
        if barrier.x < 0 or barrier.x > 800:
            increment = 20
            barriers.clear()
            barrier_num = 0
            iteration = 1
        
        collided_barrier = pygame.Rect.colliderect(player, barrier)
        if collided_barrier:
            if barrier_obj.type == CHECKPOINT_BARRIER:
                if scored == True:
                    score += 1
                    scored = False
                else:
                    scored = True
            elif barrier_obj.type == TOP_BARRIER or barrier_obj.type == BOTTOM_BARRIER:
                reset(speed, score)
            

#######################################
# Game loop
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                if hooked:
                    # Release the hook
                    hooked = False
                    player_speed_y = 0  # Reset player speed to avoid sudden drop
                elif game_started:
                    # Start grappling hook if game is started
                    hooked = True
                    hook_pos = pygame.mouse.get_pos()
        elif event.type == pygame.MOUSEBUTTONDOWN and not game_started:
            if start_button.collidepoint(event.pos):
                game_started = True
                print("Started game")
            elif easy_button.collidepoint(event.pos):
                speed = 15
                current_mode = "Easy"
                print("Speed set to easy mode")
            elif medium_button.collidepoint(event.pos):
                speed = 25
                current_mode = "Medium"
                print("Speed set to medium mode")
            elif hard_button.collidepoint(event.pos):
                speed = 35
                current_mode = "Hard"
                print("Speed set to hard mode")

    screen.fill(BLACK)

    if not game_started:
        # Draw start button
        pygame.draw.rect(screen, start_button_color, start_button)
        screen.blit(start_button_text, start_button_text_rect)
        # Draw easy button
        pygame.draw.rect(screen, easy_button_color, easy_button)
        screen.blit(easy_button_text, easy_button_text_rect)
        # Draw medium button
        pygame.draw.rect(screen, medium_button_color, medium_button)
        screen.blit(medium_button_text, medium_button_text_rect)
        # Draw hard button and select difficulty text
        pygame.draw.rect(screen, hard_button_color, hard_button)
        screen.blit(hard_button_text, hard_button_text_rect)
        screen.blit(select_button_text, select_button_text_rect)
        # Draw the current mode
        mode_text = score_font.render("Mode: " + current_mode, True, WHITE)
        screen.blit(mode_text, (20, 20))  # Display the mode
    if game_started:
        # Move player
        player_speed_y += GRAVITY
        player.y += player_speed_y

        # Check if player is on the ground
        if player.y > GROUND_HEIGHT:
            reset(speed, score)

        # Grappling hook logic
        player_pos = [player.centerx, player.centery]
        player_pos_x = [player_pos[0] - 30, player_pos[0] + 30]
        player_pos_y = [player_pos[1] - 30, player_pos[1] + 30]
        if hooked and ((player_pos_x[0] > hook_pos[0] or hook_pos[0] > player_pos_x[1]) or (player_pos_y[0] > hook_pos[1] and not hook_pos[1] > player_pos_y[1])):
            hook()
        elif hooked and ((player_pos_x[0] < hook_pos[0] and hook_pos[0] < player_pos_x[1]) and (player_pos_y[0] < hook_pos[1] and hook_pos[1] < player_pos_y[1])):
            hooked = False
            player_speed_y = 0
        else:
            # If not hooked, apply regular gravity
            hooked = False
            player.y += player_speed_y


        # Draw player with rotation
        rotated_player_surface = pygame.transform.rotate(player_surface, 0)  # No rotation
        player_rect = rotated_player_surface.get_rect(center=player.center)
        screen.blit(rotated_player_surface, player_rect.topleft)

        # If not hooked, continue with momentum
        if not hooked and game_started == True:
            player.x += hook_direction[0] * HOOK_SPEED 
            player.y += hook_direction[1] * HOOK_SPEED 

        if hooked:
            draw_hook()

        # EASY AND MEDIUM MODE
        if speed == 15 or speed == 25:
            # Draw barriers and make them move
            if barrier_num < 5 and iteration == 40:
                draw_top_barrier()
                draw_bottom_barrier()
                draw_checkpoint_barrier() 
                iteration = 1
                barrier_num += 1
            if len(barriers) != 0:
                pospos = [(750 - increment), 25]
                increment += speed
                move_barriers(pospos)
            if barrier_num > 5:
                barriers.clear()
                barrier_num = 0
            iteration += 1
        # HARD MODE
        if speed == 35 and score < 20:
            if barrier_num < 5 and iteration == 40:
                draw_top_barrier()
                draw_bottom_barrier()
                draw_checkpoint_barrier() 
                iteration = 1
                barrier_num += 1
            if len(barriers) != 0:
                pospos = [(750 - increment), 25]
                increment += speed
                move_barriers(pospos)
            if barrier_num > 5:
                barriers.clear()
                barrier_num = 0
            iteration += 1
        if speed == 35 and score >= 20:
            if barrier_num < 5 and iteration == 40:
                draw_top_barrier()
                draw_bottom_barrier()
                draw_checkpoint_barrier() 
                iteration = 1
                barrier_num += 1
            if len(barriers) != 0:
                pospos = [(0 + increment), 25]
                increment += speed
                move_barriers(pospos)
            if barrier_num > 5:
                barriers.clear()
                barrier_num = 0
            iteration += 1
        
        
        # Draw ground
        pygame.draw.line(screen, WHITE, (0, GROUND_HEIGHT), (WIDTH, GROUND_HEIGHT), 2)

        current_score = str(score)
        score_text = score_font.render("Score: " + current_score, True, WHITE)
        #screen.blit(score_display_font, (20, 20))  # Display "Score:"
        screen.blit(score_text, (20, 20))  # Display the score
        pygame.display.flip()  # Update the display

    pygame.display.flip()

    clock.tick(60)

