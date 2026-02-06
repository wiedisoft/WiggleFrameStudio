import pygame
from resources.translation import Translate
from resources.config import Config
from utils.logger import setup_logger

logger = setup_logger(__name__)
config = None
translate = None

def init():
    global config, translate
    Config.load()
    config = Config.get()
    translate = Translate(language=config.language)

def gui_keymap(app):
    return {
        pygame.K_q: app.quit,
        pygame.K_SPACE: app.take_photo,
        pygame.K_BACKSPACE: app.delete_last_frame,
        pygame.K_RETURN: app.save_movie,
        pygame.K_LALT: app.preview_movie
    }

def splash_keymap():
    return {
        pygame.K_q: "quit",
        pygame.K_RETURN: "return",
        pygame.K_BACKSPACE: "backspace",
    }