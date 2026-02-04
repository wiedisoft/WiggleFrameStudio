import pygame
import cairosvg
import io
from PIL import Image

import resources.core as core
import resources.styles as styles
from utils.logger import setup_logger

logger = setup_logger(__name__)

class SplashScreen:
    SPACING = 80
    LINE_SPACING = 8

    def __init__(self, screen):
        self.screen = screen
        self.logo_surface = self.load_svg("assets/logo.svg")

    @staticmethod
    def load_svg(path):
        try:
            png_bytes = cairosvg.svg2png(url=path)
            image = Image.open(io.BytesIO(png_bytes)).convert("RGBA")
            return pygame.image.fromstring(image.tobytes(), image.size, image.mode)
        except Exception as e:
            logger.error(f"Error loading SVG '{path}': {e}")
            return pygame.Surface((200, 200), pygame.SRCALPHA)

    @staticmethod
    def render_text_outline(font, text, text_color, outline_color, outline_width=5):
        base = font.render(text, True, text_color)
        bw, bh = base.get_size()
        pad = outline_width * 2
        surf = pygame.Surface((bw + pad*2, bh + pad*2), pygame.SRCALPHA)
        center = (pad, pad)
        for dx in range(-outline_width, outline_width + 1):
            for dy in range(-outline_width, outline_width + 1):
                if dx*dx + dy*dy <= outline_width*outline_width:
                    outline = font.render(text, True, outline_color)
                    surf.blit(outline, (center[0]+dx, center[1]+dy))
        surf.blit(base, center)
        return surf

    def show_splash(self):
        title_surface = self.render_text_outline(
            styles.FONT_LOGO, "Wiggle", styles.COLOR_HIGHLIGHT,
            (255, 255, 255), outline_width=8
        )
        subtitle_surface = styles.FONT_SUB_TITLE.render(
            "FrameStudio", True, styles.FONT_COLOR_TITLE
        )

        screen_rect = self.screen.get_rect()
        center_x, center_y = screen_rect.center

        text_block_width = max(title_surface.get_width(), subtitle_surface.get_width())
        text_block_height = title_surface.get_height() + self.LINE_SPACING + subtitle_surface.get_height()
        total_width = self.logo_surface.get_width() + self.SPACING + text_block_width

        svg_rect = self.logo_surface.get_rect()
        svg_rect.midleft = (center_x - total_width // 2, center_y)

        text_x = svg_rect.right + self.SPACING
        text_block_top = center_y - text_block_height // 2
        title_rect = title_surface.get_rect(topleft=(text_x, text_block_top))
        subtitle_rect = subtitle_surface.get_rect(midtop=(title_rect.centerx, title_rect.bottom + self.LINE_SPACING))

        self.screen.blit(self.logo_surface, svg_rect)
        self.screen.blit(title_surface, title_rect)
        self.screen.blit(subtitle_surface, subtitle_rect)
        pygame.display.flip()

    def show_dialog(self, key):
        text = styles.FONT_SMALL.render(core.translate.t(key), True, styles.FONT_COLOR_TITLE)
        rect = text.get_rect(center=(self.screen.get_width()//2, (self.screen.get_height()//4*3)))
        self.screen.blit(text, rect)

        hint = styles.FONT_TINY.render(core.translate.t("splash_screen.yes_no_quit"), True, styles.FONT_COLOR_SUB_TITLE)
        hint_rect = hint.get_rect(center=(self.screen.get_width()//2, (self.screen.get_height()//4*3)+60))
        self.screen.blit(hint, hint_rect)

        pygame.display.flip()
        return self.wait_for_interaction()

    def wait_for_interaction(self):
        keymap = core.splash_keymap()
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()
                elif event.type == pygame.KEYDOWN:
                    action = keymap.get(event.key)
                    if action:
                        return action
