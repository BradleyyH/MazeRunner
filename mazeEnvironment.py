import pygame
import sys
import random

pygame.init()

# Constants
WINDOW_SIZE = 800
GRID_SIZE = 20  # Starting grid size of 20x20
CELL_SIZE = WINDOW_SIZE // GRID_SIZE

# Colours
WHITE = (255, 255, 255)
GRAY = (128, 128, 128)
BLACK = (0, 0, 0)  # Used for walls

class MazeEnvironment:
    def __init__(self):
        self.screen = pygame.display.set_mode((WINDOW_SIZE, WINDOW_SIZE))
        pygame.display.set_caption("Maze Runner")
        self.clock = pygame.time.Clock()
        self.running = True
        # Initialize maze grid with all walls (1)
        self.maze_grid = [[1 for _ in range(GRID_SIZE)] for _ in range(GRID_SIZE)]
        # Generate the initial maze
        self.generate_maze()

    def get_neighbours(self, row, col):
        """Get valid unvisited neighbours of a cell that are 2 steps away.
        This is used for the random maze generation - we check cells 2 steps away because
        we need to leave walls between paths. For example, if we're at (1,1),
        we check (1,3), (3,1), (1,-1), and (-1,1) to ensure we leave walls
        at (1,2), (2,1), etc. Only returns neighbours that are still walls (value of 1)."""
        neighbours = []
        # Check all four directions 
        for dr, dc in [(0, 2), (2, 0), (0, -2), (-2, 0)]:
            new_row, new_col = row + dr, col + dc
            if (0 <= new_row < GRID_SIZE and 0 <= new_col < GRID_SIZE and 
                self.maze_grid[new_row][new_col] == 1):
                neighbours.append((new_row, new_col))
        return neighbours

    def generate_maze(self):
        """Generate a random maze using recursive backtracking.
        This is the main maze generation method that initializes the starting point.
        We start at a random odd position to ensure we have walls between all paths.
        The actual path carving is done recursively by the carve_path helper function."""
        # Pick a random starting position, using odd numbers only to maintain wall spacing
        start_row = random.randrange(1, GRID_SIZE-1, 2)
        start_col = random.randrange(1, GRID_SIZE-1, 2)
        # Mark the starting cell as a path (0) - this will be the first cell in our maze
        self.maze_grid[start_row][start_col] = 0
        
        def carve_path(row, col):
            neighbours = self.get_neighbours(row, col)
            random.shuffle(neighbours)
            
            for next_row, next_col in neighbours:
                if self.maze_grid[next_row][next_col] == 1:  # If unvisited
                    # Carve path by marking cells as 0
                    self.maze_grid[next_row][next_col] = 0
                    # Mark the cell between current and next as path
                    self.maze_grid[(row + next_row) // 2][(col + next_col) // 2] = 0
                    carve_path(next_row, next_col)
        
        carve_path(start_row, start_col)

    def draw_grid(self):
        # Draw vertical grid lines
        for x in range(0, WINDOW_SIZE, CELL_SIZE):
            pygame.draw.line(self.screen, GRAY, (x, 0), (x, WINDOW_SIZE))
            
        # Draw horizontal grid lines
        for y in range(0, WINDOW_SIZE, CELL_SIZE):
            pygame.draw.line(self.screen, GRAY, (0, y), (WINDOW_SIZE, y))

    def draw_maze(self):
        for row in range(GRID_SIZE):
            for col in range(GRID_SIZE):
                x = col * CELL_SIZE
                y = row * CELL_SIZE
                if self.maze_grid[row][col] == 1:  # If it is a wall:
                    pygame.draw.rect(self.screen, BLACK, (x, y, CELL_SIZE, CELL_SIZE))

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
            
            # Draw maze
            self.draw_maze()
            # Draw grid lines on top
            self.draw_grid()
            
            # Update display
            pygame.display.flip()
            self.clock.tick(60)

        pygame.quit()
        sys.exit()

if __name__ == "__main__":
    maze = MazeEnvironment()
    maze.run()
