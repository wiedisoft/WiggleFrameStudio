import yaml

from pathlib import Path
from dataclasses import dataclass

from utils.logger import setup_logger

logger = setup_logger(__name__)

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
    language: str
    debug: bool

class Config:
    _config: AppConfig | None = None

    @staticmethod
    def load(path: Path = Path("config/config.yaml")) -> None:
        logger.info("loading configuration")
        if Config._config is not None:
            return

        if not path.exists():
            logger.error(f"configuration file not found: {path}")
            raise FileNotFoundError(f"configuration file not found: {path}")

        with path.open(encoding="utf-8") as f:
            raw = yaml.safe_load(f) or {}

        frames_raw = Config.require(raw, "frames")
        movies_raw = Config.require(raw, "movies")

        Config._config = AppConfig(
            frames=Frames(
                Path(Config.require(frames_raw, "export_directory"))
            ),
            movies=Movies(
                Path(Config.require(movies_raw, "export_directory"))
            ),
            language=raw.get("language", "en"),
            debug=raw.get("debug", False),
        )
    
    @staticmethod
    def require(raw: dict, key: str):
        if key not in raw:
            logger.error(f"missing configuration key: '{key}'")
            raise KeyError(f"missing configuration key: '{key}'")
        return raw[key]

    @staticmethod
    def get() -> AppConfig:
        if Config._config is None:
            logger.error("configuration not loaded")
            raise RuntimeError("configuration not loaded")
        return Config._config