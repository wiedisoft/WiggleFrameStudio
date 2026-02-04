import re

import resources.core as core

from ui.splash_screen import SplashScreen
from utils.logger import setup_logger

logger = setup_logger(__name__)

class Files():

    @staticmethod
    def check_frames(splash: SplashScreen):
        directory = core.config.frames.export_directory
        directory.mkdir(parents=True, exist_ok=True)
        if any(directory.iterdir()):
            logger.info("Frames directory is not empty")
            match(splash.show_dialog("splash_screen.frames_exists")):
                case "quit":
                    logger.info("User chose to quit")
                    exit()
                case "backspace":
                    logger.info("User chose to start a new movie; deleting existing frames")
                    return Files.delete_files()
                case "return":
                    logger.info("User chose to resume last movie; keeping existing frames")
                    return Files.get_last_frame_number()
        return 0

    @staticmethod
    def delete_files():
        directory = core.config.frames.export_directory
        if directory.exists() and directory.is_dir():
            for file in directory.iterdir():
                if file.is_file():
                    file.unlink()
                    logger.info(f"Deleted file: {file}")
                elif file.is_dir():
                    logger.warning(f"Skipped folder: {file}")
        return 0

    @staticmethod
    def delete_last_frame():
        directory = core.config.frames.export_directory
        try:
            files = [f for f in directory.iterdir() if f.is_file()]
            if not files:
                return False 
            files = sorted(files)
            last_file = files[-1]
            last_file.unlink()
            return True

        except OSError as e:
            logger.error(f"Failed to delete last frame: {e}")
            return False
        
    @staticmethod
    def get_last_frame_number():
        directory = core.config.frames.export_directory
        if not directory.exists():
            logger.info("Frames directory is empty, no action needed")
            return 0

        max_frame = 0
        pattern = re.compile(r"frame_(\d+)\.png")
        for file in directory.iterdir():
            match = pattern.match(file.name)
            if match:
                num = int(match.group(1))
                if num > max_frame:
                    max_frame = num
        logger.info(f"Found {max_frame} as the highest frame number in {directory}")
        return max_frame