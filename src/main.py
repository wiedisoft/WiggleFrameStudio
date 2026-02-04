import pygame

from app import MainApp
import resources.core as core

if __name__ == "__main__":
    pygame.init()
    core.init()
    app = MainApp()
    app.run()