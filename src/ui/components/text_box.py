import pygame
from ui.components.ui_component import UIComponent

class TextBox(UIComponent):
    def __init__(
            self,
            text,
            font,
            color,
            x=0,
            y=0,
            visible=True,
            outline_color=None,
            outline_width=0,
            padding=0,
            centered=True
    ):
        super().__init__(x=x, y=y, visible=visible, centered=centered)

        self.text = text
        self.font = font
        self.color = color
        self.outline_color = outline_color
        self.outline_width = outline_width
        self.padding = padding

        self.rendered = None
        self.width = 0
        self.height = 0

        self.update_surface()

    def update_surface(self):
        base = self.font.render(self.text, True, self.color)

        if not self.outline_color or self.outline_width <= 0:
            self.rendered = base
            self.width, self.height = base.get_size()
            return

        bw, bh = base.get_size()
        pad = self.outline_width * 2 + self.padding * 2

        surf = pygame.Surface((bw + pad, bh + pad), pygame.SRCALPHA)

        cx = pad // 2
        cy = pad // 2

        for dx in range(-self.outline_width, self.outline_width + 1):
            for dy in range(-self.outline_width, self.outline_width + 1):
                if dx * dx + dy * dy <= self.outline_width * self.outline_width:
                    outline = self.font.render(self.text, True, self.outline_color)
                    surf.blit(outline, (cx + dx, cy + dy))

        surf.blit(base, (cx, cy))

        self.rendered = surf
        self.width, self.height = surf.get_size()

    def set_text(self, new_text):
        self.text = new_text
        self.update_surface()

    def draw(self, surface):
        if not self.visible:
            return

        screen_w = surface.get_width()
        screen_h = surface.get_height()
        x, y = self.get_draw_position(screen_w, screen_h)
        surface.blit(self.rendered, (x, y))
