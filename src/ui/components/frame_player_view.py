import time

import pygame

import resources.core as core
import resources.styles as styles
from ui.components.ui_component import UIComponent


class FramePlayerView(UIComponent):
    def __init__(
        self,
        scale=0.8,
        border_width=8,
        border_radius=15,
        border_color=styles.FONT_COLOR_TITLE,
        x=0,
        y=0,
        visible=True,
        centered=True,
        frame_interval=0.25,
        on_frame_change=None
    ):
        super().__init__(x=x, y=y, visible=visible, centered=centered)

        self.scale = scale
        self.border_width = border_width
        self.border_radius = border_radius
        self.border_color = border_color

        self.frame_interval = frame_interval
        self.last_frame_time = time.time()
        self.current_index = 0

        self.frames = self._load_frames()
        self.width = 0
        self.height = 0
        self.on_frame_change = on_frame_change

    @staticmethod
    def _load_frames():
        directory = core.config.frames.export_directory
        files = sorted(
            directory.glob("*.jpg"),
            key=lambda file: int(file.stem.split("_")[-1])
        )

        loaded = []
        for f in files:
            img = pygame.image.load(str(f)).convert()
            loaded.append(img)

        return loaded

    def reset(self):
        self.current_index = 0
        self.last_frame_time = time.time()

        if self.on_frame_change:
            self.on_frame_change(1, len(self.frames))

    def _advance_frame(self):
        now = time.time()
        if now - self.last_frame_time >= self.frame_interval:
            self.current_index = (self.current_index + 1) % len(self.frames)
            self.last_frame_time = now

        if self.on_frame_change: self.on_frame_change(self.current_index + 1,
                                                      len(self.frames))

    def scale_surface(self, surface, screen_size):
        sw, sh = surface.get_size()
        screen_w, screen_h = screen_size

        target_w = screen_w * self.scale
        target_h = screen_h * self.scale

        scale = min(target_w / sw, target_h / sh)
        new_size = (int(sw * scale), int(sh * scale))

        return pygame.transform.smoothscale(surface, new_size)

    def draw(self, surface):
        if not self.visible or not self.frames:
            return

        self._advance_frame()

        frame_surface = self.frames[self.current_index]

        screen_w = surface.get_width()
        screen_h = surface.get_height()

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
