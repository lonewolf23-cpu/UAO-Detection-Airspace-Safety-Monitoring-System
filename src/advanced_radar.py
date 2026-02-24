import pygame
import math

WIDTH, HEIGHT = 900, 700
CENTER = (WIDTH//2, HEIGHT//2)
RADIUS = 250

class AdvancedRadar:

    def update(self, detected_object):
    if detected_object is None:
        return

    # update radar tracking logic
    self.current_object = detected_object

    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption("Air Defense Radar System")

        self.clock = pygame.time.Clock()
        self.angle = 0
        self.targets = []

    def draw_glow_circle(self, radius, color):
        for i in range(10):
            pygame.draw.circle(
                self.screen,
                (color[0], color[1], color[2], 20),
                CENTER,
                radius+i,
                1
            )

    def draw_radar_grid(self):
        for r in range(50, RADIUS, 50):
            self.draw_glow_circle(r, (0,255,150))

        pygame.draw.line(self.screen,(0,255,150),
            (CENTER[0]-RADIUS,CENTER[1]),
            (CENTER[0]+RADIUS,CENTER[1]),1)

        pygame.draw.line(self.screen,(0,255,150),
            (CENTER[0],CENTER[1]-RADIUS),
            (CENTER[0],CENTER[1]+RADIUS),1)

    def draw_sweep(self):
        self.angle += 0.03
        x = CENTER[0] + RADIUS * math.cos(self.angle)
        y = CENTER[1] + RADIUS * math.sin(self.angle)

        pygame.draw.line(self.screen,(0,255,100),
                         CENTER,(x,y),3)

    def draw_targets(self):
        for t in self.targets:
            pygame.draw.circle(self.screen,(0,255,0),t,5)

    def update_target(self,pos):
        if pos:
            x = int(CENTER[0]+pos[0])
            y = int(CENTER[1]-pos[1])
            self.targets.append((x,y))

    def run(self):
        running=True
        while running:

            self.screen.fill((5,15,5))

            for event in pygame.event.get():
                if event.type==pygame.QUIT:
                    running=False

            self.draw_radar_grid()
            self.draw_sweep()
            self.draw_targets()

            pygame.display.update()
            self.clock.tick(60)
