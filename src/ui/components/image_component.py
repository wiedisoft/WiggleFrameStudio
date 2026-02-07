from ui.components.ui_component import UIComponent


class ImageComponent(UIComponent):
    def __init__(self, image_surface, x=0, y=0, centered=False, visible=True):
        super().__init__(x=x, y=y, centered=centered, visible=visible)
        self.image = image_surface
        self.width = image_surface.get_width()
        self.height = image_surface.get_height()

    def draw(self, surface):
        if not self.visible:
            return

        screen_w = surface.get_width()
        screen_h = surface.get_height()
        x, y = self.get_draw_position(screen_w, screen_h)

        surface.blit(self.image, (x, y))
