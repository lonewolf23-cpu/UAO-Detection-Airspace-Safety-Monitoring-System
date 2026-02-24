import pygame
import math
import random

WIDTH, HEIGHT = 900, 700
CENTER = (WIDTH // 2, HEIGHT // 2)
RADIUS = 260

class AdvancedRadar:

    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption("Advanced Military Radar")

        self.clock = pygame.time.Clock()

        self.angle = 0
        self.sweep_speed = 0.01   # Slower sweep (smooth)
        self.targets = []
        self.max_targets = 25

        self.spawn_timer = 0

    # -------------------------------
    # Background grid & glow
    # -------------------------------
    def draw_rings(self):
        for r in range(50, RADIUS, 50):
            pygame.draw.circle(self.screen, (0, 120, 60), CENTER, r, 1)

        # Outer glow ring
        pygame.draw.circle(self.screen, (0, 255, 120), CENTER, RADIUS, 2)

    # -------------------------------
    # Radar sweep with glow
    # -------------------------------
    def draw_sweep(self):
        sweep_surface = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)

        for i in range(60):
            fade = max(0, 180 - i * 3)
            theta = self.angle - (i * 0.02)

            x = CENTER[0] + RADIUS * math.cos(theta)
            y = CENTER[1] + RADIUS * math.sin(theta)

            pygame.draw.line(
                sweep_surface,
                (0, 255, 120, fade),
                CENTER,
                (x, y),
                2
            )

        self.screen.blit(sweep_surface, (0, 0))

    # -------------------------------
    # Random realistic noise
    # -------------------------------
    def draw_noise(self):
        for _ in range(30):
            angle = random.uniform(0, 2 * math.pi)
            distance = random.uniform(0, RADIUS)
            x = int(CENTER[0] + math.cos(angle) * distance)
            y = int(CENTER[1] + math.sin(angle) * distance)
            pygame.draw.circle(self.screen, (0, 50, 25), (x, y), 1)

    # -------------------------------
    # Add controlled targets
    # -------------------------------
    def spawn_target(self):
        angle = random.uniform(0, 2 * math.pi)
        distance = random.uniform(40, RADIUS - 20)

        x = int(CENTER[0] + math.cos(angle) * distance)
        y = int(CENTER[1] + math.sin(angle) * distance)

        self.targets.append({
            "pos": [x, y],
            "life": 255
        })

        if len(self.targets) > self.max_targets:
            self.targets.pop(0)

    # -------------------------------
    # Draw targets with fading trail
    # -------------------------------
    def draw_targets(self):
        for target in self.targets:
            x, y = target["pos"]
            life = target["life"]

            # Glow
            glow_surface = pygame.Surface((20, 20), pygame.SRCALPHA)
            pygame.draw.circle(glow_surface, (0, 255, 0, life), (10, 10), 6)
            self.screen.blit(glow_surface, (x - 10, y - 10))

            # Fade out slowly
            target["life"] -= 2

        # Remove dead targets
        self.targets = [t for t in self.targets if t["life"] > 0]

    # -------------------------------
    # Frame update
    # -------------------------------
    def run_frame(self):

        self.screen.fill((0, 15, 0))

        self.draw_noise()
        self.draw_rings()

        self.angle += self.sweep_speed
        self.draw_sweep()

        # Spawn targets slowly
        self.spawn_timer += 1
        if self.spawn_timer > 60:   # every 1 second
            self.spawn_target()
            self.spawn_timer = 0

        self.draw_targets()

        pygame.display.update()
        self.clock.tick(60)
