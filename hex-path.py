import pygame
import random
import math
import time
import threading
from queue import *
global HEX_SIZE
from collections import deque, defaultdict

# Constants
SIZE = 5
WIDTH, HEIGHT = 800, 800
HEX_SIZE = 40
MARGIN = 10


# Colors
BACKGROUND_COLOR = (255, 255, 255)
HEX_COLOR = (230, 230, 230)
HEXFULL_COLOR = (230, 230, 255)
HIGHLIGHT_COLOR = (230, 250, 250)
HIGHLIGHT_2_COLOR = (144, 250, 144)
TEXT_COLOR = (0, 0, 0)

X_COLOR = (222, 0, 0)
Y_COLOR = (0, 222, 0)
Z_COLOR = (0, 0, 222)
global t_path
t_path= [-1, -1]
# Pygame setup
pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Hex Board")
font = pygame.font.SysFont(None, 24)

def cube_to_pixel(cube, HEX_SIZE = 50):
    x = HEX_SIZE * (math.sqrt(3) * cube[0] + math.sqrt(3) / 2 * cube[1])
    y = HEX_SIZE * (3 / 2 * cube[1])
    return (x + WIDTH // 2, y + HEIGHT // 2)

def hex_corners(center, HEX_SIZE = 50):
    corners = []
    for i in range(6):
        angle_rad = math.pi / 180 * (60 * i - 30)  # Adjusted angle for pointy-topped hexagons
        x = center[0] + HEX_SIZE * math.cos(angle_rad)
        y = center[1] + HEX_SIZE * math.sin(angle_rad)
        corners.append((x, y))
    return corners

def draw_hex(cube, value, coord=False, HEX_SIZE = 50, CAM_X=0, CAM_Y=0, color=HEX_COLOR, s = screen):
    #return
    center = (cube_to_pixel(cube, HEX_SIZE=HEX_SIZE)[0] + CAM_X, cube_to_pixel(cube, HEX_SIZE=HEX_SIZE)[1] + CAM_Y)
    corners = hex_corners(center, HEX_SIZE=HEX_SIZE)
    pygame.draw.polygon(s, color, corners)
    pygame.draw.polygon(s, (0, 0, 0), corners, 1)  # Add border for better visibility
    text = font.render(str(value), True, TEXT_COLOR)
    text_rect = text.get_rect(center=center)
    s.blit(text, text_rect)

    if coord:
        off = HEX_SIZE * math.sqrt(3/4) * 5/8
        off_x = (off / 2, off / math.sqrt(3) * 2)
        off_y = (off / 2, -off / math.sqrt(3) * 2)
        off_z = (-off / math.sqrt(3) * 2, 0)

        text = font.render(str(cube[0]), True, X_COLOR)
        text_rect = text.get_rect(center=(center[0] + off_x[0] , center[1] + off_x[1] ))
        s.blit(text, text_rect)
        text = font.render(str(cube[1]), True, Y_COLOR)
        text_rect = text.get_rect(center=(center[0] + off_y[0] , center[1] + off_y[1]) )
        s.blit(text, text_rect)
        text = font.render(str(cube[2]), True, Z_COLOR)
        text_rect = text.get_rect(center=(center[0] + off_z[0] , center[1] + off_z[1] ))
        s.blit(text, text_rect)


def generate_hex_board(size):
    board = {}
    for x in range(1-size, size):
        for y in range(max(1-size, 1-x-size), min(size, -x+size)):
            z = -x - y
            board[(x, y, z)] = 0

    return board

def fill_hex_board(type = 2):

    if SIZE == 5:
        #return {(-4, 0, 4): 38, (-4, 1, 3): 37, (-4, 2, 2): 31, (-4, 3, 1): 30, (-4, 4, 0): 29, (-3, -1, 4): 39, (-3, 0, 3): 36, (-3, 1, 2): 32, (-3, 2, 1): 46, (-3, 3, 0): 47, (-3, 4, -1): 28, (-2, -2, 4): 40, (-2, -1, 3): 35, (-2, 0, 2): 33, (-2, 1, 1): 45, (-2, 2, 0): 54, (-2, 3, -1): 48, (-2, 4, -2): 27, (-1, -3, 4): 10, (-1, -2, 3): 41, (-1, -1, 2): 34, (-1, 0, 1): 44, (-1, 1, 0): 55, (-1, 2, -1): 53, (-1, 3, -2): 49, (-1, 4, -3): 26, (0, -4, 4): 9, (0, -3, 3): 11, (0, -2, 2): 42, (0, -1, 1): 43, (0, 0, 0): 56, (0, 1, -1): 61, (0, 2, -2): 52, (0, 3, -3): 50, (0, 4, -4): 25, (1, -4, 3): 8, (1, -3, 2): 12, (1, -2, 1): 13, (1, -1, 0): 14, (1, 0, -1): 57, (1, 1, -2): 60, (1, 2, -3): 51, (1, 3, -4): 24, (2, -4, 2): 0, (2, -3, 1): 17, (2, -2, 0): 16, (2, -1, -1): 15, (2, 0, -2): 58, (2, 1, -3): 59, (2, 2, -4): 23, (3, -4, 1): 6, (3, -3, 0): 18, (3, -2, -1): 19, (3, -1, -2): 20, (3, 0, -3): 21, (3, 1, -4): 22, (4, -4, 0): 0, (4, -3, -1): 4, (4, -2, -2): 0, (4, -1, -3): 2, (4, 0, -4): 1}

        #return {(-4, 0, 4): 10, (-4, 1, 3): 11, (-4, 2, 2): 12, (-4, 3, 1): 13, (-4, 4, 0): 14, (-3, -1, 4): 9, (-3, 0, 3): 19, (-3, 1, 2): 18, (-3, 2, 1): 17, (-3, 3, 0): 16, (-3, 4, -1): 15, (-2, -2, 4): 8, (-2, -1, 3): 20, (-2, 0, 2): 21, (-2, 1, 1): 0, (-2, 2, 0): 0, (-2, 3, -1): 28, (-2, 4, -2): 29, (-1, -3, 4): 6, (-1, -2, 3): 7, (-1, -1, 2): 22, (-1, 0, 1): 0, (-1, 1, 0): 25, (-1, 2, -1): 27, (-1, 3, -2): 31, (-1, 4, -3): 30, (0, -4, 4): 1, (0, -3, 3): 5, (0, -2, 2): 0, (0, -1, 1): 55, (0, 0, 0): 56, (0, 1, -1): 0, (0, 2, -2): 32, (0, 3, -3): 33, (0, 4, -4): 34, (1, -4, 3): 2, (1, -3, 2): 4, (1, -2, 1): 0, (1, -1, 0): 0, (1, 0, -1): 0, (1, 1, -2): 0, (1, 2, -3): 0, (1, 3, -4): 35, (2, -4, 2): 3, (2, -3, 1): 49, (2, -2, 0): 51, (2, -1, -1): 60, (2, 0, -2): 39, (2, 1, -3): 0, (2, 2, -4): 36, (3, -4, 1): 48, (3, -3, 0): 50, (3, -2, -1): 61, (3, -1, -2): 44, (3, 0, -3): 0, (3, 1, -4): 0, (4, -4, 0): 47, (4, -3, -1): 46, (4, -2, -2): 45, (4, -1, -3): 0, (4, 0, -4): 0}
        return {(-4, 0, 4): 0, (-4, 1, 3): 0, (-4, 2, 2): 0, (-4, 3, 1): 0, (-4, 4, 0): 0, (-3, -1, 4): 0, (-3, 0, 3): 19, (-3, 1, 2): 18, (-3, 2, 1): 0, (-3, 3, 0): 0, (-3, 4, -1): 0, (-2, -2, 4): 0, (-2, -1, 3): 20, (-2, 0, 2): 21, (-2, 1, 1): 0, (-2, 2, 0): 0, (-2, 3, -1): 28, (-2, 4, -2): 29, (-1, -3, 4): 6, (-1, -2, 3): 0, (-1, -1, 2): 0, (-1, 0, 1): 0, (-1, 1, 0): 25, (-1, 2, -1): 27, (-1, 3, -2): 31, (-1, 4, -3): 30, (0, -4, 4): 1, (0, -3, 3): 0, (0, -2, 2): 0, (0, -1, 1): 55, (0, 0, 0): 56, (0, 1, -1): 0, (0, 2, -2): 32, (0, 3, -3): 33, (0, 4, -4): 34, (1, -4, 3): 0, (1, -3, 2): 0, (1, -2, 1): 0, (1, -1, 0): 0, (1, 0, -1): 0, (1, 1, -2): 0, (1, 2, -3): 0, (1, 3, -4): 35, (2, -4, 2): 0, (2, -3, 1): 49, (2, -2, 0): 51, (2, -1, -1): 60, (2, 0, -2): 39, (2, 1, -3): 0, (2, 2, -4): 36, (3, -4, 1): 48, (3, -3, 0): 50, (3, -2, -1): 61, (3, -1, -2): 44, (3, 0, -3): 0, (3, 1, -4): 0, (4, -4, 0): 47, (4, -3, -1): 46, (4, -2, -2): 45, (4, -1, -3): 0, (4, 0, -4): 0}
    if type == 1:
        return {(-5, 0, 5): 0, (-5, 1, 4): 0, (-5, 2, 3): 0, (-5, 3, 2): 0, (-5, 4, 1): 0, (-5, 5, 0): 0, (-4, -1, 5): 0, (-4, 0, 4): 16, (-4, 1, 3): 0, (-4, 2, 2): 0, (-4, 3, 1): 0, (-4, 4, 0): 0, (-4, 5, -1): 0, (-3, -2, 5): 0, (-3, -1, 4): 19, (-3, 0, 3): 0, (-3, 1, 2): 0, (-3, 2, 1): 0, (-3, 3, 0): 0, (-3, 4, -1): 0, (-3, 5, -2): 0, (-2, -3, 5): 0, (-2, -2, 4): 0, (-2, -1, 3): 0, (-2, 0, 2): 7, (-2, 1, 1): 0, (-2, 2, 0): 1, (-2, 3, -1): 38, (-2, 4, -2): 39, (-2, 5, -3): 0, (-1, -4, 5): 78, (-1, -3, 4): 0, (-1, -2, 3): 22, (-1, -1, 2): 0, (-1, 0, 1): 3, (-1, 1, 0): 0, (-1, 2, -1): 36, (-1, 3, -2): 0, (-1, 4, -3): 47, (-1, 5, -4): 0, (0, -5, 5): 0, (0, -4, 4): 0, (0, -3, 3): 74, (0, -2, 2): 0, (0, -1, 1): 0, (0, 0, 0): 0, (0, 1, -1): 0, (0, 2, -2): 0, (0, 3, -3): 0, (0, 4, -4): 0, (0, 5, -5): 0, (1, -5, 4): 0, (1, -4, 3): 0, (1, -3, 2): 0, (1, -2, 1): 0, (1, -1, 0): 0, (1, 0, -1): 67, (1, 1, -2): 0, (1, 2, -3): 0, (1, 3, -4): 0, (1, 4, -5): 52, (2, -5, 3): 0, (2, -4, 2): 0, (2, -3, 1): 84, (2, -2, 0): 0, (2, -1, -1): 0, (2, 0, -2): 0, (2, 1, -3): 32, (2, 2, -4): 0, (2, 3, -5): 54, (3, -5, 2): 0, (3, -4, 1): 83, (3, -3, 0): 0, (3, -2, -1): 0, (3, -1, -2): 62, (3, 0, -3): 0, (3, 1, -4): 0, (3, 2, -5): 0, (4, -5, 1): 91, (4, -4, 0): 0, (4, -3, -1): 0, (4, -2, -2): 0, (4, -1, -3): 61, (4, 0, -4): 58, (4, 1, -5): 0, (5, -5, 0): 0, (5, -4, -1): 0, (5, -3, -2): 88, (5, -2, -3): 0, (5, -1, -4): 0, (5, 0, -5): 0}
    if type == 2:
        return {(-5, 0, 5): 91, (-5, 1, 4): 90, (-5, 2, 3): 83, (-5, 3, 2): 82, (-5, 4, 1): 67, (-5, 5, 0): 66, (-4, -1, 5): 88, (-4, 0, 4): 89, (-4, 1, 3): 84, (-4, 2, 2): 81, (-4, 3, 1): 68, (-4, 4, 0): 65, (-4, 5, -1): 45, (-3, -2, 5): 87, (-3, -1, 4): 86, (-3, 0, 3): 85, (-3, 1, 2): 80, (-3, 2, 1): 69, (-3, 3, 0): 64, (-3, 4, -1): 46, (-3, 5, -2): 44, (-2, -3, 5): 76, (-2, -2, 4): 77, (-2, -1, 3): 78, (-2, 0, 2): 79, (-2, 1, 1): 70, (-2, 2, 0): 63, (-2, 3, -1): 47, (-2, 4, -2): 43, (-2, 5, -3): 23, (-1, -4, 5): 75, (-1, -3, 4): 74, (-1, -2, 3): 73, (-1, -1, 2): 72, (-1, 0, 1): 71, (-1, 1, 0): 62, (-1, 2, -1): 48, (-1, 3, -2): 42, (-1, 4, -3): 24, (-1, 5, -4): 22, (0, -5, 5): 56, (0, -4, 4): 57, (0, -3, 3): 58, (0, -2, 2): 59, (0, -1, 1): 60, (0, 0, 0): 61, (0, 1, -1): 49, (0, 2, -2): 41, (0, 3, -3): 25, (0, 4, -4): 21, (0, 5, -5): 1, (1, -5, 4): 55, (1, -4, 3): 54, (1, -3, 2): 53, (1, -2, 1): 52, (1, -1, 0): 51, (1, 0, -1): 50, (1, 1, -2): 40, (1, 2, -3): 26, (1, 3, -4): 20, (1, 4, -5): 2, (2, -5, 3): 34, (2, -4, 2): 35, (2, -3, 1): 36, (2, -2, 0): 37, (2, -1, -1): 38, (2, 0, -2): 39, (2, 1, -3): 27, (2, 2, -4): 19, (2, 3, -5): 3, (3, -5, 2): 33, (3, -4, 1): 32, (3, -3, 0): 31, (3, -2, -1): 30, (3, -1, -2): 29, (3, 0, -3): 28, (3, 1, -4): 18, (3, 2, -5): 4, (4, -5, 1): 12, (4, -4, 0): 13, (4, -3, -1): 14, (4, -2, -2): 15, (4, -1, -3): 16, (4, 0, -4): 17, (4, 1, -5): 5, (5, -5, 0): 11, (5, -4, -1): 10, (5, -3, -2): 9, (5, -2, -3): 8, (5, -1, -4): 7, (5, 0, -5): 6}
    return generate_hex_board(6)

def draw_board_outline(board, HEX_SIZE, CAM_X=0, CAM_Y=0):
    boundary_hexagons = set()
    for cube in board.keys():
        x, y, z = cube
        if x == 1 - SIZE or y == 1 - SIZE or z == 1 - SIZE or x == SIZE - 1 or y == SIZE - 1 or z == SIZE - 1:
            boundary_hexagons.add(cube)

    # Draw outline using the corners of boundary hexagons
    for cube in boundary_hexagons:
        center = (cube_to_pixel(cube, HEX_SIZE=HEX_SIZE)[0] + CAM_X, cube_to_pixel(cube, HEX_SIZE=HEX_SIZE)[1] + CAM_Y)
        corners = hex_corners(center, HEX_SIZE=HEX_SIZE)
        for i in range(6):
            start = corners[i]
            end = corners[(i + 1) % 6]  # Wrap around to connect the last corner to the first one
            pygame.draw.line(screen, (0, 0, 0), start, end, 5)



def clamp(val, start, end):
    return max(min(val, end), start)


def pixel_to_cube(pixel, HEX_SIZE=50, zoom=1, CAM_X=0, CAM_Y=0):
    x, y = pixel
    x = (x - WIDTH // 2 - CAM_X) / zoom
    y = (y - HEIGHT // 2 - CAM_Y) / zoom

    q = (math.sqrt(3) / 3 * x - 1 / 3 * y) / HEX_SIZE
    r = (2 / 3 * y) / HEX_SIZE
    s = -q - r

    return cube_round((q, r, s))

    def cube_to_pixel(cube, HEX_SIZE = 50):

     x = HEX_SIZE * (math.sqrt(3) * cube[0] + math.sqrt(3) / 2 * cube[1])
    y = HEX_SIZE * (3 / 2 * cube[1])
    return (x + WIDTH // 2, y + HEIGHT // 2)


def cube_round(cube):
    q, r, s = cube
    q_round = round(q)
    r_round = round(r)
    s_round = round(s)

    q_diff = abs(q_round - q)
    r_diff = abs(r_round - r)
    s_diff = abs(s_round - s)

    if q_diff > r_diff and q_diff > s_diff:
        q_round = -r_round - s_round
    elif r_diff > s_diff:
        r_round = -q_round - s_round
    else:
        s_round = -q_round - r_round

    return (q_round, r_round, s_round)

def get_adjacent_hexes(cube, board):
    directions = [
        (1, -1, 0), (-1, 1, 0),  # x-direction
        (1, 0, -1), (-1, 0, 1),  # y-direction
        (0, 1, -1), (0, -1, 1)   # z-direction
    ]

    adjacent_hexes = [(cube[0] + d[0], cube[1] + d[1], cube[2] + d[2]) for d in directions]
    return [hex for hex in adjacent_hexes if hex in board.keys()]

def populate_board(board):
    solve_board_by_map(board)
    return
    l = board.keys()
    for i in l:
        board[i] = 0
    ne = [(-0, 0, 0)]
    c = 1
    while (any([board[q] == 0 for q in l])):
        for h in l:
            if h in ne:
                if (board[h] == 0):
                    board[h] = c
                    c+=1
                    ne = get_adjacent_hexes(h, board)

def get_lists(board):
    board_of_sets_of_possible_values = {}
    board_size = len(board)
    values_determined = []
    values_undetermined = list(range(1, board_size + 1))
    cubes_undetermined = list(board.keys())
    cubes_determined = []
    for cube, value in board.items():
        if (value != 0):
            values_undetermined.remove(value)
            cubes_undetermined.remove(cube)
            values_determined.append(value)
            cubes_determined.append(cube)
            board_of_sets_of_possible_values[cube] = -1
        else:
            board_of_sets_of_possible_values[cube] = set()
    return values_determined, values_undetermined, cubes_undetermined, cubes_determined

def solve_board_by_map(board):
    board_of_sets_of_possible_values = {}
    board_size = len(board)
    values_determined = []
    values_undetermined = list(range(1, board_size+1))
    cubes_undetermined = list(board.keys())
    cubes_determined = []
    for cube, value in board.items():
        if (value != 0):
            values_undetermined.remove(value)
            cubes_undetermined.remove(cube)
            values_determined.append(value)
            cubes_determined.append(cube)
            board_of_sets_of_possible_values[cube] = -1
        else:
            board_of_sets_of_possible_values[cube] = set()
    if len(values_undetermined) == 0:
        print("board is full")
        return False
    if board_size in values_undetermined or 1 in values_undetermined:
        print("no defined start and end")
        return False

    possibilities = {}
    for cube in cubes_undetermined:
        possibilities[cube] = set()

    for num in values_undetermined:
        closest_up_index = index_of_smallest_greater_than(values_determined, num)
        closest_down_index = index_of_largest_smaller_than(values_determined, num)
        dist_up = values_determined[closest_up_index] - num
        dist_down = num - values_determined[closest_down_index]

        possible_places_up = get_neis_by_dist(cubes_determined[closest_up_index], dist_up, board, cubes_undetermined)

        possible_places_down = get_neis_by_dist(cubes_determined[closest_down_index], dist_down, board, cubes_undetermined)

        possible_places = possible_places_down & possible_places_up

        #print(num, dist_up, possible_places_down, possible_places_up)
        if len(possible_places) == 1:
            board[list(possible_places)[0]] = num
            return solve_board_by_map(board)
        for p in possible_places:
            possibilities[p].add(num)

    for p in possibilities.keys():
        if len(possibilities[p]) == 1:
            board[p] = list(possibilities[p])[0]
            return solve_board_by_map(board)




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

def solve_board_by_hamiltonian_path(board): # wroking method
    start_time = time.time()

    path = [-1] * len(board)
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
    if not hamiltonian_path_util(board, path, visited, 1, found):
        print("No Hamiltonian Path exists")
        return None
    else:
        for p in range(len(path)):
            board[path[p]] = p+1
        print("starting solve")
        end_time = time.time()
        execution_time = end_time - start_time
        print(f"Execution time: {execution_time} seconds")
        return path
def hamiltonian_path_util(board, path, visited, pos, found): # recursive part of working method
    if pos == len(board):
        return True

    for cube in get_adjacent_hexes(path[pos - 1], board):

        if cube not in visited and ((board[cube] == 0 and pos+1 not in found) or board[cube] == pos+1):  # can be optimized to check if path makes sense
            path[pos] = cube
            visited.add(cube)

            # Recur to construct the rest of the path
            if hamiltonian_path_util(board, path, visited, pos + 1, found):
                return True

            # If adding vertex v doesn't lead to a solution, remove it
            path[pos] = -1
            visited.remove(cube)
    #time.sleep(0.5)
    global t_path
    t_path = path
    return False


def find_isolated_groups(board, path = []):
    visited = set()
    groups = []

    def bfs(start):
        queue = deque([start])
        group = []
        while queue:
            node = queue.popleft()
            if node in visited:
                continue
            visited.add(node)
            group.append(node)
            x, y, z = node
            for neighbor in get_adjacent_hexes((x, y, z), board):
                if neighbor in board and board[neighbor] == 0 and neighbor not in path and neighbor not in visited:
                    queue.append(neighbor)
        return group

    for cell in board:
        if board[cell] == 0 and cell not in path and cell not in visited:
            group = bfs(cell)
            if group:
                groups.append(group)

    return groups


from collections import deque


def does_path_make_sense(board, path):
    #ahhhhhhhh
    return True


global groups_col
groups_col = []

def search_path(board, cube_start, cube_end):
    frontier = Queue()
    frontier.put(cube_start)
    reached = set()
    reached.add(cube_start)

    while not frontier.empty():
        current = frontier.get()
        for next_cube in get_adjacent_hexes(current, board):
            if board[next_cube] == 0 and next_cube not in reached:
                frontier.put(next_cube)
                reached.add(next_cube)
                if next_cube == cube_end:
                    return True
    return False



def d_path(path, zoom, CAM_X, CAM_Y):
    s = pygame.Surface((1000, 750), pygame.SRCALPHA)  # per-pixel alpha
    s.fill((255, 255, 255, 0))  # notice the alpha value in the color
    start, end = -1, -1
    for i in range(len(path)-1):
        cor = path[i]
        cor2 = path[i+1]
        if cor2 != -1:
            pos = cube_to_pixel(cor, HEX_SIZE=HEX_SIZE * zoom)
            pos2 = cube_to_pixel(cor2, HEX_SIZE=HEX_SIZE * zoom)
            pos = (pos[0] + CAM_X, pos[1] + CAM_Y)
            pos2 = (pos2[0] + CAM_X, pos2[1] + CAM_Y)
            pygame.draw.line(s, (33, 1, 111, 111), pos, pos2, 5)
            end = cor2
    if start != -1:
        pos = cube_to_pixel(start, HEX_SIZE=HEX_SIZE * zoom)
        pos = (pos[0] + CAM_X, pos[1] + CAM_Y)
        pygame.draw.circle(s, (33, 1, 111, 111), pos, 25, 5)
    if end != -1:
        pos = cube_to_pixel(end, HEX_SIZE=HEX_SIZE * zoom)
        pos = (pos[0] + CAM_X, pos[1] + CAM_Y)
        pygame.draw.circle(s, (33, 1, 111, 111), pos, 25, 5)
    screen.blit(s, (0, 0))

def solve_board_by_hamiltonian_sub_path_many(board):
    values_determined, values_undetermined, cubes_undetermined, cubes_determined = get_lists(board)
    cube_smallest_value = cubes_determined.index(min(values_determined))
    ## idk what the f i am doing here sorry
    return
def solve_board_by_hamiltonian_sub_path(board, cube_start, cube_end):
    if board[cube_start] == -1 or board[cube_end] == -1:
        return False
    l = board[cube_end] - board[cube_start]
    path = [-1] * (l+1)
    found = {num for num in board.values() if num in range(board[cube_start], board[cube_end]+1)}
    # Let the first vertex in the path be the 1
    path[0] = cube_start

    # Use backtracking to find the Hamiltonian Path
    if not hamiltonian_sub_path_util(board, path, 1, found, board[cube_start]):
        return None
    else:
        #for p in range(len(path)):
        #    board[path[p]] = p+1
        return path
def hamiltonian_sub_path_util(board, path, pos, found, start):
    if pos == len(path):
        return True
    for cube in get_adjacent_hexes(path[pos - 1], board):
        if cube not in path and ((board[cube] == 0 and pos+start not in found) or board[cube] == pos+start):
            path[pos] = cube

            # Recur to construct the rest of the path
            if hamiltonian_sub_path_util(board, path, pos + 1, found, start):
                return True

            # If adding vertex v doesn't lead to a solution, remove it
            path[pos] = -1
    return False


def change_v(mouse_pos, zoom, CAM_X, CAM_Y, board, v):
    hex_under_mouse = cube_round(pixel_to_cube(mouse_pos, HEX_SIZE=HEX_SIZE, zoom=zoom, CAM_X=CAM_X, CAM_Y=CAM_Y))
    if hex_under_mouse in board:
        board[hex_under_mouse] = board[hex_under_mouse] * 10 + v  # Increment value in the hex under mouse

def main():
    board = generate_hex_board(SIZE)
    adjacent_hexes = {cube: get_adjacent_hexes(cube, board) for cube in board.keys()} # use once instead of every time !!implement!!
    detail_board = generate_hex_board(SIZE)
    clock = pygame.time.Clock()
    running = True
    zoom = 1
    camera_offset = [0, 0]
    panning, pan_start, pan_end = False, [0, 0], [0, 0]
    draw_path = True
    possiblity_board = []
    global t_path
    global groups_col
    t_path = [-1, -1]
    tracing = -1
    while running:
        mouse_pos = pygame.mouse.get_pos()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            elif event.type == pygame.MOUSEBUTTONDOWN:
                pan_start = mouse_pos
                panning = True

            elif event.type == pygame.MOUSEBUTTONUP:
                panning = False

            elif event.type == pygame.MOUSEWHEEL:
                if event.y > 0:  # Scrolled up
                    zoom += event.y * 0.3
                    camera_offset[0] -= (mouse_pos[0] - WIDTH/2) * event.y * 0.3
                    camera_offset[1] -= (mouse_pos[1] - HEIGHT / 2) * event.y * 0.3
                elif event.y < 0 and zoom > 0.4:  # Scrolled down
                    zoom += event.y * 0.3
                    camera_offset[0] -= (mouse_pos[0] - WIDTH / 2) * event.y * 0.3
                    camera_offset[1] = (mouse_pos[1] - HEIGHT / 2) * event.y * 0.3
                zoom = clamp(zoom, 0.4, 8)
                camera_offset[0] = clamp(camera_offset[0], -WIDTH/2 * zoom, WIDTH/2 * zoom)
                camera_offset[1] = clamp(camera_offset[1], -HEIGHT / 2 * zoom, HEIGHT / 2 * zoom)

            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:  # Reset
                    camera_offset = [0, 0]
                    zoom = 1
                    board = generate_hex_board(SIZE)
                elif event.key == pygame.K_DELETE:
                    hex_under_mouse = cube_round(
                        pixel_to_cube(mouse_pos, HEX_SIZE=HEX_SIZE, zoom=zoom, CAM_X=CAM_X, CAM_Y=CAM_Y))
                    if hex_under_mouse in board:
                        board[hex_under_mouse] = board[hex_under_mouse] = 0
                elif event.key == pygame.K_p:
                    print(board)
                    temp = []
                    groups_col = find_isolated_groups(board, temp)
                elif event.key == pygame.K_s:
                    print(does_path_make_sense(board, []))
                elif event.key == pygame.K_f:
                    start_time = time.time()
                    populate_board(board) ###
                    end_time = time.time()
                    execution_time = end_time - start_time
                    print(f"Execution time: {execution_time} seconds")
                elif event.key == pygame.K_t:
                    possiblity_board = solve_board_by_map(board)
                elif event.key == pygame.K_h:
                    solver_thread = threading.Thread(target=solve_board_by_hamiltonian_path, args=(board,))
                    solver_thread.start()
                elif event.key == pygame.K_j:
                    hex_under_mouse = cube_round(
                        pixel_to_cube(mouse_pos, HEX_SIZE=HEX_SIZE, zoom=zoom, CAM_X=CAM_X, CAM_Y=CAM_Y))
                    solve_board_by_hamiltonian_sub_path(board,(0,0,0), hex_under_mouse)
                elif event.key in range(pygame.K_0, pygame.K_9+1):
                    change_v(mouse_pos, zoom, camera_offset[0], camera_offset[1], board, event.key - pygame.K_0)
                elif event.key == pygame.K_BACKSLASH:
                    tracing = []
                    hex_under_mouse = cube_round(pixel_to_cube(mouse_pos, HEX_SIZE=HEX_SIZE, zoom=zoom, CAM_X=CAM_X, CAM_Y=CAM_Y))
                    if hex_under_mouse in board:
                        tracing.append(hex_under_mouse)
                        board[hex_under_mouse] = 1
                elif event.key == pygame.K_SLASH:
                    for i in range(0, len(tracing)):
                        board[tracing[i]] = i+1
                    tracing = -1
                elif event.key == pygame.K_m:
                    board = {(-5, 0, 5): 0, (-5, 1, 4): 1, (-5, 2, 3): 0, (-5, 3, 2): 0, (-5, 4, 1): 0, (-5, 5, 0): 7, (-4, -1, 5): 0, (-4, 0, 4): 0, (-4, 1, 3): 0, (-4, 2, 2): 0, (-4, 3, 1): 15, (-4, 4, 0): 0, (-4, 5, -1): 0, (-3, -2, 5): 0, (-3, -1, 4): 91, (-3, 0, 3): 0, (-3, 1, 2): 0, (-3, 2, 1): 0, (-3, 3, 0): 0, (-3, 4, -1): 0, (-3, 5, -2): 0, (-2, -3, 5): 0, (-2, -2, 4): 82, (-2, -1, 3): 85, (-2, 0, 2): 19, (-2, 1, 1): 18, (-2, 2, 0): 0, (-2, 3, -1): 13, (-2, 4, -2): 11, (-2, 5, -3): 0, (-1, -4, 5): 0, (-1, -3, 4): 71, (-1, -2, 3): 0, (-1, -1, 2): 0, (-1, 0, 1): 0, (-1, 1, 0): 0, (-1, 2, -1): 0, (-1, 3, -2): 0, (-1, 4, -3): 0, (-1, 5, -4): 0, (0, -5, 5): 0, (0, -4, 4): 0, (0, -3, 3): 0, (0, -2, 2): 68, (0, -1, 1): 43, (0, 0, 0): 0, (0, 1, -1): 0, (0, 2, -2): 30, (0, 3, -3): 0, (0, 4, -4): 0, (0, 5, -5): 0, (1, -5, 4): 0, (1, -4, 3): 0, (1, -3, 2): 0, (1, -2, 1): 0, (1, -1, 0): 0, (1, 0, -1): 41, (1, 1, -2): 0, (1, 2, -3): 0, (1, 3, -4): 0, (1, 4, -5): 0, (2, -5, 3): 0, (2, -4, 2): 0, (2, -3, 1): 0, (2, -2, 0): 0, (2, -1, -1): 0, (2, 0, -2): 0, (2, 1, -3): 0, (2, 2, -4): 0, (2, 3, -5): 0, (3, -5, 2): 0, (3, -4, 1): 0, (3, -3, 0): 0, (3, -2, -1): 0, (3, -1, -2): 0, (3, 0, -3): 37, (3, 1, -4): 0, (3, 2, -5): 0, (4, -5, 1): 0, (4, -4, 0): 61, (4, -3, -1): 0, (4, -2, -2): 0, (4, -1, -3): 0, (4, 0, -4): 0, (4, 1, -5): 0, (5, -5, 0): 0, (5, -4, -1): 60, (5, -3, -2): 55, (5, -2, -3): 0, (5, -1, -4): 0, (5, 0, -5): 0}

        if tracing != -1:
            hex_under_mouse = cube_round(
                pixel_to_cube(mouse_pos, HEX_SIZE=HEX_SIZE, zoom=zoom, CAM_X=CAM_X, CAM_Y=CAM_Y))
            if hex_under_mouse in board and tracing[-1] != hex_under_mouse:
                tracing.append(hex_under_mouse)
                board[tracing[len(tracing)-1]] = len(tracing)


        if panning:  # If panning
            pan_end = pygame.mouse.get_pos()
            delta_x = pan_end[0] - pan_start[0]
            delta_y = pan_end[1] - pan_start[1]
            camera_offset[0] = camera_offset[0] + delta_x
            camera_offset[1] = camera_offset[1] + delta_y
            pan_start = pan_end

        CAM_X = camera_offset[0]
        CAM_Y = camera_offset[1]

        screen.fill(BACKGROUND_COLOR)
        draw_board_outline(board, HEX_SIZE=HEX_SIZE*zoom, CAM_X=CAM_X, CAM_Y=CAM_Y)

        for cube, value in board.items():
            if value == 0:
                draw_hex(cube, value, coord=False, HEX_SIZE=HEX_SIZE * zoom, CAM_X=CAM_X, CAM_Y=CAM_Y, color=HEX_COLOR)
            else:
                draw_hex(cube, value, coord=False, HEX_SIZE=HEX_SIZE * zoom, CAM_X=CAM_X, CAM_Y=CAM_Y, color=HEXFULL_COLOR)


        hex_under_mouse = cube_round(pixel_to_cube(mouse_pos, HEX_SIZE=HEX_SIZE, zoom=zoom, CAM_X=CAM_X, CAM_Y=CAM_Y))
        if hex_under_mouse in board.keys():
            draw_hex(hex_under_mouse, board[hex_under_mouse], coord=True, HEX_SIZE=HEX_SIZE*zoom, CAM_X=CAM_X, CAM_Y=CAM_Y, color=HIGHLIGHT_2_COLOR)
            for adjacent_hex in get_adjacent_hexes(hex_under_mouse, board):
                draw_hex(adjacent_hex, board[adjacent_hex], coord=False, HEX_SIZE=HEX_SIZE * zoom, CAM_X=CAM_X,
                         CAM_Y=CAM_Y, color=HIGHLIGHT_COLOR)
        if t_path != [-1, -1]:
            d_path(t_path, zoom, CAM_X, CAM_Y)
        if draw_path:
            s = pygame.Surface((1000, 750), pygame.SRCALPHA)  # per-pixel alpha
            s.fill((255, 255, 255, 0))  # notice the alpha value in the color
            for c in range(1, len(board)):
                for cor in board.keys():
                    if board[cor] == c:
                        for cor2 in get_adjacent_hexes(cor, board):
                            if board[cor2] == c+1:
                                pos = cube_to_pixel(cor, HEX_SIZE=HEX_SIZE*zoom)
                                pos2 = cube_to_pixel(cor2,HEX_SIZE=HEX_SIZE*zoom)
                                pos = (pos[0] + CAM_X, pos[1] + CAM_Y)
                                pos2 = (pos2[0] + CAM_X, pos2[1] + CAM_Y)
                                pygame.draw.line(s, (222, 1, 33, 111), pos, pos2, 5)
            start, end = -1, -1
            for cube, value in board.items():
                if value == 1:
                    start = cube
                if value == len(board):
                    end = cube
            if start != -1:
                pos = cube_to_pixel(start, HEX_SIZE=HEX_SIZE * zoom)
                pos = (pos[0] + CAM_X, pos[1] + CAM_Y)
                pygame.draw.circle(s, (222, 1, 33, 111), pos, 25, 5)
            if end != -1:
                pos = cube_to_pixel(end, HEX_SIZE=HEX_SIZE * zoom)
                pos = (pos[0] + CAM_X, pos[1] + CAM_Y)
                pygame.draw.circle(s, (222, 1, 33, 111), pos, 25, 5)
            screen.blit(s, (0, 0))

        rect = pygame.Rect(mouse_pos[0] - 25, mouse_pos[1] - 25, 50, 50)
        pygame.draw.rect(screen, X_COLOR, rect, 2)  # Draw rectangle with border


        if groups_col != []:
            a = 0
            for i in groups_col:
                a += 1
                for j in i:
                    center = (cube_to_pixel(j, HEX_SIZE=HEX_SIZE)[0] + CAM_X,
                              cube_to_pixel(j, HEX_SIZE=HEX_SIZE)[1] + CAM_Y)
                    text = font.render(str(a), True, (111, 111, 22))
                    text_rect = text.get_rect(center=(center[0], center[1]+ 16))
                    screen.blit(text, text_rect)



        pygame.display.flip()
        clock.tick(30)

    pygame.quit()

if __name__ == "__main__":
    main()


