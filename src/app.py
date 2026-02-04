import pygame

import resources.core as core
import resources.styles as styles

from media.camera import Camera
from ui.main_ui import MainGUI
from ui.splash_screen import SplashScreen
from utils.files import Files
from utils.logger import setup_logger

logger = setup_logger(__name__)

class MainApp:
    def __init__(self):
        logger.info("Starting WiggleFrameStudio")
        self.screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
        pygame.display.set_caption("Wiggle Frame Studio")
        self.screen.fill(styles.BACKGROUND_COLOR)
        
        splash = SplashScreen(self.screen)
        splash.show_splash()
        
        frame = Files.check_frames(splash)
        self.cam = Camera(frame)
        self.gui = MainGUI(self.screen)
        self.running = True
        
        self.keymap = core.gui_keymap(self)

    def take_photo(self):
        filename = self.cam.capture_photo()
        logger.info(f"Frame saved: {filename}")

    def delete_last_frame(self):
        if (Files.delete_last_frame()):
            self.cam.set_frame_number(self.cam.get_frame_number() - 1)

    def handle_event(self, event):
        if event.type == pygame.QUIT:
            self.quit()
        elif event.type == pygame.KEYDOWN:
            action = self.keymap.get(event.key)
            if action:
                action()

    def run(self):
        logger.info("Running")
        while self.running:
            for event in pygame.event.get():
                self.handle_event(event)

            frame = self.cam.get_frame()
            self.gui.display_frame(frame)
             
        self.quit()
        
    def quit(self):
        self.cam.stop()
        self.running = False
        pygame.quit()
        exit()
