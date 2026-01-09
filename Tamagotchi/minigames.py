import pygame
import random
import time
import os

# --- Constants ---
SCREEN_WIDTH = 480
SCREEN_HEIGHT = 320
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)

def bouncing_ball_game(screen, font):
    """
    A simple mini-game where the player clicks the ball to keep it bouncing.
    The game lasts for a fixed duration, and the score is based on clicks.
    Returns the final score.
    """
    
    # --- Initialize Mixer (if not already) ---
    if not pygame.mixer.get_init():
        pygame.mixer.init()

    # --- Load Music ---
    base_path = os.path.dirname(__file__)
    music_path = os.path.join(base_path, "assets", "audio", "play.wav")
    
    try:
        pygame.mixer.music.load(music_path)
        pygame.mixer.music.play(-1) # Play indefinitely
    except pygame.error as e:
        print(f"Warning: Could not load or play music file. Error: {e}")

    # --- Game State ---
    score = 0
    game_duration = 15.0 # seconds
    start_time = time.time()
    
    # --- Pet Properties ---
    pet_radius = 30
    pet_x = SCREEN_WIDTH // 2
    pet_y = SCREEN_HEIGHT // 2
    pet_vy = 0 # vertical velocity
    gravity = 0.5
    bounce_strength = -10
    
    clock = pygame.time.Clock()
    running = True
    
    while running:
        # --- Event Handling ---
        click_pos = None
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                # --- Stop Music ---
                pygame.mixer.music.stop() # Stop music on early exit
                return 0 # Return 0 if game is quit prematurely

            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                click_pos = event.pos
            elif event.type == pygame.FINGERDOWN:
                # Scale normalized touch coordinates to screen dimensions
                win_w, win_h = screen.get_size()
                click_pos = (int(event.x * win_w), int(event.y * win_h))

        if click_pos:
            distance = ((click_pos[0] - pet_x)**2 + (click_pos[1] - pet_y)**2)**0.5
            if distance <= pet_radius:
                pet_vy = bounce_strength
                score += 1

        # --- Game Logic ---
        # Apply gravity
        pet_vy += gravity
        pet_y += pet_vy
        
        # Bounce off top/bottom walls
        if pet_y - pet_radius < 0:
            pet_y = pet_radius
            pet_vy = 0
        if pet_y + pet_radius > SCREEN_HEIGHT:
            pet_y = SCREEN_HEIGHT - pet_radius
            pet_vy *= -0.7 # Lose some energy on bounce

        # --- Timer ---
        time_elapsed = time.time() - start_time
        time_left = game_duration - time_elapsed
        if time_left <= 0:
            running = False
            
        # --- Drawing ---
        screen.fill(BLACK)
        
        # Draw pet
        pygame.draw.circle(screen, GREEN, (int(pet_x), int(pet_y)), pet_radius)
        
        # Draw Score and Timer
        score_text = font.render(f"Score: {score}", True, WHITE)
        screen.blit(score_text, (10, 10))
        
        timer_text = font.render(f"Time: {int(time_left)}", True, WHITE)
        screen.blit(timer_text, (SCREEN_WIDTH - timer_text.get_width() - 10, 10))
        
        # --- Update Display ---
        pygame.display.flip()
        clock.tick(60)
        
    # --- Stop Music ---
    pygame.mixer.music.stop()
    return score