import pygame
import sys
import random

# Constants
WINDOW_SIZE = 800
GRID_SIZE = 20
CELL_SIZE = WINDOW_SIZE // GRID_SIZE

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

pygame.init()

class MazeEnvironment:
    def __init__(self):
        self.screen = pygame.display.set_mode((WINDOW_SIZE, WINDOW_SIZE))
        pygame.display.set_caption("Maze Runner")
        self.clock = pygame.time.Clock()
        self.running = True
        # Create a grid with all inner cells as 0 (path) and all border cells as 1 (wall)
        self.maze_grid = [[0 for _ in range(GRID_SIZE)] for _ in range(GRID_SIZE)]
        for i in range(GRID_SIZE):
            self.maze_grid[0][i] = 1
            self.maze_grid[GRID_SIZE-1][i] = 1
            self.maze_grid[i][0] = 1
            self.maze_grid[i][GRID_SIZE-1] = 1
        # Place start and end points on different borders (not corners)
        self.start, self.end = self.place_start_end_points()

    def place_start_end_points(self):
        borders = [
            [(0, i) for i in range(1, GRID_SIZE-1)],  # Top
            [(GRID_SIZE-1, i) for i in range(1, GRID_SIZE-1)],  # Bottom
            [(i, 0) for i in range(1, GRID_SIZE-1)],  # Left
            [(i, GRID_SIZE-1) for i in range(1, GRID_SIZE-1)]  # Right
        ]
        b1, b2 = random.sample(range(4), 2)
        start = random.choice(borders[b1])
        end = random.choice(borders[b2])
        return start, end

    def draw_maze(self):
        for row in range(GRID_SIZE):
            for col in range(GRID_SIZE):
                x = col * CELL_SIZE
                y = row * CELL_SIZE
                if (row, col) == self.start:
                    color = (0, 255, 0)  # Green
                elif (row, col) == self.end:
                    color = (255, 0, 0)  # Red
                else:
                    color = BLACK if self.maze_grid[row][col] == 1 else WHITE
                pygame.draw.rect(self.screen, color, (x, y, CELL_SIZE, CELL_SIZE))

    def run(self):
        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
            self.screen.fill(WHITE)
            self.draw_maze()
            pygame.display.flip()
            self.clock.tick(60)
        pygame.quit()
        sys.exit()

if __name__ == "__main__":
    MazeEnvironment().run()
