import os
import re
import pygame
from ui.splashscreen import SplashScreen

class Files():

    def check_frames(screen, frames_directory):
        os.makedirs(frames_directory, exist_ok=True)
        if os.listdir(frames_directory):
            SplashScreen.show_dialog(screen, "Frames-Ordner ist nicht leer. Weitermachen?")

            keymap = {
                pygame.K_q: lambda: exit(),
                pygame.K_BACKSPACE: lambda: Files.delete_files(frames_directory),
                pygame.K_RETURN: lambda: Files.get_last_frame_number(frames_directory)
            }

            waiting = True
            while waiting:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        pygame.quit()
                        exit()
                    elif event.type == pygame.KEYDOWN:
                        action = keymap.get(event.key)
                        if callable(action):
                            return action()

    def delete_files(path):
        if os.path.exists(path) and os.path.isdir(path):
            for file in os.listdir(path):
                filepath = os.path.join(path, file)
                if os.path.isfile(filepath):
                    os.remove(filepath)
                    print(f"{filepath} gelöscht.")
                elif os.path.isdir(filepath):
                    print(f"{filepath} ist ein Unterordner und wird übersprungen.")                    
        return 0

    def delete_last_frame(path):
        try:
            files = os.listdir(path)
            files = sorted(files)
            last_file = files[-1]
            file_path = os.path.join(path, last_file)
            os.remove(file_path)
            return True
        except OSError:
            return False

    def get_last_frame_number(frames_directory):
        if not os.path.exists(frames_directory):
            return 0

        max_frame = 0
        pattern = re.compile(r"frame_(\d+)\.png")
        for file in os.listdir(frames_directory):
            match = pattern.match(file)
            if match:
                num = int(match.group(1))
                if num > max_frame:
                    max_frame = num

        return max_frame