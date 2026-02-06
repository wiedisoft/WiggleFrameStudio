import yaml
from pathlib import Path
from typing import Any
from utils.logger import setup_logger

logger = setup_logger(__name__)

class Translate:
    def __init__(
        self,
        path: Path = Path("config/translations.yaml"),
        language: str = "de",
        fallback: str = "en",
    ):
        logger.info(f"loading translation - using language: {language}")

        if not path.exists():
            logger.error(f"translation file not found: {path}")
            raise FileNotFoundError(f"translation file not found: {path}")

        with open(path, encoding="utf-8") as f:
            self.translations = yaml.safe_load(f) or {}

        self.language = language
        self.fallback = fallback

    def set_language(self, lang: str) -> None:
        self.language = lang

    def t(self, key: str, **kwargs: Any) -> str:
        value = (
            self._get(self.language, key)
            or self._get(self.fallback, key)
        )

        if value is None:
            return key

        if kwargs:
            try:
                value = value.format(**kwargs)
            except KeyError:
                pass

        return value

    def _get(self, lang: str, key: str):
        keys = key.split(".")
        value = self.translations.get(lang, {})
        for k in keys:
            if not isinstance(value, dict):
                return None
            value = value.get(k)
        return value