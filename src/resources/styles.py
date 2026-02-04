import os
import pygame
from utils.logger import setup_logger

logger = setup_logger(__name__)
pygame.init()

# Fonts
path = "assets/Chewy-Regular.ttf"
if not os.path.exists(path):
    logger.error(f"translation file not found: {path}")
    raise FileNotFoundError(f"translation file not found: {path}")

FONT_LOGO = pygame.font.Font(path, 160)
FONT_SUB_TITLE = pygame.font.Font(path, 80)
FONT_REGULAR = pygame.font.Font(path, 30)
FONT_SMALL = pygame.font.Font(path, 30)
FONT_TINY = pygame.font.Font(path, 20)

FONT_COLOR_TITLE = (255, 255, 255)
FONT_COLOR_SUB_TITLE = (200, 200, 200)

COLOR_HIGHLIGHT = (253, 91, 78)
COLOR_ACCENT = (254, 202, 56)
COLOR_FOREGROUND = (0, 174, 199)
COLOR_FOREGROUND_DARK = (9, 36, 66)

BACKGROUND_COLOR = (1, 5, 32) 