import pygame
import sys
import random
import numpy as np
import os
from astar_search import astar_search

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
        pygame.display.set_caption("Random Maze Generator")
        self.clock = pygame.time.Clock()
        self.running = True

        # Load bush image, creating a dictionary for scaled versions of different cell sizes
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
        
        # Prevent the algorithm from leaving the maze (Marks edges as unusable)
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

        while np.size(cell) > 0 and self.running:
            cell_neighbours = np.vstack((cell + up, cell + left, cell + down, cell + right))
            # Only consider the neighbours that haven't been visited
            valid_neighbours = cell_neighbours[walls[cell_neighbours[:, 0], cell_neighbours[:, 1], 0] == 1]

            if np.size(valid_neighbours) > 0:
                # Pick a random valid neighbour
                neighbour = valid_neighbours[random.randrange(0, np.shape(valid_neighbours)[0]), :]
                if np.size(cell) > 2:
                    # If a cell is an array, pick one with this neighbour only
                    cell = cell[np.sum(abs(cell - neighbour), axis=1) == 1]
                    cell = cell[random.randrange(0, np.shape(cell)[0]), :]
                walls[neighbour[0], neighbour[1], 0] = 0  # Mark neighbour as visited
                # Remove the wall between current cell and neighbour
                walls[min(cell[0], neighbour[0]), min(cell[1], neighbour[1]), 1 + abs(neighbour[1] - cell[1])] = 0
                # Always move to the neighbour
                cell = np.array([neighbour[0], neighbour[1]], dtype=np.int16)
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
                need_cell_range = False

        # Convert to block grid. 1 is a wall, 0 is a path
        blocks[1:-1:2, 1:-1:2] = 0  # Open the cells
        blocks[1:-1:2, 2:-2:2] = walls[1:-1, 1:-2, 2]  # Horizontal walls
        blocks[2:-2:2, 1:-1:2] = walls[1:-2, 1:-1, 1]  # Vertical walls
        return blocks

    def place_start_end_points(self):
        """
        Randomly places the start (green) and end (red) points on different borders of the maze.
        Ensures both are always accessible from the maze by opening the adjacent cell inside the maze.
        """
        maze_dim = self.maze_grid.shape[0]
        borders = [
            [(0, i) for i in range(1, maze_dim-1)],  # Top border
            [(maze_dim-1, i) for i in range(1, maze_dim-1)],  # Bottom border
            [(i, 0) for i in range(1, maze_dim-1)],  # Left border
            [(i, maze_dim-1) for i in range(1, maze_dim-1)]  # Right border
        ]
        b1, b2 = random.sample(range(4), 2)
        start = random.choice(borders[b1])
        end = random.choice(borders[b2])
        # Open the start and end in the maze
        self.maze_grid[start[0]][start[1]] = 0
        self.maze_grid[end[0]][end[1]] = 0

        # Make sure the cell inside the maze next to start/end is open
        def adjacent_inside(point):
            row, col = point
            if row == 0: return (row+1, col)
            if row == maze_dim-1: return (row-1, col)
            if col == 0: return (row, col+1)
            if col == maze_dim-1: return (row, col-1)
        self.maze_grid[adjacent_inside(start)[0]][adjacent_inside(start)[1]] = 0
        self.maze_grid[adjacent_inside(end)[0]][adjacent_inside(end)[1]] = 0

        return start, end

    # Ensure that the loaded bush image is scaled correctly, given cell size
    def get_scaled_bush(self, width, height):
        """Returns a bush image scaled correctly."""
        key = (width, height)
        if key not in self.bush_images:
            self.bush_images[key] = pygame.transform.scale(
                pygame.image.load(os.path.join('squarebush.png')),
                (width, height)
            )
        return self.bush_images[key]

    def draw_maze(self):
        """
        Draws the maze to the Pygame window.
        """
        maze_dim = self.maze_grid.shape[0]
        for row in range(maze_dim):
            for col in range(maze_dim):
                # Calculate dimensions for cell
                if col == maze_dim - 1:
                    cell_width = WINDOW_SIZE - int(col * CELL_SIZE)
                else:
                    cell_width = int((col + 1) * CELL_SIZE) - int(col * CELL_SIZE)
                if row == maze_dim - 1:
                    cell_height = WINDOW_SIZE - int(row * CELL_SIZE)
                else:
                    cell_height = int((row + 1) * CELL_SIZE) - int(row * CELL_SIZE)
                x = int(col * CELL_SIZE)
                y = int(row * CELL_SIZE)
                
                if (row, col) == self.start:
                    pygame.draw.rect(self.screen, GREEN, (x, y, cell_width, cell_height))
                elif (row, col) == self.end:
                    pygame.draw.rect(self.screen, RED, (x, y, cell_width, cell_height))
                elif self.maze_grid[row][col] == 1:  # Wall
                    # Get a bush image scaled to the exact dimensions needed
                    bush = self.get_scaled_bush(cell_width, cell_height)
                    self.screen.blit(bush, (x, y))
                else:  # Path
                    pygame.draw.rect(self.screen, WHITE, (x, y, cell_width, cell_height))


    def run(self):
        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                # Click to generate a new maze (temp for testing)
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    self.maze_grid = self.generate_maze(GRID_SIZE, GRID_SIZE)
                    self.start, self.end = self.place_start_end_points()
            self.screen.fill(WHITE)
            self.draw_maze()
            pygame.display.flip()
            self.clock.tick(60)

            path = astar_search(self.maze_grid, self.start, self.end)
            print(path)  # This will print the list of (row, col) tuples if a path is found

        pygame.quit()
        sys.exit()

if __name__ == "__main__":
    MazeEnvironment().run()
