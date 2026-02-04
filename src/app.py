import pygame

from media.camera import Camera
import resources.core as core
import resources.styles as styles
from ui.main_ui import GUI
from ui.splashscreen import Splash_Screen
from utils.files import Files
from utils.logger import setup_logger

logger = setup_logger(__name__)

class MainApp:
    def __init__(self):
        logger.info("starting WiggleFrameStudio")
        self.screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
        self.screen.fill(styles.BACKGROUND_COLOR)
        Splash_Screen.show_splash(self.screen)
        self.keymap = core.gui_keymap(self)

        frame = Files.check_frames(self.screen)
        self.cam = Camera(frame)
        self.gui = GUI()
        self.running = True

    def quit(self):
        self.running = False

    def take_photo(self):
        filename = self.cam.capture_photo()
        logger.info(f"photo {filename} saved")

    def delete_last_frame(self):
        if (Files.delete_last_frame()):
            self.cam.set_frame_number(self.cam.get_frame_number() - 1)

    def run(self):
        logger.info("Running")
        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.quit()
                elif event.type == pygame.KEYDOWN:
                    action = self.keymap.get(event.key)
                    if action:
                        action()

            frame = self.cam.get_frame()
            self.gui.display_frame(frame)
            self.gui.tick(30)

        self.cam.stop()
        self.gui.quit()
