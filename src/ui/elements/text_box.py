class TextBox:
    def __init__(self, text, font, color, x, y, parent=None):
        self.text = text
        self.font = font
        self.color = color
        self.x = x
        self.y = y
        self.parent = parent
        self.rendered = None
        self.update_surface()

    def update_surface(self):
        self.rendered = self.font.render(self.text, True, self.color)

    def set_text(self, new_text):
        self.text = new_text
        self.update_surface()

    def draw(self, surface):
        # Parent-Container bestimmen
        if self.parent:
            px, py, pw, ph = self.parent.get_rect()
        else:
            px, py = 0, 0
            pw, ph = surface.get_width(), surface.get_height()

        tw = self.rendered.get_width()
        th = self.rendered.get_height()

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
            x = px + (pw - tw) // 2 + offset
        elif mode == "right":
            x = px + pw - tw + offset
        elif isinstance(mode, float):  # relative + offset
            x = px + int(pw * mode) + offset
        else:  # absolute
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
            y = py + (ph - th) // 2 + offset
        elif mode == "bottom":
            y = py + ph - th + offset
        elif isinstance(mode, float):  # relative + offset
            y = py + int(ph * mode) + offset
        else:  # absolute
            y = py + int(mode)

        surface.blit(self.rendered, (x, y))
