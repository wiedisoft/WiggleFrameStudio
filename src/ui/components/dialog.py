from ui.components.ui_component import UIComponent


class Dialog(UIComponent):
    def __init__(self, elements, spacing=10, x=0, y=0, visible=True, centered=True):
        super().__init__(x=x, y=y, visible=visible, centered=centered)
        self.elements = elements
        self.spacing = spacing
        self.width = 0
        self.height = 0

    def draw(self, surface):
        if not self.visible:
            return

        screen_w = surface.get_width()
        screen_h = surface.get_height()

        total_height = sum(e.height for e in self.elements)
        total_height += self.spacing * (len(self.elements) - 1)
        max_width = max(e.width for e in self.elements)

        self.width = max_width
        self.height = total_height

        x, y = self.compute_position(screen_w, screen_h)

        current_y = y
        for element in self.elements:
            element.draw_x = x + (self.width - element.width) // 2
            element.draw_y = current_y

            element.draw(surface)

            current_y += element.height + self.spacing
