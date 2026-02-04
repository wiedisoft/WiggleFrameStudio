import pygame
import numpy as np

class GUI:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
        pygame.display.set_caption("Wiggle Frame Studio")
        self.clock = pygame.time.Clock()

    def scale_to_80_percent(self, surface, screen_size):
        sw, sh = surface.get_size()
        screen_w, screen_h = screen_size
        target_w = screen_w * 0.8
        target_h = screen_h * 0.8
        scale = min(target_w / sw, target_h / sh)
        new_size = (int(sw * scale), int(sh * scale))
        return pygame.transform.smoothscale(surface, new_size)  

    def display_frame(self, frame):
        frame_corrected = frame[:, :, ::-1]
        surface = pygame.surfarray.make_surface(np.rot90(frame_corrected))
        surface = self.scale_to_80_percent(surface, self.screen.get_size())
        x = (self.screen.get_width() - surface.get_width()) // 2
        y = (self.screen.get_height() - surface.get_height()) // 2
        self.screen.fill((0, 0, 0))
        self.screen.blit(surface, (x, y))
        pygame.display.flip()

    def tick(self, fps=30):
        self.clock.tick(fps)

    def quit(self):
        pygame.quit()

