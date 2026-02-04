import pygame
import cairosvg
import io
from PIL import Image

import resources.core as core
import resources.styles as styles
from utils.logger import setup_logger

logger = setup_logger(__name__)

class Splash_Screen():

    def show_splash(screen):
        png_bytes = cairosvg.svg2png(url="assets/logo.svg")
        image = Image.open(io.BytesIO(png_bytes)).convert("RGBA")
        mode = image.mode
        size = image.size
        data = image.tobytes()

        svg_surface = pygame.image.fromstring(data, size, mode)
        title_surface = Splash_Screen().render_text_outline(
            styles.FONT_LOGO,
            "Wiggle",
            styles.COLOR_HIGHLIGHT,
            (255, 255, 255),
            outline_width=8
        )

        subtitle_surface = styles.FONT_SUB_TITLE.render(
            "FrameStudio", True, styles.FONT_COLOR_TITLE
        )

        spacing = 80
        line_spacing = 8

        screen_rect = screen.get_rect()
        center_x = screen_rect.centerx
        center_y = screen_rect.centery

        text_block_width = max(
            title_surface.get_width(),
            subtitle_surface.get_width()
        )
        text_block_height = (
            title_surface.get_height()
            + line_spacing
            + subtitle_surface.get_height()
        )

        total_width = (
            svg_surface.get_width()
            + spacing
            + text_block_width
        )

        svg_rect = svg_surface.get_rect()
        svg_rect.midleft = (
            center_x - total_width // 2,
            center_y
        )

        text_block_top = center_y - text_block_height // 2
        text_x = svg_rect.right + spacing

        title_rect = title_surface.get_rect(
            topleft=(text_x, text_block_top)
        )

        subtitle_rect = subtitle_surface.get_rect()
        subtitle_rect.midtop = (
            title_rect.centerx,
            title_rect.bottom + line_spacing
        )

        screen.blit(svg_surface, svg_rect)
        screen.blit(title_surface, title_rect)
        screen.blit(subtitle_surface, subtitle_rect)
        pygame.display.flip()


    @staticmethod
    def show_dialog(screen, key):
        text = styles.FONT_SMALL.render(core.translate.t(key), True, styles.FONT_COLOR_TITLE)
        rect = text.get_rect(center=(screen.get_width()//2, (screen.get_height()//4 * 3 ) - 30))
        screen.blit(text, rect)

        hint = styles.FONT_TINY.render(core.translate.t("splash_screen.yes_no_quit"), True, styles.FONT_COLOR_SUB_TITLE)
        hint_rect = hint.get_rect(center=(screen.get_width()//2, (screen.get_height()//4 * 3) + 30))
        screen.blit(hint, hint_rect)

        pygame.display.flip()
        return Splash_Screen().wait_for_interaction()
    
    @staticmethod
    def wait_for_interaction():
        keymap = core.splash_keymap()

        waiting = True
        while waiting:
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    action = keymap.get(event.key)
                    if action:
                        return action

    @staticmethod
    def render_text_outline(font, text, text_color, outline_color, outline_width=5):
        base = font.render(text, True, text_color)
        bw, bh = base.get_size()

        pad = outline_width * 2

        surf = pygame.Surface(
            (bw + pad * 2, bh + pad * 2),
            pygame.SRCALPHA
        )

        center = (pad, pad)
        for dx in range(-outline_width, outline_width + 1):
            for dy in range(-outline_width, outline_width + 1):
                if dx * dx + dy * dy <= outline_width * outline_width:
                    outline = font.render(text, True, outline_color)
                    surf.blit(outline, (center[0] + dx, center[1] + dy))
        surf.blit(base, center)
        return surf