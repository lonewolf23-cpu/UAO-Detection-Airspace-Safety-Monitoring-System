import pygame
import math

WIDTH, HEIGHT = 900, 700
CENTER = (WIDTH//2, HEIGHT//2)
RADIUS = 260

class AdvancedRadar:

    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption("Military Radar Display")

        self.clock = pygame.time.Clock()
        self.angle = 0
        self.targets = []
        self.trails = []

    def draw_rings(self):
        for r in range(50, RADIUS, 50):
            pygame.draw.circle(self.screen,(0,255,120),CENTER,r,1)

    def draw_sweep_sector(self):

        for i in range(20):

            alpha = max(5, 60 - i*3)

            surface = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)

            theta = self.angle - (i*0.03)

            x = CENTER[0] + RADIUS * math.cos(theta)
            y = CENTER[1] + RADIUS * math.sin(theta)

            pygame.draw.line(surface,(0,255,120,alpha),
                             CENTER,(x,y),3)

            self.screen.blit(surface,(0,0))

    def draw_noise(self):
        for _ in range(50):
            x = CENTER[0] + int(math.cos(math.radians(_*7))*RADIUS*0.6)
            y = CENTER[1] + int(math.sin(math.radians(_*5))*RADIUS*0.6)
            pygame.draw.circle(self.screen,(0,80,40),(x,y),1)

    def update(self,pos):
        if pos:
            x = int(CENTER[0]+pos[0])
            y = int(CENTER[1]-pos[1])

            self.targets.append((x,y))
            self.trails.append((x,y))

            if len(self.trails) > 20:
                self.trails.pop(0)

    def draw_targets(self):

        for i,t in enumerate(self.trails):
            fade = int(255*(i/len(self.trails)))
            pygame.draw.circle(self.screen,(0,fade,0),t,4)

        for t in self.targets:
            pygame.draw.circle(self.screen,(0,255,0),t,6)

    def run_frame(self):

        self.screen.fill((0,10,0))

        self.draw_noise()
        self.draw_rings()

        self.angle += 0.03
        self.draw_sweep_sector()

        self.draw_targets()

        pygame.display.update()
        self.clock.tick(60)
