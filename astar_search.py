import heapq
from typing import List, Tuple, Optional
import numpy as np

def astar_search(maze: np.ndarray, start: Tuple[int, int], end: Tuple[int, int]) -> Optional[List[Tuple[int, int]]]:
    """
    Finds the optimal path in a maze from start to end using the A* search algorithm.

    Args:
        maze: 2D numpy array where 0 is a path and 1 is a wall.
        start: (row, col) tuple for the start position.
        end: (row, col) tuple for the end position.

    Returns:
        List of (row, col) tuples representing the path from start to end, including both.
        Returns None if no path is found.
    """
    # TODO: Implement the A* search algorithm
    pass 