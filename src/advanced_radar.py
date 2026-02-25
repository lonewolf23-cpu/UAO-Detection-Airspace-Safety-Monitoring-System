import pygame
import math

WIDTH, HEIGHT = 900, 700
CENTER = (WIDTH//2, HEIGHT//2)
RADIUS = 260


class AdvancedRadar:

    def __init__(self):

        pygame.init()
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption("3D Deep Radar")

        self.clock = pygame.time.Clock()

        # Sweeper angle (ONLY this rotates)
        self.angle = 0

        # Targets
        self.targets = []

        # Pulse wave
        self.pulse = 0

        # HUD Font
        self.font = pygame.font.SysFont("consolas", 14, bold=True)

    # ==============================
    # 🎯 UPDATE TARGET
    # ==============================
    def update(self, pos):

        if pos is None:
            return

        x = int(CENTER[0] + pos[0])
        y = int(CENTER[1] - pos[1])

        depth = math.sqrt(pos[0]**2 + pos[1]**2)
        classification = self.classify(depth)

        self.targets.append({
            "pos": [x, y],
            "life": 255,
            "depth": depth,
            "class": classification,
            "blink": 0
        })

        if len(self.targets) > 30:
            self.targets.pop(0)

    # ==============================
    # 🛩 CLASSIFIER
    # ==============================
    def classify(self, depth):

        if depth < 60:
            return "Friendly"
        elif depth < 140:
            return "Unknown"
        else:
            return "Threat"

    # ==============================
    # 🛰 STATIC GRID (NO ROTATION)
    # ==============================
    def draw_grid(self):

        # Range Rings
        for r in range(50, RADIUS, 50):
            pygame.draw.circle(self.screen, (0, 100, 40), CENTER, r, 1)

        # Horizontal Axis
        pygame.draw.line(
            self.screen, (0, 80, 30),
            (CENTER[0] - RADIUS, CENTER[1]),
            (CENTER[0] + RADIUS, CENTER[1]), 1
        )

        # Vertical Axis
        pygame.draw.line(
            self.screen, (0, 80, 30),
            (CENTER[0], CENTER[1] - RADIUS),
            (CENTER[0], CENTER[1] + RADIUS), 1
        )

    # ==============================
    # 🌊 PULSE WAVE
    # ==============================
    def draw_pulse(self):

        self.pulse += 1
        r = self.pulse % RADIUS

        pygame.draw.circle(self.screen, (0, 255, 120), CENTER, r, 1)

    # ==============================
    # 📡 SWEEPER (ONLY THIS MOVES)
    # ==============================
    def draw_sweep(self):

        surface = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)

        for i in range(50):

            fade = max(0, 150 - i * 3)

            theta = self.angle - (i * 0.02)

            x = CENTER[0] + RADIUS * math.cos(theta)
            y = CENTER[1] + RADIUS * math.sin(theta)

            pygame.draw.line(surface, (0, 255, 120, fade), CENTER, (x, y), 2)

        self.screen.blit(surface, (0, 0))

        self.angle += 0.01  # Only sweeper rotates

    # ==============================
    # 🚨 TARGET TRACKING
    # ==============================
    def draw_targets(self):

        for target in self.targets:

            x, y = target["pos"]
            depth = target["depth"]
            cls = target["class"]

            size = max(3, int(10 - (depth / 50)))

            if cls == "Threat":
                target["blink"] += 1
                if target["blink"] % 20 < 10:
                    color = (255, 0, 0)
                else:
                    color = (100, 0, 0)
            elif cls == "Unknown":
                color = (255, 255, 0)
            else:
                color = (0, 255, 0)

            pygame.draw.circle(self.screen, color, (x, y), size)

            target["life"] -= 1

        self.targets = [t for t in self.targets if t["life"] > 0]

    # ==============================
    # 🧠 THREAT HUD LABELS
    # ==============================
    def draw_hud_labels(self):

        for target in self.targets:

            x, y = target["pos"]
            depth = int(target["depth"])
            cls = target["class"]

            if cls == "Threat":
                color = (255, 0, 0)
            elif cls == "Unknown":
                color = (255, 255, 0)
            else:
                color = (0, 255, 0)

            label1 = self.font.render(cls, True, color)
            label2 = self.font.render(f"R:{depth}", True, color)

            self.screen.blit(label1, (x + 8, y - 10))
            self.screen.blit(label2, (x + 8, y + 5))

    # ==============================
    # FRAME RENDER
    # ==============================
    def run_frame(self):

        self.screen.fill((0, 15, 0))

        self.draw_grid()
        self.draw_pulse()
        self.draw_sweep()
        self.draw_targets()
        self.draw_hud_labels()

        pygame.display.update()
        self.clock.tick(60)
