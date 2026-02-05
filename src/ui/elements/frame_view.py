import pygame
import numpy as np
import resources.styles as styles

class FrameView:
    def __init__(self, scale=0.8, border_width=8, border_radius=15,
                 border_color=styles.FONT_COLOR_TITLE):
        self.scale = scale
        self.border_width = border_width
        self.border_radius = border_radius
        self.border_color = border_color

    def get_rect(self): 
        return (self.x, self.y, self.width, self.height)

    def numpy_to_surface(self, frame):
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

    def draw(self, screen, frame):
        surface = self.numpy_to_surface(frame)
        surface = self.scale_surface(surface, screen.get_size())

        frame_surf = pygame.Surface(
            (surface.get_width() + self.border_width*2,
            surface.get_height() + self.border_width*2),
            pygame.SRCALPHA
        )

        frame_surf.blit(surface, (self.border_width, self.border_width))

        rect = frame_surf.get_rect()
        pygame.draw.rect(
            frame_surf,
            self.border_color,
            rect,
            self.border_width,
            self.border_radius
        )

        x = (screen.get_width() - frame_surf.get_width()) // 2
        y = (screen.get_height() - frame_surf.get_height()) // 2

        self.x = x
        self.y = y
        self.width = frame_surf.get_width()
        self.height = frame_surf.get_height()

        screen.blit(frame_surf, (x, y))


        frame_surf.blit(surface, (self.border_width, self.border_width))

        rect = frame_surf.get_rect()
        pygame.draw.rect(
            frame_surf,
            self.border_color,
            rect,
            self.border_width,
            self.border_radius
        )

        x = (screen.get_width() - frame_surf.get_width()) // 2
        y = (screen.get_height() - frame_surf.get_height()) // 2

        screen.blit(frame_surf, (x, y))
