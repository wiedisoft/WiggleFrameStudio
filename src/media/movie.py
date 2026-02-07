import math
from datetime import datetime

from moviepy import ImageSequenceClip

import resources.core as core
from ui.components.progress_logger import ProgressLogger
from utils.logger import setup_logger

logger = setup_logger(__name__)


def get_movie_length(frames):
    return math.ceil(frames / core.config.movies.frames_per_second)


def export_movie(gui):
    gui.set_status_text(core.translate.t("main_ui.export_movie"))
    gui.set_export_progress(0.0)

    def update_progress(value):
        gui.set_export_progress(value)

    progress_logger = ProgressLogger(update_progress)

    gui.set_status_text(core.translate.t("main_ui.read_frames"))
    directory = core.config.movies.export_directory
    directory.mkdir(exist_ok=True)

    frames = sorted(
        core.config.frames.export_directory.glob("*.jpg"),
        key=lambda f: int(f.stem.split("_")[-1])
    )

    if not frames:
        gui.set_status_text(core.translate.t("main_ui.no_frames"))
        logger.warning(f"No frames found in: {core.config.frames.export_directory}")
        return

    gui.set_status_text(core.translate.t("main_ui.prepare_movie"))
    clip = ImageSequenceClip(
        list(map(str, frames)),
        fps=core.config.movies.frames_per_second,
        load_images=False
    )

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    output_video = directory / f"{core.config.movies.filename}_{timestamp}.mp4"

    gui.set_status_text(core.translate.t("main_ui.save_movie"))
    clip.write_videofile(str(output_video), codec="libx264",
                         fps=core.config.movies.frames_per_second,
                         logger=progress_logger, audio=False, preset="ultrafast",
                         ffmpeg_params=["-pix_fmt", "yuv420p", "-crf", "23", "-threads",
                                        "4"])
    logger.info(f"Video successfully exported: {output_video}")
    gui.set_status_text(core.translate.t("main_ui.successfully_saved"))
