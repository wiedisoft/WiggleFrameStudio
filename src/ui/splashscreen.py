import pygame

class SplashScreen():

    def show_splash(screen, image_path):
        splash = pygame.image.load(image_path)
        splash = pygame.transform.scale(splash, screen.get_size())
        screen.blit(splash, (0, 0))
        pygame.display.flip()

    def show_dialog(screen, message):
        font = pygame.font.SysFont(None, 50)
        small_font = pygame.font.SysFont(None, 30)
        text = font.render(message, True, (255, 255, 255))
        rect = text.get_rect(center=(screen.get_width()//2, screen.get_height()//4 * 3 ))
        screen.blit(text, rect)
        hint = small_font.render("Y = Ja, N = Nein", True, (200, 200, 200))
        hint_rect = hint.get_rect(center=(screen.get_width()//2, (screen.get_height()//4 * 3) + 30))
        screen.blit(hint, hint_rect)
        pygame.display.flip()
