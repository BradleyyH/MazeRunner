import pygame
import sys

pygame.init()

# Constants
WINDOW_SIZE = 800
GRID_SIZE = 20  # Starting grid size of 20x20
CELL_SIZE = WINDOW_SIZE // GRID_SIZE

# Colours
WHITE = (255, 255, 255)
GRAY = (128, 128, 128)

class MazeEnvironment:
    def __init__(self):
        self.screen = pygame.display.set_mode((WINDOW_SIZE, WINDOW_SIZE))
        pygame.display.set_caption("Maze Runner")
        self.clock = pygame.time.Clock()
        self.running = True

    def draw_grid(self):
        # Draw vertical grid lines
        for x in range(0, WINDOW_SIZE, CELL_SIZE):
            pygame.draw.line(self.screen, GRAY, (x, 0), (x, WINDOW_SIZE))
        # Draw horizontal grid lines
        for y in range(0, WINDOW_SIZE, CELL_SIZE):
            pygame.draw.line(self.screen, GRAY, (0, y), (WINDOW_SIZE, y))

    def run(self):
        while self.running:
            # Handle events
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        self.running = False

            # Clear screen
            self.screen.fill(WHITE)
            
            # Draw grid
            self.draw_grid()
            
            # Update display
            pygame.display.flip()
            self.clock.tick(60)

        pygame.quit()
        sys.exit()

if __name__ == "__main__":
    maze = MazeEnvironment()
    maze.run()
