import pygame
from queue import Queue
import resources.styles as styles
from media.movie import get_movie_length
from ui.components.frame_view import FrameView
from ui.components.progress_bar import ProgressBar
from ui.components.text_box import TextBox
import resources.core as core
from utils.files import count_frames


class MainGUI:
    def __init__(self, screen):
        self.gui_updates = Queue()
        self.frame = None
        self.screen = screen
        self.export_progress = None
        self.clock = pygame.time.Clock()

        self.frame_view = FrameView(x=0.5, y=0.5, centered=True)

        frames = count_frames()
        self.movie_information = TextBox(
            core.translate.t("main_ui.movie_information", count=frames,
                             length=get_movie_length(frames)),
                             styles.FONT_TINY,
                             styles.FONT_COLOR_TITLE,
                             x=0.1,
                             y=0.11,
                             centered=False)

        self.title = TextBox(
            "WiggleFrameStudio",
            styles.FONT_SUB_TITLE,
            styles.COLOR_HIGHLIGHT,
            x=0.5,
            y=0.05,
            outline_color=styles.FONT_COLOR_TITLE,
            outline_width=8,
            centered=True)

        self.progress_bar = ProgressBar(
            width=0.4,
            height=0.04,
            x=0.5,
            y=0.9,
            fill_color=styles.COLOR_HIGHLIGHT,
            bg_color=styles.BACKGROUND_COLOR,
            border_width=8,
            centered=True
        )

        self.status_text = TextBox(
            "status",
            styles.FONT_REGULAR,
            styles.FONT_COLOR_TITLE,
            x=0.5,
            y=0.9,
            centered=True
        )

    def display_frame(self, frame, fps=30):
        self.frame = frame
        self.screen.fill(styles.BACKGROUND_COLOR)

        self.frame_view.set_frame(frame)
        self.frame_view.draw(self.screen)
        self.movie_information.draw(self.screen)
        self.title.draw(self.screen)
        if self.progress_bar.progress is not None:
            self.progress_bar.draw(self.screen)
            self.status_text.draw(self.screen)

        while not self.gui_updates.empty():
            key, value = self.gui_updates.get()
            if key == "status":
                self.status_text.set_text(value)

        pygame.display.flip()
        self.tick(fps)

    def tick(self, fps=30):
        self.clock.tick(fps)

    def set_status_text(self, text):
        self.gui_updates.put(("status", text))

    def set_export_progress(self, value):
        self.progress_bar.set_progress(value)
