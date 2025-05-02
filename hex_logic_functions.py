
import time
from collections import deque, defaultdict

from numpy.matlib import empty

def generate_hex_board(size):
    board = {}
    for x in range(1-size, size):
        for y in range(max(1-size, 1-x-size), min(size, -x+size)):
            z = -x - y
            board[(x, y, z)] = 0

    return board



def get_adjacent_hexes(cube, board):
    directions = [
        (1, -1, 0), (-1, 1, 0),  # x-direction
        (1, 0, -1), (-1, 0, 1),  # y-direction
        (0, 1, -1), (0, -1, 1)   # z-direction
    ]

    adjacent_hexes = [(cube[0] + d[0], cube[1] + d[1], cube[2] + d[2]) for d in directions]
    return [hex for hex in adjacent_hexes if hex in board.keys()]








def get_neis_by_dist(start, dist, board, cubes_undetermined):
    possible_places = set()
    possible_places.add(start)
    for i in range(dist):
        new_possible_places = set()
        for s in possible_places:
            for n in get_adjacent_hexes(s, board):
                if n in cubes_undetermined:
                    new_possible_places.add(n)

        possible_places = new_possible_places
    return possible_places

def index_of_smallest_greater_than(lst, num):
    # Initialize variables to keep track of the smallest number and its index
    smallest_greater = None
    index_of_smallest = -1
    # Iterate over the list with indices
    for i, value in enumerate(lst):
        if value > num:
            if smallest_greater is None or value < smallest_greater:
                smallest_greater = value
                index_of_smallest = i

    return index_of_smallest


def index_of_largest_smaller_than(lst, num):
    # Initialize variables to keep track of the largest number and its index
    largest_smaller = None
    index_of_largest = -1

    # Iterate over the list with indices
    for i, value in enumerate(lst):
        if value < num:
            if largest_smaller is None or value > largest_smaller:
                largest_smaller = value
                index_of_largest = i

    return index_of_largest

def solve_board_by_hamiltonian_path(board, path_to_draw): # wroking method
    start_time = time.time()
    size = len(board)
    path = [-1] * size
    visited = set()
    found = {num for num in board.values() if num != 0}
    # Let the first vertex in the path be the 1
    for cube, value in board.items():
        if value == 1:
            path[0] = cube
            visited.add(cube)

    if path[0] == -1:
        return None

    # Use backtracking to find the Hamiltonian Path
    if not hamiltonian_path_util(board, path, visited, 1, found, path_to_draw):
        print("No Hamiltonian Path exists")
        return None
    else:
        for p in range(len(path)):
            board[path[p]] = p+1
        for i in range(size):
            path_to_draw[i] = -1
        print("starting solve")
        end_time = time.time()
        execution_time = end_time - start_time
        print(f"Execution time: {execution_time} seconds")
        return path
def hamiltonian_path_util(board, path, visited, pos, found, path_to_draw): # recursive part of working method
    size = len(board)
    if pos == size:
        return True

    for cube in get_adjacent_hexes(path[pos - 1], board):

        if cube not in visited and ((board[cube] == 0 and pos+1 not in found) or board[cube] == pos+1) :  # can be optimized to prune dead ends
            path[pos] = cube
            visited.add(cube)

            # Recur to construct the rest of the path
            if is_remaining_area_connected(board, visited, pos + 1, found):  # <---- Connectivity pruning here
                if hamiltonian_path_util(board, path, visited, pos + 1, found, path_to_draw):
                    return True

            # If adding vertex v doesn't lead to a solution, remove it (backtracking)
            path[pos] = -1
            visited.remove(cube)

    for i in range(size):
        path_to_draw[i] = path[i]
    return False



def is_remaining_area_connected(board, visited, current_step, found):
    # Cells that can still be visited in the future:
    def is_future_usable(cell):
        val = board[cell]
        return (
            cell not in visited and
            (
                val == 0 or            # empty
                (val > current_step and val in found)  # scheduled for later
            )
        )

    usable = {cell for cell in board if is_future_usable(cell)}
    if not usable:
        return True

    # Start flood fill from any usable cell
    start = next(iter(usable))
    reachable = set()
    stack = [start]

    while stack:
        current = stack.pop()
        if current in reachable:
            continue
        reachable.add(current)
        for neighbor in get_adjacent_hexes(current, board):
            if neighbor in usable and neighbor not in reachable:
                stack.append(neighbor)

    return len(reachable) == len(usable)



def is_on_boundary(coord, size):
    x, y, z = coord
    max_distance = size - 1
    return max(abs(x), abs(y), abs(z)) == max_distance



def count_pockets(board, path, visited):
    blocked = {}
    pockets = 0
    for c, v in board.items():
        if v == 0 and c not in visited:
            blocked[c] = 0
        else:
            blocked[c] = 1
    if path:
        blocked[path[-1]] = 0


    # Check all grid cells
    for c, v in blocked.items():
        if v == 2:
            continue
        if v == 1:
            continue
        if v == 0:
            pockets += 1
            queue = deque()
            queue.append(c)
            while queue:
                cube = queue.popleft()
                if cube == -1:
                    continue
                blocked[cube] = 2
                for adjacent_hex in get_adjacent_hexes(cube, board):
                    if blocked[adjacent_hex] == 0:
                        queue.append(adjacent_hex)


    return blocked, pockets












def largest_smaller_than(arr, n):
    result = None
    for num in arr:
        if num < n:
            result = num
        else:
            break  # since list is ordered, we can stop early
    return result

def smallest_greater_than(arr, n):
    for num in arr:
        if num > n:
            return num
    return None  # No number greater than n found



def solve_by_possibilities(board):
    diction = {i: [] for i in range(1, len(board)+1)}
    known = []
    for c, v in board.items():
        if v != 0:
            diction[v] = [c]
            known.append(v)

    for v, options in diction.items():
        if options is []:
            nex = smallest_greater_than(known, v)
            pre = largest_smaller_than(known, v)


    #?????

    print(diction)

    return board