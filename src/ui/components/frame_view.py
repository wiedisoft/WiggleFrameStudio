import pygame
import numpy as np
from ui.components.ui_component import UIComponent
import resources.styles as styles

class FrameView(UIComponent):
    def __init__(
        self,
        scale=0.8,
        border_width=8,
        border_radius=15,
        border_color=styles.FONT_COLOR_TITLE,
        x=0,
        y=0,
        visible=True,
        centered=True
    ):
        super().__init__(x=x, y=y, visible=visible, centered=centered)

        self.scale = scale
        self.border_width = border_width
        self.border_radius = border_radius
        self.border_color = border_color

        self.frame = None
        self.width = 0
        self.height = 0
        self._cached_surface = None

    def set_frame(self, frame):
        self.frame = frame

    @staticmethod
    def numpy_to_surface(frame):
        frame_corrected = frame[:, :, ::-1]
        return pygame.surfarray.make_surface(np.rot90(frame_corrected))

    def scale_surface(self, surface, screen_size):
        sw, sh = surface.get_size()
        screen_w, screen_h = screen_size

        target_w = screen_w * self.scale
        target_h = screen_h * self.scale

        scale = min(target_w / sw, target_h / sh)
        new_size = (int(sw * scale), int(sh * scale))

        return pygame.transform.smoothscale(surface, new_size)

    def get_rect(self):
        return self.x, self.y, self.width, self.height

    def draw(self, surface):
        if not self.visible or self.frame is None:
            return

        screen_w = surface.get_width()
        screen_h = surface.get_height()

        frame_surface = self.numpy_to_surface(self.frame)
        frame_surface = self.scale_surface(frame_surface, (screen_w, screen_h))

        self.width = frame_surface.get_width() + self.border_width * 2
        self.height = frame_surface.get_height() + self.border_width * 2
        x, y = self.get_draw_position(screen_w, screen_h)

        frame_surf = pygame.Surface((self.width, self.height), pygame.SRCALPHA)
        frame_surf.blit(frame_surface, (self.border_width, self.border_width))

        pygame.draw.rect(
            frame_surf,
            self.border_color,
            frame_surf.get_rect(),
            width=self.border_width,
            border_radius=self.border_radius
        )

        surface.blit(frame_surf, (x, y))
