import pygame
import numpy as np

import resources.styles as styles

class MainGUI:
    def __init__(self, screen):
        self.screen = screen
        self.clock = pygame.time.Clock()

    def scale_to_80_percent(self, surface, screen_size):
        sw, sh = surface.get_size()
        screen_w, screen_h = screen_size
        target_w = screen_w * 0.8
        target_h = screen_h * 0.8
        scale = min(target_w / sw, target_h / sh)
        new_size = (int(sw * scale), int(sh * scale))
        return pygame.transform.smoothscale(surface, new_size)  

    def display_frame(self, frame, fps=30):
        frame_corrected = frame[:, :, ::-1]
        surface = pygame.surfarray.make_surface(np.rot90(frame_corrected))
        surface = self.scale_to_80_percent(surface, self.screen.get_size())

        border_width = 8
        border_radius = 15

        frame_surf = pygame.Surface(
            (surface.get_width() + border_width*2, surface.get_height() + border_width*2),
            pygame.SRCALPHA
        )

        frame_surf.blit(surface, (border_width, border_width))
        rect = pygame.Rect(0, 0, frame_surf.get_width(), frame_surf.get_height())
        pygame.draw.rect(frame_surf, styles.FONT_COLOR_TITLE, rect, border_width, border_radius)
        x = (self.screen.get_width() - frame_surf.get_width()) // 2
        y = (self.screen.get_height() - frame_surf.get_height()) // 2

        self.screen.blit(frame_surf, (x, y))
        pygame.display.flip()
        self.tick(fps)

    def tick(self, fps=30):
        self.clock.tick(fps)
