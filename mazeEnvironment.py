import pygame
import sys
import random
import numpy as np
import os

# Maze generation algorithm
# This project generates a random maze using a Depth First Search (DFS) algorithm.
# The start is represented by a green cell, and the end represented by a red cell.

WINDOW_SIZE = 800
GRID_SIZE = 50  # Number of maze cells excluding the border
CELL_SIZE = WINDOW_SIZE / (GRID_SIZE * 2 + 1)

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)
RED = (255, 0, 0)


pygame.init()

class MazeEnvironment:
    def __init__(self):
        # Set up the Pygame window
        self.screen = pygame.display.set_mode((WINDOW_SIZE, WINDOW_SIZE))
        pygame.display.set_caption("Maze Runner")
        self.clock = pygame.time.Clock()
        self.running = True

        # Load bush image and create a dictionary of scaled versions for different cell sizes
        bush_image = pygame.image.load(os.path.join('squarebush.png'))
        self.bush_images = {}  # Cache for scaled bush images

        # Generate the maze and position the start and end points
        self.maze_grid = self.generate_maze(GRID_SIZE, GRID_SIZE)
        self.start, self.end = self.place_start_end_points()

    def generate_maze(self, num_rows, num_cols):
        """
        Generates a maze using the randomized depth-first search (DFS) algorithm.
        It works as follows:
        1. Select a random cell and mark it as visited.
        2. While there are unvisited cells:
           - Randomly pick an unvisited neighbour.
           - Remove the wall between the current cell and the neighbour.
           - Move to the neighbour and repeat.
           - If you reach a dead end, backtrack to the last cell with unvisited neighbours and continue.

        This results in a maze where every cell is reachable, without any loops.
        The start and end points are placed on different borders to improve complexity/difficulty of the maze.
        """
        wall_size = np.array([num_rows, num_cols], dtype=np.int16)
        walls = np.ones((wall_size[0] + 2, wall_size[1] + 2, 3), dtype=np.byte)
        
        # Mark the outer edges as unusable (-1)
        walls[:, 0, 0] = -1
        walls[:, wall_size[1] + 1, 0] = -1
        walls[0, :, 0] = -1
        walls[wall_size[0] + 1, :, 0] = -1

        block_size = np.array([num_rows * 2 + 1, num_cols * 2 + 1], dtype=np.int16)
        blocks = np.ones((block_size[0], block_size[1]), dtype=np.byte)

        # DFS Algorithm
        # Pick a random starting cell (not on the border)
        cell = np.array([random.randrange(2, wall_size[0]), random.randrange(2, wall_size[1])], dtype=np.int16)
        walls[cell[0], cell[1], 0] = 0  # Mark as visited

        # Define directions
        up    = np.array([-1,  0], dtype=np.int16)
        down  = np.array([ 1,  0], dtype=np.int16)
        left  = np.array([ 0, -1], dtype=np.int16)
        right = np.array([ 0,  1], dtype=np.int16)

        need_cell_range = False
        round_nr = 0
        corridor_start = 0
        corridor_len = 999  # Long corridors for a more open maze

        while np.size(cell) > 0 and self.running:
            round_nr += 1
            # Get all four neighbours
            cell_neighbours = np.vstack((cell + up, cell + left, cell + down, cell + right))
            # Only consider neighbours that haven't been visited
            valid_neighbours = cell_neighbours[walls[cell_neighbours[:, 0], cell_neighbours[:, 1], 0] == 1]

            if np.size(valid_neighbours) > 0:
                # Pick a random valid neighbour
                neighbour = valid_neighbours[random.randrange(0, np.shape(valid_neighbours)[0]), :]
                if np.size(cell) > 2:
                    # If cell is an array, pick one with this neighbour only
                    cell = cell[np.sum(abs(cell - neighbour), axis=1) == 1]
                    cell = cell[random.randrange(0, np.shape(cell)[0]), :]
                walls[neighbour[0], neighbour[1], 0] = 0  # Mark neighbour as visited
                # Remove the wall between current cell and neighbour
                walls[min(cell[0], neighbour[0]), min(cell[1], neighbour[1]), 1 + abs(neighbour[1] - cell[1])] = 0
                if round_nr - corridor_start < corridor_len:
                    cell = np.array([neighbour[0], neighbour[1]], dtype=np.int16)
                else:
                    need_cell_range = True
            else:
                if np.size(cell) > 2:
                    cell = np.zeros((0, 0))
                else:
                    need_cell_range = True

            if need_cell_range:
                # Start a new corridor from a random visited cell
                cell = np.transpose(np.nonzero(walls[1:-1, 1:-1, 0] == 0)) + 1
                valid_neighbour_exists = np.array([walls[cell[:, 0] - 1, cell[:, 1], 0],
                                                  walls[cell[:, 0] + 1, cell[:, 1], 0],
                                                  walls[cell[:, 0], cell[:, 1] - 1, 0],
                                                  walls[cell[:, 0], cell[:, 1] + 1, 0]
                                                  ]).max(axis=0)
                cell_no_neighbours = cell[valid_neighbour_exists != 1]
                walls[cell_no_neighbours[:, 0], cell_no_neighbours[:, 1], 0] = -1
                corridor_start = round_nr + 0
                need_cell_range = False

        # Convert to block grid: 1 = wall, 0 = path
        blocks[1:-1:2, 1:-1:2] = 0  # Open the cells
        blocks[1:-1:2, 2:-2:2] = walls[1:-1, 1:-2, 2]  # Horizontal walls
        blocks[2:-2:2, 1:-1:2] = walls[1:-2, 1:-1, 1]  # Vertical walls
        return blocks

    def place_start_end_points(self):
        """
        Randomly places the start (green) and end (red) points on different borders of the maze.
        Ensures both are always accessible from the maze by opening the adjacent cell inside the maze.
        """
        N = self.maze_grid.shape[0]
        borders = [
            [(0, i) for i in range(1, N-1)],  # Top border
            [(N-1, i) for i in range(1, N-1)],  # Bottom border
            [(i, 0) for i in range(1, N-1)],  # Left border
            [(i, N-1) for i in range(1, N-1)]  # Right border
        ]
        b1, b2 = random.sample(range(4), 2)
        start = random.choice(borders[b1])
        end = random.choice(borders[b2])
        # Open the start and end in the maze
        self.maze_grid[start[0]][start[1]] = 0
        self.maze_grid[end[0]][end[1]] = 0

        # Make sure the cell inside the maze next to start/end is open
        def adjacent_inside(point):
            r, c = point
            if r == 0: return (r+1, c)
            if r == N-1: return (r-1, c)
            if c == 0: return (r, c+1)
            if c == N-1: return (r, c-1)
        self.maze_grid[adjacent_inside(start)[0]][adjacent_inside(start)[1]] = 0
        self.maze_grid[adjacent_inside(end)[0]][adjacent_inside(end)[1]] = 0

        return start, end

    # Ensure the loaded bush image is scaled to correct dimensions
    def get_scaled_bush(self, width, height):
        """Get a bush image scaled to the exact dimensions needed."""
        key = (width, height)
        if key not in self.bush_images:
            self.bush_images[key] = pygame.transform.scale(
                pygame.image.load(os.path.join('squarebush.png')),
                (width, height)
            )
        return self.bush_images[key]

    def draw_maze(self):
        """
        Draws the maze to the Pygame window. Bush image = wall, white = path, green = start, red = end.
        The rectangles and bush images are sized to perfectly fill the window with no gaps.
        """
        N = self.maze_grid.shape[0]
        for row in range(N):
            for col in range(N):
                # Calculate exact dimensions for this cell
                if col == N - 1:
                    w = WINDOW_SIZE - int(col * CELL_SIZE)
                else:
                    w = int((col + 1) * CELL_SIZE) - int(col * CELL_SIZE)
                if row == N - 1:
                    h = WINDOW_SIZE - int(row * CELL_SIZE)
                else:
                    h = int((row + 1) * CELL_SIZE) - int(row * CELL_SIZE)
                x = int(col * CELL_SIZE)
                y = int(row * CELL_SIZE)
                
                if (row, col) == self.start:
                    pygame.draw.rect(self.screen, GREEN, (x, y, w, h))
                elif (row, col) == self.end:
                    pygame.draw.rect(self.screen, RED, (x, y, w, h))
                elif self.maze_grid[row][col] == 1:  # Wall
                    # Get a bush image scaled to the exact dimensions needed
                    bush = self.get_scaled_bush(w, h)
                    self.screen.blit(bush, (x, y))
                else:  # Path
                    pygame.draw.rect(self.screen, WHITE, (x, y, w, h))


    def run(self):
        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                # Click to generate a new maze (great for testing viability!)
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    self.maze_grid = self.generate_maze(GRID_SIZE, GRID_SIZE)
                    self.start, self.end = self.place_start_end_points()
            self.screen.fill(WHITE)
            self.draw_maze()
            pygame.display.flip()
            self.clock.tick(60)
        pygame.quit()
        sys.exit()

if __name__ == "__main__":
    MazeEnvironment().run()
