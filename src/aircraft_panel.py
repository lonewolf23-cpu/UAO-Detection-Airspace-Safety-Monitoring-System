import pygame


class AircraftPanel:

    def __init__(self):

        pygame.init()

        self.screen = pygame.display.set_mode((400,300))
        pygame.display.set_caption("Aircraft Information")

        self.font = pygame.font.SysFont("Arial",20)

    def show(self, target_id, position):

        self.screen.fill((20,20,20))

        text1 = self.font.render(f"Target ID: {target_id}", True, (255,255,255))
        text2 = self.font.render(f"Position: {position}", True, (255,255,255))

        self.screen.blit(text1,(20,50))
        self.screen.blit(text2,(20,100))

        pygame.display.update()
