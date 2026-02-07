import pygame

import resources.core as core
from app import MainApp

if __name__ == "__main__":
    pygame.init()
    core.init()
    app = MainApp()
    app.run()
