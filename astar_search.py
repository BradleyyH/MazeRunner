import heapq
from typing import List, Tuple, Optional, Generator
import numpy as np

def astar_search(
    maze: np.ndarray,
    start: Tuple[int, int],
    end: Tuple[int, int]
) -> Generator[
    dict, None, None
]:
    """
     Finds the optimal path in a maze from start to end using the A* search algorithm.

    Args:
        maze: 2D numpy array where 0 is a path and 1 is a wall.
        start: (row, col) tuple for start position.
        end: (row, col) tuple for end position.

    Returns:
        List of (row, col) tuples representing the path from the start to the end.
        Returns None if no path is found (Should never happen).
        
        
    Generator version of the A* search algorithm to show the pathfinding process.
    Yields a dict with the current state at each step:
      - 'current': the current node
      - 'open_set': set of nodes in the open set
      - 'closed_set': set of nodes in the closed set
      - 'path': the current path (if found, else None)
    """
    
    def heuristic(current: Tuple[int, int], goal: Tuple[int, int]) -> int:
        return abs(current[0] - goal[0]) + abs(current[1] - goal[1])

    open_heap = []
    heapq.heappush(open_heap, (heuristic(start, end), 0, start))
    open_set = {start}
    came_from = {}
    g_score = {start: 0}
    f_score = {start: heuristic(start, end)}
    closed_set = set()

    # 4 directional movement for our maze
    neighbors = [(-1, 0), (1, 0), (0, -1), (0, 1)]

    while open_heap:
        current = heapq.heappop(open_heap)[2]
        open_set.discard(current)
        if current == end:
            # Reconstruct path
            path = [current]
            while current in came_from:
                current = came_from[current]
                path.append(current)
            path.reverse()
            yield {
                'current': current,
                'open_set': set(open_set),
                'closed_set': set(closed_set),
                'path': path
            }
            return
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
                if neighbor not in open_set:
                    heapq.heappush(open_heap, (f_score[neighbor], tentative_g_score, neighbor))
                    open_set.add(neighbor)
        yield {
            'current': current,
            'open_set': set(open_set),
            'closed_set': set(closed_set),
            'path': None
        }
    # No path found
    yield {
        'current': None,
        'open_set': set(),
        'closed_set': set(closed_set),
        'path': None
    }
    return