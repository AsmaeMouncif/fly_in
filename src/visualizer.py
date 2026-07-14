import pygame


class Visualizer:
    def run(self):
        pygame.init()
        screen = pygame.display.set_mode((1100, 600), pygame.RESIZABLE)
        pygame.display.set_caption("fly-in")

        running = True

        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

            screen.fill((0, 0, 0))

            # cercle vide (contour blanc)
            # pygame.draw.circle(screen, (0, 255, 0), (550, 300), 70, 3)

            pygame.display.flip()

        pygame.quit()
