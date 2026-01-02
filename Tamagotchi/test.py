#!/usr/bin/env python3
import os
import sys
import time
import json
import platform
import pygame
import math
import random
import signal

# Configure mixer pre-init from environment to reduce resampling and underruns on Pi
_AUDIO_FREQ = int(os.getenv("TAMAGOTCHI_AUDIO_FREQ", "22050"))
_AUDIO_CHANNELS = int(os.getenv("TAMAGOTCHI_AUDIO_CHANNELS", "2"))
_AUDIO_BUFFER = int(os.getenv("TAMAGOTCHI_AUDIO_BUF", "512"))
try:
    pygame.mixer.pre_init(_AUDIO_FREQ, -16, _AUDIO_CHANNELS, _AUDIO_BUFFER)
except Exception:
    pass

SCREEN_WIDTH = 480
SCREEN_HEIGHT = 320
FPS = 30
SAVE_FILE = "pet_save.json"
TIME_SCALE = float(os.getenv("TAMAGOTCHI_TIME_SCALE", "1.0"))

def is_raspberry_pi() -> bool:
    if os.getenv("TAMAGOTCHI_FORCE_PI", "") == "1":
        return True
    try:
        with open("/proc/device-tree/model", "r") as f:
            if "Raspberry Pi" in f.read():
                return True
    except Exception:
        pass
    try:
        with open("/proc/cpuinfo", "r") as f:
            cpu = f.read()
            if "BCM" in cpu or "Raspberry" in cpu:
                return True
    except Exception:
        pass
    return "arm" in platform.machine().lower()

MAX_CATCHUP_SECONDS = 4 * 3600

# Stats decay per hour
HUNGER_DECAY_PER_HOUR = 10.0
HAPPINESS_DECAY_PER_HOUR = 8.0
ENERGY_DECAY_PER_HOUR = 5.0
CLEANLINESS_DECAY_PER_HOUR = 6.0
CLEANLINESS_HEALTH_PENALTY_PER_HOUR = 2.5
HEALTH_DECAY_CONDITIONAL_PER_HOUR = 5.0

STAGE_YOUNG_SECONDS = 60
STAGE_ADULT_SECONDS = 300
STAGE_ELDER_SECONDS = 600

EVOLUTION_MIN_CARE = 50.0

HUNGER_ALERT = 80.0
CLEANLINESS_ALERT = 30.0
HEALTH_ALERT = 40.0
ENERGY_ALERT = 20.0
HAPPINESS_ALERT = 40.0

BADGE_PULSE_SPEED = 4.0
BADGE_PULSE_AMPLITUDE = 2
NOTIFY_COOLDOWN = 120.0
REACTION_DURATION_HUNGER = 2.0
REACTION_DURATION_CLEAN = 2.0

COLOR_BG = (30, 30, 50)
COLOR_TEXT = (255, 255, 255)
COLOR_UI_BG = (60, 60, 90)
COLOR_HEALTH = (0, 255, 0)
COLOR_HUNGER = (255, 0, 0)
COLOR_HAPPY = (255, 255, 0)

# -----------------------
# Pet Class
# -----------------------
class Pet:
    def __init__(self):
        self.hunger = 50.0
        self.happiness = 100.0
        self.energy = 100.0
        self.health = 100.0
        self.cleanliness = 100.0
        self.is_alive = True
        self.state = "HAPPY"
        self.birth_time = time.time()
        self.life_stage = "BABY"
        self.last_update = time.time()
        self.notified_needs = {}
        self.last_interaction = time.time()

    def update(self):
        if not self.is_alive:
            self.state = "DEAD"
            return
        now = time.time()
        elapsed = min(now - self.last_update, MAX_CATCHUP_SECONDS) * TIME_SCALE
        self.last_update = now

        # Hunger decay
        self.hunger = min(100.0, self.hunger + HUNGER_DECAY_PER_HOUR * elapsed / 3600)

        # Happiness decay faster if neglected
        elapsed_since_interaction = now - getattr(self, "last_interaction", now)
        decay = HAPPINESS_DECAY_PER_HOUR * elapsed / 3600
        if elapsed_since_interaction > 3600:
            decay *= 1.5
        if elapsed_since_interaction > 7200:
            decay *= 2.0
        self.happiness = max(0.0, self.happiness - decay)

        self.energy = max(0.0, self.energy - ENERGY_DECAY_PER_HOUR * elapsed / 3600)
        self.cleanliness = max(0.0, self.cleanliness - CLEANLINESS_DECAY_PER_HOUR * elapsed / 3600)

        if self.hunger > 80 or self.energy < 20:
            self.health = max(0.0, self.health - HEALTH_DECAY_CONDITIONAL_PER_HOUR * elapsed / 3600)
        if self.cleanliness < 30:
            self.health = max(0.0, self.health - CLEANLINESS_HEALTH_PENALTY_PER_HOUR * elapsed / 3600)

        age = now - self.birth_time
        prev_stage = self.life_stage
        if age >= STAGE_ELDER_SECONDS:
            candidate = "ELDER"
        elif age >= STAGE_ADULT_SECONDS:
            candidate = "ADULT"
        elif age >= STAGE_YOUNG_SECONDS:
            candidate = "YOUNG"
        else:
            candidate = "BABY"
        avg_care = (self.health + self.happiness)/2
        if candidate != prev_stage and avg_care >= EVOLUTION_MIN_CARE:
            self.life_stage = candidate

        if self.health <= 0:
            self.is_alive = False
        elif self.health < 40 or self.hunger > 90:
            self.state = "SICK"
        elif self.happiness < 40:
            self.state = "SAD"
        else:
            self.state = "HAPPY"

    def feed(self):
        if self.is_alive:
            self.hunger = max(0.0, self.hunger - 20.0)
            self.energy = min(100.0, self.energy + 10.0)
            self.health = min(100.0, self.health + 2.0)
            self.last_interaction = time.time()

    def play(self):
        if self.is_alive and self.energy > 10:
            self.happiness = min(100.0, self.happiness + 25.0)
            self.energy = max(0.0, self.energy - 15.0)
            self.last_interaction = time.time()

    def give_medicine(self):
        if not self.is_alive:
            return
        self.health = min(100.0, self.health + 15.0)
        self.happiness = max(0.0, self.happiness - 5.0)

    def nap(self):
        if not self.is_alive:
            return
        self.energy = min(100.0, self.energy + 30.0)
        self.happiness = min(100.0, self.happiness + 5.0)
        self.last_interaction = time.time()

    def clean(self):
        if self.is_alive:
            self.cleanliness = min(100.0, self.cleanliness + 30.0)
            self.happiness = min(100.0, self.happiness + 5.0)
            self.energy = max(0.0, self.energy - 5.0)

    def save(self):
        data = {
            "hunger": self.hunger,
            "happiness": self.happiness,
            "energy": self.energy,
            "health": self.health,
            "cleanliness": self.cleanliness,
            "is_alive": self.is_alive,
            "last_update": time.time(),
            "notified_needs": self.notified_needs
        }
        tmp = SAVE_FILE + ".tmp"
        with open(tmp, 'w') as f:
            json.dump(data, f)
        os.replace(tmp, SAVE_FILE)

    def load(self):
        defaults = {"hunger":50,"happiness":100,"energy":100,"health":100,"cleanliness":100,"is_alive":True,"last_update":time.time()}
        if not os.path.exists(SAVE_FILE):
            for k,v in defaults.items():
                setattr(self,k,v)
            return
        try:
            with open(SAVE_FILE,"r") as f:
                data=json.load(f)
        except Exception:
            data=defaults
        for k,v in defaults.items():
            setattr(self,k,float(data.get(k,v)) if isinstance(v,float) else data.get(k,v))
        self.notified_needs = data.get("notified_needs",{})
        self.last_update = float(data.get("last_update", time.time()))
        self.update()

# -----------------------
# GameEngine Class
# -----------------------
class GameEngine:
    def __init__(self):
        pygame.init()

        if platform.system() == "Linux":
            os.environ["SDL_VIDEODRIVER"]="kmsdrm"
            try:
                self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.FULLSCREEN)
            except pygame.error:
                self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        else:
            try:
                self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SCALED | pygame.RESIZABLE)
            except pygame.error:
                self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("Pocket Pi-Pet")
        self.clock = pygame.time.Clock()
        self.font = pygame.font.Font(None, 24)
        self.pet = Pet()
        self.pet.load()

        # Idle/reaction variables
        self.reaction_offsets = {"arms":0.0,"legs":0.0,"torso":0.0}
        self._idle_timer = 0.0
        self._next_idle = 1.0 + random.random()*3
        self._idle_offsets = {"arms":0.0,"legs":0.0,"torso":0.0,"ears":0.0}

        self.blink_interval=3.0
        self.blink_duration=0.12
        self.blinking=False
        self.blink_elapsed=0.0
        self.blink_timer=self.blink_interval
        self.idle_bob_offset=0
        self._bob_phase=0.0
        self.belly_squish=0.0
        self.tail_wag=0.0
        self._last_step_time=time.time()
        self.pending_messages=[]
        self.pet_reaction=None
        self.hud_text=None
        self.hud_expiry=0.0

        # UI buttons (test sandbox)
        self.buttons = []
        btn_w = 80
        btn_h = 36
        margin = 10
        y = SCREEN_HEIGHT - btn_h - margin

        # --- Reaction helpers ---
        def react_feed():
            self.pet.feed()
            self.belly_squish = 1.0
            self.pet_reaction = {"type": "hunger", "phase": 0}
            self._reaction_end = time.time() + REACTION_DURATION_HUNGER

        def react_clean():
            self.pet.clean()
            self.pet_reaction = {"type": "cleanliness", "phase": 0}
            self._reaction_end = time.time() + REACTION_DURATION_CLEAN

        def react_play():
            self.pet.play()
            self.tail_wag = 1.0

        def react_nap():
            self.pet.nap()
            self.belly_squish = 0.6

        def react_med():
            self.pet.give_medicine()

        labels = [
            ("Feed", react_feed),
            ("Play", react_play),
            ("Clean", react_clean),
            ("Nap", react_nap),
            ("Med", react_med),
        ]

        for i, (label, action) in enumerate(labels):
            x = margin + i * (btn_w + margin)
            rect = pygame.Rect(x, y, btn_w, btn_h)
            self.buttons.append({
                "rect": rect,
                "label": label,
                "action": action,
                "hover": False,
                "pressed": False
            })

    def _update_pet_appearance(self, dt):
        # reaction timing / cleanup
        if self.pet_reaction:
            if time.time() >= getattr(self, "_reaction_end", 0):
                self.pet_reaction = None
        if self.blinking:
            self.blink_elapsed += dt
            if self.blink_elapsed >= self.blink_duration:
                self.blinking=False
                self.blink_elapsed=0.0
                self.blink_timer=self.blink_interval
        else:
            self.blink_timer -= dt
            if self.blink_timer<=0:
                self.blinking=True
                self.blink_elapsed=0.0
                self.blink_timer=self.blink_interval+self.blink_duration

        self._bob_phase += dt*2.0
        self.idle_bob_offset=int(4*(1+math.sin(self._bob_phase))-4)

        if self.belly_squish>0:
            self.belly_squish=max(0.0,self.belly_squish-dt*1.5)
        if self.tail_wag>0:
            self.tail_wag=max(0.0,self.tail_wag-dt*1.5)

        # idle personality
        self._idle_timer += dt
        if self._idle_timer>=self._next_idle:
            action=random.choice(["arm_wave","leg_kick","torso_tilt","ear_flick"])
            if action=="arm_wave":
                self._idle_offsets["arms"]=random.choice([-5,5])
            elif action=="leg_kick":
                self._idle_offsets["legs"]=random.choice([-4,4])
            elif action=="torso_tilt":
                self._idle_offsets["torso"]=random.choice([-3,3])
            elif action=="ear_flick":
                self._idle_offsets["ears"]=random.choice([-2,2])
            self._idle_timer=0.0
            self._next_idle=1.0+random.random()*3
        for k in self._idle_offsets:
            self._idle_offsets[k]*=0.85

        # reaction offsets
        if self.pet_reaction:
            phase = self.pet_reaction.get("phase", 0)
            rtype = self.pet_reaction.get("type", "")
            if rtype == "hunger":
                self.reaction_offsets["arms"] = 8.0 if phase == 0 else -4.0
                self.reaction_offsets["torso"] = 2.0 if phase == 0 else 0.0
                self.pet_reaction["phase"] = 1
            elif rtype == "cleanliness":
                self.reaction_offsets["legs"] = 6.0 if phase == 0 else -3.0
                self.pet_reaction["phase"] = 1
            else:
                self.reaction_offsets = {"arms": 0.0, "legs": 0.0, "torso": 0.0}
        else:
            for k in self.reaction_offsets:
                self.reaction_offsets[k] *= 0.8

    def draw_ui(self):
        for btn in self.buttons:
            if btn["pressed"]:
                bg = (40, 40, 70)
            elif btn["hover"]:
                bg = (80, 80, 120)
            else:
                bg = COLOR_UI_BG

            pygame.draw.rect(self.screen, bg, btn["rect"], border_radius=6)
            pygame.draw.rect(self.screen, (120,120,160), btn["rect"], 2, border_radius=6)

            label_surf = self.font.render(btn["label"], True, COLOR_TEXT)
            label_rect = label_surf.get_rect(center=btn["rect"].center)
            self.screen.blit(label_surf, label_rect)

    def draw_pet(self,pos):
        cx,cy=pos
        # body
        body_w=110+int(self.belly_squish*14)
        body_h=90-int(self.belly_squish*10)
        body_rect=pygame.Rect(cx-body_w//2,cy-body_h//2,body_w,body_h)
        pygame.draw.ellipse(self.screen,(240,190,210),body_rect)
        inner_rect=body_rect.inflate(-8,-8)
        pygame.draw.ellipse(self.screen,(255,220,225),inner_rect)
        # torso
        torso_rect=pygame.Rect(cx-body_w//4,cy-body_h//2+20+self.reaction_offsets["torso"]+self._idle_offsets["torso"],body_w//2,body_h//2+10)
        pygame.draw.ellipse(self.screen,(255,220,225),torso_rect)
        # legs
        pygame.draw.ellipse(self.screen,(255,220,225),(cx-body_w//4,cy+body_h//4+self.reaction_offsets["legs"]+self._idle_offsets["legs"],16,20))
        pygame.draw.ellipse(self.screen,(255,220,225),(cx+body_w//4-16,cy+body_h//4+self.reaction_offsets["legs"]+self._idle_offsets["legs"],16,20))
        # arms
        pygame.draw.ellipse(self.screen,(255,220,225),(cx-body_w//2-6,cy-10+self.idle_bob_offset+self.reaction_offsets["arms"]+self._idle_offsets["arms"],12,18))
        pygame.draw.ellipse(self.screen,(255,220,225),(cx+body_w//2-6,cy-10-self.idle_bob_offset+self.reaction_offsets["arms"]+self._idle_offsets["arms"],12,18))
        # ears
        pygame.draw.polygon(self.screen,(255,220,225),[(cx-30,cy-40+self._idle_offsets["ears"]),(cx-22,cy-62+self._idle_offsets["ears"]),(cx-14,cy-38+self._idle_offsets["ears"])])
        pygame.draw.polygon(self.screen,(255,220,225),[(cx+30,cy-40+self._idle_offsets["ears"]),(cx+22,cy-62+self._idle_offsets["ears"]),(cx+14,cy-38+self._idle_offsets["ears"])])
        pygame.draw.circle(self.screen,(240,190,210),(cx,cy-56),6)
        # eyes
        eye_y=cy-12+self.idle_bob_offset//2
        eye_x_off=28
        eye_r=12
        pupil_r=5
        eyes_open=not self.blinking
        if eyes_open:
            pygame.draw.circle(self.screen,(255,255,255),(cx-eye_x_off,eye_y),eye_r)
            pygame.draw.circle(self.screen,(255,255,255),(cx+eye_x_off,eye_y),eye_r)
            pygame.draw.circle(self.screen,(20,20,40),(cx-eye_x_off,eye_y),pupil_r)
            pygame.draw.circle(self.screen,(20,20,40),(cx+eye_x_off,eye_y),pupil_r)
        else:
            pygame.draw.rect(self.screen,(240,190,210),(cx-eye_x_off-eye_r,eye_y-4,eye_r*2,8),border_radius=6)
            pygame.draw.rect(self.screen,(240,190,210),(cx+eye_x_off-eye_r,eye_y-4,eye_r*2,8),border_radius=6)
        # mouth
        mouth_y=cy+8
        mouth_w,mouth_h=28,10
        mouth_color=(60,30,30)
        mrect=pygame.Rect(cx-mouth_w//2,mouth_y-mouth_h//2,mouth_w,mouth_h)
        if self.pet_reaction and self.pet_reaction.get("type")=="hunger" and self.pet_reaction.get("phase")==1:
            pygame.draw.ellipse(self.screen,mouth_color,mrect.inflate(-8,0))
        elif self.pet.state=="SICK":
            pygame.draw.arc(self.screen,mouth_color,mrect,math.pi*0.25,math.pi*0.75,3)
        elif self.pet.state=="SAD":
            pygame.draw.arc(self.screen,mouth_color,mrect,math.pi*0.25,math.pi*0.75,2)
        else:
            pygame.draw.rect(self.screen,mouth_color,(cx-10,mouth_y,20,6),border_radius=4)
        # belly overlay
        if self.belly_squish>0.01:
            band_w=int(body_w*0.6)
            band_h=int(12*self.belly_squish)
            pygame.draw.ellipse(self.screen,(230,190,200),(cx-band_w//2,cy+body_h//4-band_h//2,band_w,band_h))
        self._last_drawn_pet={"eyes_open":eyes_open,"belly_squish":float(self.belly_squish),"idle_bob_offset":int(self.idle_bob_offset)}

# -----------------------
# Run
# -----------------------
if __name__=="__main__":
    game=GameEngine()
    running=True
    while running:
        dt = game.clock.tick(FPS) / 1000.0

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False
            elif event.type == pygame.MOUSEMOTION:
                for btn in game.buttons:
                    btn["hover"] = btn["rect"].collidepoint(event.pos)
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                for btn in game.buttons:
                    if btn["rect"].collidepoint(event.pos):
                        btn["pressed"] = True
            elif event.type == pygame.MOUSEBUTTONUP and event.button == 1:
                for btn in game.buttons:
                    if btn["pressed"] and btn["rect"].collidepoint(event.pos):
                        btn["action"]()
                    btn["pressed"] = False

        game._update_pet_appearance(dt)
        game.screen.fill(COLOR_BG)
        game.draw_pet((SCREEN_WIDTH//2, SCREEN_HEIGHT//2))
        game.draw_ui()
        pygame.display.flip()

    pygame.quit()
    sys.exit()