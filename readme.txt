
See image

run main

Hex Grid Visualization and Hex-Hidato Solver in pygame
look up Hidato rules online


Features
- Hexagonal Grid: Visualize a hexagonal grid with custom values.
- Interactive: Zoom in/out, pan the grid, and modify hex values using mouse and keyboard inputs.
- Pathfinding: Draw paths between hexes based on values and solve puzzles like Hamiltonian paths.
- Visual Feedback: Highlights specific hexes and their neighbors for easier navigation.

Controls
Mouse:
- Left-click and drag to pan the camera.
- Scroll to zoom in or out.
- Hover over a hex to highlight it and its neighbors.

Keyboard:
0-9: Change the value of the hex under the mouse (appends the number, so you can press 3, then 4 for 34).
R: Reset the board, camera and zoom level.
DELETE: Delete the hex under the mouse.
H: Start solving a Hamiltonian path (runs in a separate thread).
P: Print board.
M: Load a predefined puzzle board based on SIZE (default is 5).


Will draw paths between hexes based on their values, starting from the hex marked with the value 1 to the hex marked with the highest value.

Solves puzzle using a modified Hamiltonian path algorithm (there might be other optimizations for larger boards).
The pathfinding logic includes:
A Breadth-First Search (BFS) algorithm (search_path) to find paths between two hexes.
A Hamiltonian path solver that finds a specific path through all the hexes.