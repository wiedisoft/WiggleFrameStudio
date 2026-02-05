import pygame
from queue import Queue

import resources.styles as styles
from ui.elements.frame_view import FrameView
from ui.elements.progress_bar import ProgressBar 
from ui.elements.text_box import TextBox

class MainGUI:
    def __init__(self, screen):
        self.gui_updates = Queue()
        self.screen = screen
        self.export_progress = None
        self.clock = pygame.time.Clock()
        self.frame_view = FrameView()
        
        self.movie_information = TextBox("Information", styles.FONT_REGULAR, styles.FONT_COLOR_TITLE, "left", ("top", - 50), parent=self.frame_view)
        self.progress_bar = ProgressBar(width=800, height=50, border_width=8, border_color=styles.FONT_COLOR_TITLE, bg_color=styles.BACKGROUND_COLOR, fill_color=styles.COLOR_HIGHLIGHT, x="center", y=("bottom", + 80), parent=self.frame_view) 
        self.status_text = TextBox("", styles.FONT_REGULAR, styles.FONT_COLOR_TITLE, "center", "middle", parent=self.progress_bar)
        
    def display_frame(self, frame, fps=30):
        self.frame = frame
        self.screen.fill(styles.BACKGROUND_COLOR)
        self.frame_view.draw(self.screen, frame)
        
        self.movie_information.draw(self.screen)
        if self.progress_bar.progress is not None:
            x = (self.screen.get_width() - self.progress_bar.width) // 2
            y = self.screen.get_height() - 60
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

