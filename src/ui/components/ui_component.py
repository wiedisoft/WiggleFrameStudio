class UIComponent:
    def __init__(self, x=0, y=0, centered=False, visible=True):
        self.x = x
        self.y = y
        self.centered = centered
        self.visible = visible

        self.width = 0
        self.height = 0

    def get_rect(self):
        return self.x, self.y, self.width, self.height

    @staticmethod
    def resolve_value(value, total):
        if isinstance(value, float):
            return int(total * value)
        return int(value)

    def compute_position(self, screen_w, screen_h):
        px = self.resolve_value(self.x, screen_w)
        py = self.resolve_value(self.y, screen_h)

        if self.centered:
            px -= self.width // 2
            py -= self.height // 2

        return px, py

    def get_draw_position(self, screen_w, screen_h):
        if hasattr(self, "draw_x") and hasattr(self, "draw_y"):
            return self.draw_x, self.draw_y

        return self.compute_position(screen_w, screen_h)
