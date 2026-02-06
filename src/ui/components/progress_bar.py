import pygame
from ui.components.ui_component import UIComponent

class ProgressBar(UIComponent):
    def __init__(
            self,
            width=400,
            height=30,
            border_radius=15,
            border_width=4,
            border_color=(255, 255, 255),
            bg_color=(80, 80, 80),
            fill_color=(0, 200, 0),
            x=0,
            y=0,
            visible=True,
            centered=True
    ):
        super().__init__(x=x, y=y, visible=visible, centered=centered)

        self.width = width
        self.height = height
        self.border_radius = border_radius
        self.border_width = border_width
        self.border_color = border_color
        self.bg_color = bg_color
        self.fill_color = fill_color

        self.progress = None

    def set_progress(self, value):
        if value is None:
            self.progress = None
        else:
            self.progress = max(0.0, min(1.0, value))

    def draw(self, surface):
        if not self.visible or self.progress is None:
            return

        screen_w = surface.get_width()
        screen_h = surface.get_height()

        w = self.resolve_value(self.width, screen_w)
        h = self.resolve_value(self.height, screen_h)

        x, y = self.get_draw_position(screen_w, screen_h)

        if not hasattr(self, "draw_x"):
            old_w, old_h = self.width, self.height
            self.width, self.height = w, h
            x, y = self.compute_position(screen_w, screen_h)
            self.width, self.height = old_w, old_h

        pygame.draw.rect(
            surface,
            self.border_color,
            (x, y, w, h),
            border_radius=self.border_radius,
            width=self.border_width
        )

        inner_x = x + self.border_width
        inner_y = y + self.border_width
        inner_w = w - self.border_width * 2
        inner_h = h - self.border_width * 2

        pygame.draw.rect(
            surface,
            self.bg_color,
            (inner_x, inner_y, inner_w, inner_h),
            border_radius=max(0, self.border_radius - self.border_width)
        )

        fill_width = int(inner_w * self.progress)
        pygame.draw.rect(
            surface,
            self.fill_color,
            (inner_x, inner_y, fill_width, inner_h),
            border_radius=max(0, self.border_radius - self.border_width)
        )
