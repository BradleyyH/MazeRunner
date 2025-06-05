import heapq
from typing import List, Tuple, Optional
import numpy as np

def astar_search(maze: np.ndarray, start: Tuple[int, int], end: Tuple[int, int]) -> Optional[List[Tuple[int, int]]]:
    """
    Finds the optimal path in a maze from start to end using the A* search algorithm.

    Args:
        maze: 2D numpy array where 0 is a path and 1 is a wall.
        start: (row, col) tuple for start position.
        end: (row, col) tuple for end position.

    Returns:
        List of (row, col) tuples representing the path from the start to the end.
        Returns None if no path is found (Should never happen).
    """

    def heuristic(current: Tuple[int, int], goal: Tuple[int, int]) -> int:
        return abs(current[0] - goal[0]) + abs(current[1] - goal[1])

    open_set = []
    heapq.heappush(open_set, (heuristic(start, end), 0, start))  # (f_score, g_score, node)

    came_from = {}
    g_score = {start: 0}
    f_score = {start: heuristic(start, end)}
    closed_set = set()

    # 4 directional movement for our maze
    neighbors = [(-1, 0), (1, 0), (0, -1), (0, 1)]

    while open_set:
        current = heapq.heappop(open_set)[2]
        if current == end:
            # Reconstruct path
            path = [current]
            while current in came_from:
                current = came_from[current]
                path.append(current)
            path.reverse()
            return path
        closed_set.add(current)
        for d_row, d_col in neighbors:
            neighbor = (current[0] + d_row, current[1] + d_col)
            if 0 <= neighbor[0] < maze.shape[0] and 0 <= neighbor[1] < maze.shape[1]:
                if maze[neighbor[0]][neighbor[1]] == 1:
                    continue
            else:
                continue
            if neighbor in closed_set:
                continue
            tentative_g_score = g_score[current] + 1
            if tentative_g_score < g_score.get(neighbor, float('inf')):
                came_from[neighbor] = current
                g_score[neighbor] = tentative_g_score
                f_score[neighbor] = tentative_g_score + heuristic(neighbor, end)
                heapq.heappush(open_set, (f_score[neighbor], tentative_g_score, neighbor))
    return None