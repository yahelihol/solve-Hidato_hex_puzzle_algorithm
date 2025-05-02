import pygame
import random
import math
import time
import threading
from queue import *

from pygame.examples.music_drop_fade import draw_text_line

global HEX_SIZE
from collections import deque, defaultdict


from input_functions import *
from hex_logic_functions import *
from hex_drawing_functions import *
from init import *







def clamp(val, start, end):
    return max(min(val, end), start)


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



def change_v(mouse_pos, zoom, CAM_X, CAM_Y, board, v):
    hex_under_mouse = cube_round(pixel_to_cube(mouse_pos, HEX_SIZE=HEX_SIZE, zoom=zoom, CAM_X=CAM_X, CAM_Y=CAM_Y))
    if hex_under_mouse in board:
        board[hex_under_mouse] = board[hex_under_mouse] * 10 + v  # Increment value in the hex under mouse
    return board



def main():
    zoom = 1
    camera_offset = [0, 0]
    board = {}
    clock = pygame.time.Clock()
    board = generate_hex_board(SIZE)
    adjacent_hexes = {cube: get_adjacent_hexes(cube, board) for cube in board.keys()} # use once instead of every time !!implement!!
    detail_board = generate_hex_board(SIZE)
    CAM_X = camera_offset[0]
    CAM_Y = camera_offset[1]
    running = True
    panning, pan_start, pan_end = False, [0, 0], [0, 0]
    draw_path = True
    path_to_draw = [-1] * len(board)
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


            if event.type == pygame.KEYDOWN:
                if event.type == pygame.KEYDOWN:
                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_t:
                            board = solve_by_possibilities(board)
                        elif event.key == pygame.K_r:
                            board, camera_offset, zoom = reset_camera()
                        elif event.key == pygame.K_DELETE:
                            delete_hex(mouse_pos, CAM_X, CAM_Y, zoom, board)
                        elif event.key == pygame.K_h:
                            solve_by_hamiltonian_thread(board, path_to_draw)
                        elif event.key == pygame.K_p:
                            print(board)
                            blocked, pockets = count_pockets(board, [], set())
                            print(pockets)
                        elif event.key == pygame.K_m:
                            if SIZE == 5:
                                board = {(-4, 0, 4): 0, (-4, 1, 3): 0, (-4, 2, 2): 0, (-4, 3, 1): 46, (-4, 4, 0): 0, (-3, -1, 4): 0, (-3, 0, 3): 41, (-3, 1, 2): 44, (-3, 2, 1): 0, (-3, 3, 0): 0, (-3, 4, -1): 48, (-2, -2, 4): 0, (-2, -1, 3): 0, (-2, 0, 2): 0, (-2, 1, 1): 0, (-2, 2, 0): 53, (-2, 3, -1): 0, (-2, 4, -2): 0, (-1, -3, 4): 0, (-1, -2, 3): 37, (-1, -1, 2): 35, (-1, 0, 1): 31, (-1, 1, 0): 0, (-1, 2, -1): 0, (-1, 3, -2): 1, (-1, 4, -3): 0, (0, -4, 4): 0, (0, -3, 3): 0, (0, -2, 2): 27, (0, -1, 1): 0, (0, 0, 0): 0, (0, 1, -1): 61, (0, 2, -2): 0, (0, 3, -3): 2, (0, 4, -4): 0, (1, -4, 3): 0, (1, -3, 2): 0, (1, -2, 1): 26, (1, -1, 0): 0, (1, 0, -1): 0, (1, 1, -2): 56, (1, 2, -3): 0, (1, 3, -4): 0, (2, -4, 2): 0, (2, -3, 1): 25, (2, -2, 0): 15, (2, -1, -1): 13, (2, 0, -2): 0, (2, 1, -3): 0, (2, 2, -4): 0, (3, -4, 1): 0, (3, -3, 0): 0, (3, -2, -1): 0, (3, -1, -2): 0, (3, 0, -3): 9, (3, 1, -4): 0, (4, -4, 0): 0, (4, -3, -1): 0, (4, -2, -2): 0, (4, -1, -3): 0, (4, 0, -4): 0}
                            if SIZE == 6:
                                board = {(-5, 0, 5): 0, (-5, 1, 4): 1, (-5, 2, 3): 0, (-5, 3, 2): 0, (-5, 4, 1): 0, (-5, 5, 0): 7, (-4, -1, 5): 0, (-4, 0, 4): 0, (-4, 1, 3): 0, (-4, 2, 2): 0, (-4, 3, 1): 15, (-4, 4, 0): 0, (-4, 5, -1): 0, (-3, -2, 5): 0, (-3, -1, 4): 91, (-3, 0, 3): 0, (-3, 1, 2): 0, (-3, 2, 1): 0, (-3, 3, 0): 0, (-3, 4, -1): 0, (-3, 5, -2): 0, (-2, -3, 5): 0, (-2, -2, 4): 82, (-2, -1, 3): 85, (-2, 0, 2): 19, (-2, 1, 1): 18, (-2, 2, 0): 0, (-2, 3, -1): 13, (-2, 4, -2): 11, (-2, 5, -3): 0, (-1, -4, 5): 0, (-1, -3, 4): 71, (-1, -2, 3): 0, (-1, -1, 2): 0, (-1, 0, 1): 0, (-1, 1, 0): 0, (-1, 2, -1): 0, (-1, 3, -2): 0, (-1, 4, -3): 0, (-1, 5, -4): 0, (0, -5, 5): 0, (0, -4, 4): 0, (0, -3, 3): 0, (0, -2, 2): 68, (0, -1, 1): 43, (0, 0, 0): 0, (0, 1, -1): 0, (0, 2, -2): 30, (0, 3, -3): 0, (0, 4, -4): 0, (0, 5, -5): 0, (1, -5, 4): 0, (1, -4, 3): 0, (1, -3, 2): 0, (1, -2, 1): 0, (1, -1, 0): 0, (1, 0, -1): 41, (1, 1, -2): 0, (1, 2, -3): 0, (1, 3, -4): 0, (1, 4, -5): 0, (2, -5, 3): 0, (2, -4, 2): 0, (2, -3, 1): 0, (2, -2, 0): 0, (2, -1, -1): 0, (2, 0, -2): 0, (2, 1, -3): 0, (2, 2, -4): 0, (2, 3, -5): 0, (3, -5, 2): 0, (3, -4, 1): 0, (3, -3, 0): 0, (3, -2, -1): 0, (3, -1, -2): 0, (3, 0, -3): 37, (3, 1, -4): 0, (3, 2, -5): 0, (4, -5, 1): 0, (4, -4, 0): 61, (4, -3, -1): 0, (4, -2, -2): 0, (4, -1, -3): 0, (4, 0, -4): 0, (4, 1, -5): 0, (5, -5, 0): 0, (5, -4, -1): 60, (5, -3, -2): 55, (5, -2, -3): 0, (5, -1, -4): 0, (5, 0, -5): 0}
                        elif pygame.K_0 <= event.key <= pygame.K_9:
                            change_v(mouse_pos, zoom, camera_offset[0], camera_offset[1], board, event.key - pygame.K_0)


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


        """
        blocked, pockets = count_pockets(board, [], set())
        for c, v in blocked.items():
            if v == 0:
                pygame.draw.circle(screen, (111, 2, 2, 111), cube_to_pixel(c, HEX_SIZE=HEX_SIZE * zoom), 15, 3)
            if v == 1:
                pygame.draw.circle(screen, (2, 111, 2, 111), cube_to_pixel(c, HEX_SIZE=HEX_SIZE * zoom), 15, 3)
            if v == 2:
                pygame.draw.circle(screen, (2, 2, 111, 111), cube_to_pixel(c, HEX_SIZE=HEX_SIZE * zoom), 15, 3)
        """

        hex_under_mouse = cube_round(pixel_to_cube(mouse_pos, HEX_SIZE=HEX_SIZE, zoom=zoom, CAM_X=CAM_X, CAM_Y=CAM_Y))
        if hex_under_mouse in board.keys():
            draw_hex(hex_under_mouse, board[hex_under_mouse], coord=True, HEX_SIZE=HEX_SIZE*zoom, CAM_X=CAM_X, CAM_Y=CAM_Y, color=HIGHLIGHT_2_COLOR)
            for adjacent_hex in get_adjacent_hexes(hex_under_mouse, board):
                draw_hex(adjacent_hex, board[adjacent_hex], coord=False, HEX_SIZE=HEX_SIZE * zoom, CAM_X=CAM_X,
                         CAM_Y=CAM_Y, color=HIGHLIGHT_COLOR)
        d_path(path_to_draw, zoom, CAM_X, CAM_Y)
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




        pygame.display.flip()
        clock.tick(30)

    pygame.quit()

if __name__ == "__main__":
    main()


