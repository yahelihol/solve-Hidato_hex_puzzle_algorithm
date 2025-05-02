import math
import pygame
from init import *


def cube_round(cube):
    """rounds a cube-coordinate (q, r, s) to the nearest hex cell."""
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
