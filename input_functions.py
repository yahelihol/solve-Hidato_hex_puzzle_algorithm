import threading
from hex_logic_functions import *
from hex_drawing_functions import *
from init import *

import threading

def reset_camera():

    camera_offset = [0, 0]
    zoom = 1
    board = generate_hex_board(SIZE)
    return board, camera_offset, zoom

def delete_hex(mouse_pos, CAM_X, CAM_Y, zoom, board):
    hex_under_mouse = cube_round(pixel_to_cube(mouse_pos, HEX_SIZE=HEX_SIZE, zoom=zoom, CAM_X=CAM_X, CAM_Y=CAM_Y))
    if hex_under_mouse in board:
        board[hex_under_mouse] = 0
    return board

def solve_by_hamiltonian_thread(board, path_to_draw):
    solver_thread = threading.Thread(target=solve_board_by_hamiltonian_path, args=(board, path_to_draw))
    solver_thread.start()
    return board
