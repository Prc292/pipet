import os
import sys
import platform
import pygame
from constants import *
from models import PetState
from pet_entity import Pet

class GameEngine:
    """Main wrapper for the primary game loop ."""
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SCALED | pygame.RESIZABLE)
        self.clock, self.font = pygame.time.Clock(), pygame.font.Font(None, 22)
        
        self.pet = Pet()
        self.pet.load()

        # UI Hitboxes
        self.btn_feed = pygame.Rect(20, 250, 100, 40)
        self.btn_play = pygame.Rect(135, 250, 100, 40)
        self.btn_sleep = pygame.Rect(250, 250, 100, 40)
        self.btn_quit = pygame.Rect(365, 250, 100, 40)

    def draw_bar(self, x, y, value, color, label):
        self.screen.blit(self.font.render(label, True, COLOR_TEXT), (x, y - 18))
        pygame.draw.rect(self.screen, COLOR_UI_BAR_BG, (x, y, 100, 12), border_radius=6)
        if value > 5:
            pygame.draw.rect(self.screen, color, (x, y, int(value), 12), border_radius=6)

    def run(self):
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT: running = False
                if event.type == pygame.MOUSEBUTTONDOWN and self.pet.is_alive:
                    if self.btn_feed.collidepoint(event.pos):
                        self.pet.stats.hunger = self.pet.stats.clamp(self.pet.stats.hunger - 20)
                        self.pet.transition_to(PetState.EATING)
                    elif self.btn_play.collidepoint(event.pos):
                        self.pet.stats.happiness = self.pet.stats.clamp(self.pet.stats.happiness + 20)
                        self.pet.stats.energy = self.pet.stats.clamp(self.pet.stats.energy - 10)
                    elif self.btn_sleep.collidepoint(event.pos):
                        new_state = PetState.IDLE if self.pet.state == PetState.SLEEPING else PetState.SLEEPING
                        self.pet.transition_to(new_state)
                    elif self.btn_quit.collidepoint(event.pos): running = False

            self.pet.update()
            if self.pet.state == PetState.EATING and self.pet.state_timer > 3.0:
                self.pet.transition_to(PetState.IDLE)

            self.screen.fill(COLOR_BG)
            self.draw_bar(20, 35, self.pet.stats.health, COLOR_HEALTH, "HEALTH")
            self.draw_bar(135, 35, 100 - self.pet.stats.hunger, COLOR_HUNGER, "FULLNESS")
            self.draw_bar(250, 35, self.pet.stats.happiness, COLOR_HAPPY, "HAPPY")
            self.draw_bar(365, 35, self.pet.stats.energy, COLOR_ENERGY, "ENERGY")

            cx, cy = SCREEN_WIDTH // 2, 160
            if self.pet.life_stage == "EGG":
                pygame.draw.ellipse(self.screen, (245, 245, 210), (cx-25, cy-35, 50, 70))
            else:
                self.pet.draw(self.screen, cx, cy)

            # --- Dynamic Buttons ---
            buttons = [
                (self.btn_feed, "FEED"),
                (self.btn_play, "PLAY"),
                (self.btn_sleep, "SLEEP" if self.pet.state != PetState.SLEEPING else "WAKE"),
                (self.btn_quit, "QUIT")
            ]
            for rect, txt in buttons:
                pygame.draw.rect(self.screen, COLOR_BTN, rect, border_radius=8)
                text_surf = self.font.render(txt, True, (255, 255, 255))
                self.screen.blit(text_surf, text_surf.get_rect(center=rect.center))

            pygame.display.flip()
            self.clock.tick(FPS)

        self.pet.save()
        pygame.quit()
        sys.exit()

if __name__ == "__main__":
    GameEngine().run()