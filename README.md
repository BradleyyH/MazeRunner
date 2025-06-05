# Maze Runner

An A* search algorithm finding the optimal solution through procedurally generated maps in python.
This will utilise libraries like Pygame and numpy.

## Controls

- Left click to create new random maze
- Space to pause search algorithm
- Up/Down arrow to change speed A* is shown
- R to restart the A* search

## Setup

1. Create a virtual environment (recommended):
```bash
python -m venv venv
source venv/bin/activate  # On Unix/macOS
# or
.\venv\Scripts\activate  # On Windows
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Run the maze environment:
```bash
python mazeEnvironment.py
```

## Planned Features
- [x] Procedural maze generation using recursive backtracking
- [x] A* pathfinding algorithm
- [ ] Visualising optimal path being found in real time
