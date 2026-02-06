from picamera2 import Picamera2
import resources.core as core

class Camera:
    def __init__(self, start_frame=0, size=(1920, 1080)):
        self.picam2 = Picamera2()
        self.size = size
        self.frame_number = start_frame
        self._configure_camera()

    def _configure_camera(self):
        config = self.picam2.create_preview_configuration(
            main={"format": "RGB888", "size": self.size},
            buffer_count=2
        )
        self.picam2.configure(config)
        self.picam2.start()

    def get_frame(self):
        return self.picam2.capture_array("main")

    def capture_photo(self):
        self.frame_number += 1
        filename = f"{core.config.frames.export_directory}/frame_{self.frame_number:04d}.jpg"
        self.picam2.capture_file(filename, format="jpeg")
        return filename

    def stop(self):
        self.picam2.stop()
