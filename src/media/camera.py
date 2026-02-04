from picamera2 import Picamera2
import resources.core as core

class Camera:
    def __init__(self, start_frame=0, preview_size=(1920, 1080), photo_size=(3280, 2464)):
        self.picam2 = Picamera2()
        self.preview_size = preview_size
        self.photo_size = photo_size
        self.frame_number = start_frame
        self._configure_preview()

    def get_frame_number(self):
        return self.frame_number

    def set_frame_number(self, value):
        if (value > -1):
            self.frame_number = value

    def _configure_preview(self):
        preview_config = self.picam2.create_preview_configuration(
            main={"format": "RGB888", "size": self.preview_size}
        )
        self.picam2.configure(preview_config)
        self.picam2.start()

    def get_frame(self):
        return self.picam2.capture_array()

    def capture_photo(self):
        self.frame_number += 1
        capture_config = self.picam2.create_still_configuration(
            main={"format": "RGB888", "size": self.photo_size}
        )
        filename = f"{core.config.frames.export_directory}/frame_{self.frame_number:04d}.png"
        self.picam2.switch_mode_and_capture_file(capture_config, filename)
        return filename

    def stop(self):
        self.picam2.stop()
