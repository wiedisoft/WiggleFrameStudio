import pygame
import cairosvg
import io
from PIL import Image
import resources.core as core
import resources.styles as styles
from ui.components.image_component import ImageComponent
from ui.components.text_box import TextBox
from utils.logger import setup_logger

logger = setup_logger(__name__)

class SplashScreen:
    SPACING = 0.05
    LINE_SPACING = 0.01

    def __init__(self, screen):
        self.screen = screen
        self.logo_surface = self.load_svg("assets/logo.svg")

        self.logo = ImageComponent(
            self.logo_surface,
            x=0.35,
            y=0.5,
            centered=True
        )

        self.title = TextBox(
            "Wiggle",
            styles.FONT_LOGO,
            styles.COLOR_HIGHLIGHT,
            x=0.65,
            y=0.44,
            centered=True,
            outline_color=styles.FONT_COLOR_TITLE,
            outline_width=8
        )

        self.subtitle = TextBox(
            "FrameStudio",
            styles.FONT_SUB_TITLE,
            styles.FONT_COLOR_TITLE,
            x=0.65,
            y=0.57,
            centered=True
        )

    @staticmethod
    def load_svg(path):
        try:
            png_bytes = cairosvg.svg2png(url=path)
            image = Image.open(io.BytesIO(png_bytes)).convert("RGBA")
            return pygame.image.fromstring(image.tobytes(), image.size, image.mode)
        except Exception as e:
            logger.error(f"Error loading SVG '{path}': {e}")
            return pygame.Surface((200, 200), pygame.SRCALPHA)

    def show_splash(self):
        self.screen.fill(styles.BACKGROUND_COLOR)

        self.logo.draw(self.screen)
        self.title.draw(self.screen)
        self.subtitle.draw(self.screen)

        pygame.display.flip()

    def show_dialog(self, key):
        text = TextBox(
            core.translate.t(key),
            styles.FONT_SMALL,
            styles.FONT_COLOR_TITLE,
            x=0.5,
            y=0.75,
            centered=True
        )

        hint = TextBox(
            core.translate.t("splash_screen.yes_no_quit"),
            styles.FONT_TINY,
            styles.FONT_COLOR_SUB_TITLE,
            x=0.5,
            y=0.80,
            centered=True
        )

        text.draw(self.screen)
        hint.draw(self.screen)
        pygame.display.flip()

        return self.wait_for_interaction()

    @staticmethod
    def wait_for_interaction():
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
