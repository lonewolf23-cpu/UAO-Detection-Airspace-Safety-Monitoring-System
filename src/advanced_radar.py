import pygame
import math
import random

WIDTH, HEIGHT = 900, 700
CENTER = (WIDTH//2, HEIGHT//2)
RADIUS = 260

class AdvancedRadar:

    def __init__(self):

        pygame.init()
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption("3D Deep Radar") #millitry grade defence radar copy or temp

        self.clock = pygame.time.Clock()

        self.angle = 0
        self.grid_angle = 0
        self.targets = []

        self.pulse = 0

    # ==============================
    # 🎯 MAIN UPDATE FUNCTION
    # ==============================
    def update(self, pos):

        if pos is None:
            return

        x = int(CENTER[0] + pos[0])
        y = int(CENTER[1] - pos[1])

        depth = math.sqrt(pos[0]**2 + pos[1]**2)

        classification = self.classify(depth)

        self.targets.append({
            "pos":[x,y],
            "life":255,
            "depth":depth,
            "class":classification,
            "blink":0
        })

        if len(self.targets) > 30:
            self.targets.pop(0)

    # ==============================
    # 🛩 CLASSIFICATION SYSTEM
    # ==============================
    def classify(self, depth):

        if depth < 60:
            return "Friendly"
        elif depth < 140:
            return "Unknown"
        else:
            return "Threat"

    # ==============================
    # 🛰 ROTATING GRID
    # ==============================
    def draw_grid(self):                  #  this is the setup of the grid scaner grid

        for i in range(0,360,30):

            theta = math.radians(i) + self.grid_angle

            x = CENTER[0] + RADIUS*math.cos(theta)
            y = CENTER[1] + RADIUS*math.sin(theta)

            pygame.draw.line(self.screen,(0,90,40),CENTER,(x,y),1)

        for r in range(50,RADIUS,50):
            pygame.draw.circle(self.screen,(0,100,40),CENTER,r,1)

        self.grid_angle += 0.002

    # ==============================
    # 🌊 PULSE WAVE
    # ==============================
    def draw_pulse(self):

        self.pulse += 1

        r = (self.pulse % RADIUS)

        pygame.draw.circle(self.screen,(0,255,120),CENTER,r,1)

    # ==============================
    # SWEEP
    # ==============================
    def draw_sweep(self):                #sweeper in the scanneer

        surface = pygame.Surface((WIDTH,HEIGHT),pygame.SRCALPHA)

        for i in range(50):

            fade = max(0,150-i*3)

            theta = self.angle - (i*0.02)

            x = CENTER[0] + RADIUS*math.cos(theta)
            y = CENTER[1] + RADIUS*math.sin(theta)

            pygame.draw.line(surface,(0,255,120,fade),CENTER,(x,y),2)

        self.screen.blit(surface,(0,0))

        self.angle += 0.01

    # ==============================
    # 🚨 TARGET TRACKING
    # ==============================
    def draw_targets(self):

        for target in self.targets:

            x,y = target["pos"]
            life = target["life"]
            depth = target["depth"]
            cls = target["class"]

            size = max(3,int(10-(depth/50)))

            if cls == "Threat":
                target["blink"] += 1
                if target["blink"]%20 < 10:
                    color = (255,0,0)
                else:
                    color = (100,0,0)
            elif cls == "Unknown":
                color = (255,255,0)
            else:
                color = (0,255,0)

            glow = pygame.Surface((20,20),pygame.SRCALPHA)
            pygame.draw.circle(glow,(*color,life),(10,10),size)
            self.screen.blit(glow,(x-10,y-10))

            target["life"] -= 1

        self.targets = [t for t in self.targets if t["life"]>0]

    # ==============================
    # FRAME RUNNER
    # ==============================
    def run_frame(self):

        self.screen.fill((0,15,0))

        self.draw_grid()
        self.draw_pulse()
        self.draw_sweep()
        self.draw_targets()

        pygame.display.update()
        self.clock.tick(60)
