import threading
import pygame
pygame.init()
SIZE = 5
WIDTH, HEIGHT = 800, 800
HEX_SIZE = 40
MARGIN = 10

font = pygame.font.SysFont(None, 24)

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

