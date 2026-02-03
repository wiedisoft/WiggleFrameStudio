from dataclasses import dataclass
import yaml
from pathlib import Path

@dataclass
class Frames:
    export_directory: Path


@dataclass
class Movies:
    export_directory: Path

@dataclass
class AppConfig:
    frames: Frames
    movies: Movies
    debug: bool

class Config:
    _config: AppConfig | None = None

    @staticmethod
    def load(path: Path = Path("config/config.yaml")) -> None:
        if Config._config is not None:
            return

        with path.open() as f:
            raw = yaml.safe_load(f)

        Config._config = AppConfig(
            frames=Frames(Path(raw["frames"]["export_directory"])),
            movies=Movies(Path(raw["movies"]["export_directory"])),
            debug=raw.get("debug")
        )

    @staticmethod
    def get() -> AppConfig:
        if Config._config is None:
            raise RuntimeError("Config wurde noch nicht geladen")
        return Config._config