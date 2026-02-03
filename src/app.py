from ui.splashscreen import SplashScreen
from utils.logger import setup_logger
from utils.files import Files
from camera import Camera
from gui import GUI
import pygame
from utils.config import Config

logger = setup_logger(__name__)
Config().load()
config = Config().get()

class MainApp:
    def __init__(self):
        logger.info("Initialisiere")
        pygame.init()
        self.screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
        SplashScreen.show_splash(self.screen, "assets/logo_dark.png")
        
        self.keymap = {
            pygame.K_q: self.quit,
            pygame.K_SPACE: self.take_photo,
            pygame.K_BACKSPACE: self.delete_last_frame,
            pygame.K_RETURN: ()
        }

        frame = Files.check_frames(self.screen, config.frames.export_directory)
        print("starte mit frame " + str(frame))
        self.cam = Camera(frame)
        self.gui = GUI()
        self.running = True

    def quit(self):
        self.running = False

    def take_photo(self):
        filename = self.cam.capture_photo()

    def delete_last_frame(self):
        if (Files.delete_last_frame(config.frames.export_directory)):
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
