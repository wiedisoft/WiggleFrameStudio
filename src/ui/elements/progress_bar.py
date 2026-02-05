import pygame

class ProgressBar:
    def __init__(
        self,
        width=400,
        height=30,
        border_radius=15,
        border_width=4,
        border_color=(255, 255, 255),
        bg_color=(80, 80, 80),
        fill_color=(0, 200, 0),
        x="center",
        y="bottom",
        parent=None
    ):
        self.width = width
        self.height = height
        self.border_radius = border_radius
        self.border_width = border_width
        self.border_color = border_color
        self.bg_color = bg_color
        self.fill_color = fill_color
        self.progress = None
        self.x = x
        self.y = y
        self.last_x = 0
        self.last_y = 0
        self.parent = parent

    def get_rect(self): 
        return (self.last_x, self.last_y, self.width, self.height)

    def set_progress(self, value):
        if value is None:
            self.progress = None
        else:
            self.progress = max(0.0, min(1.0, value))


    def draw(self, surface):
        if self.progress is None: 
            return
        
        if self.parent:
            px, py, pw, ph = self.parent.get_rect()
        else:
            px, py = 0, 0
            pw, ph = surface.get_width(), surface.get_height()

        # -------------------------
        # X POSITION
        # -------------------------
        if isinstance(self.x, tuple):
            mode, offset = self.x
        else:
            mode, offset = self.x, 0

        if mode == "left":
            x = px + offset
        elif mode == "center":
            x = px + (pw - self.width) // 2 + offset
        elif mode == "right":
            x = px + pw - self.width + offset
        elif isinstance(mode, float):
            x = px + int(pw * mode) + offset
        else:
            x = px + int(mode)

        # -------------------------
        # Y POSITION
        # -------------------------
        if isinstance(self.y, tuple):
            mode, offset = self.y
        else:
            mode, offset = self.y, 0

        if mode == "top":
            y = py + offset
        elif mode == "middle":
            y = py + (ph - self.height) // 2 + offset
        elif mode == "bottom":
            y = py + ph - self.height + offset
        elif isinstance(mode, float):
            y = py + int(ph * mode) + offset
        else:
            y = py + int(mode)

        # -------------------------
        # BORDER
        # -------------------------
        pygame.draw.rect(
            surface,
            self.border_color,
            (x, y, self.width, self.height),
            border_radius=self.border_radius,
            width=self.border_width
        )

        inner_x = x + self.border_width
        inner_y = y + self.border_width
        inner_w = self.width - self.border_width * 2
        inner_h = self.height - self.border_width * 2

        self.last_x = x 
        self.last_y = y

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
