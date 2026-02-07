import threading

import pygame

import media.movie as movie
import resources.core as core
import resources.styles as styles
from media.camera import Camera
from media.movie import get_movie_length
from ui.main_ui import MainGUI
from ui.splash_screen import SplashScreen
from utils.files import check_frames, count_frames, delete_last_frame
from utils.logger import setup_logger

logger = setup_logger(__name__)


class MainApp:
    def __init__(self):
        logger.info("Starting WiggleFrameStudio")

        icon = pygame.image.load("assets/icon.png")
        pygame.display.set_icon(icon)

        self.screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
        pygame.display.set_caption("WiggleFrameStudio")
        self.screen.fill(styles.BACKGROUND_COLOR)

        splash = SplashScreen(self.screen)
        splash.show_splash()

        frame = check_frames(splash, logger)
        self.cam = Camera(frame)
        self.gui = MainGUI(self.screen)
        self.running = True
        self.reset_export_ui_at = None
        self.export_thread = None
        self.keymap = core.gui_keymap(self)

    def take_photo(self):
        filename = self.cam.capture_photo()
        logger.info(f"Frame saved: {filename}")
        frames = count_frames()
        self.gui.movie_information.set_text(
            core.translate.t("main_ui.movie_information", count=frames,
                             length=get_movie_length(frames)))

    def delete_last_frame(self):
        if delete_last_frame(logger):
            self.cam.frame_number = self.cam.frame_number() - 1

    def preview_movie(self):
        self.gui.capture_mode = not self.gui.capture_mode
        frames = count_frames()
        if not self.gui.capture_mode:
            self.gui.movie_information.set_text(
                core.translate.t("main_ui.movie_preview", current=1, total=frames))
            self.gui.frame_player_view.reset()
        else:
            self.gui.movie_information.set_text(
                core.translate.t("main_ui.movie_information", count=frames,
                                 length=get_movie_length(frames)))

    def delete_project(self):
        return

    def save_movie(self):
        self.export_thread = threading.Thread(
            target=movie.export_movie,
            args=(self.gui,),
            daemon=True
        )
        self.export_thread.start()

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

            if self.export_thread is not None:
                if not self.export_thread.is_alive():
                    self.reset_export_ui_at = pygame.time.get_ticks() + 5000
                    self.export_thread = None

            now = pygame.time.get_ticks()
            if self.reset_export_ui_at is not None and now >= self.reset_export_ui_at:
                self.gui.set_export_progress(None)
                self.gui.set_status_text("")
                self.reset_export_ui_at = None

        self.quit()

    def quit(self):
        self.cam.stop()
        self.running = False
        pygame.quit()
        exit()
