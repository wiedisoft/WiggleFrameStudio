import logging

class ColorFormatter(logging.Formatter):
    COLORS = {
        "DEBUG": "\033[37m",
        "INFO": "\033[32m",
        "WARNING": "\033[33m",
        "ERROR": "\033[31m",
        "CRITICAL": "\033[41m",
    }
    RESET = "\033[0m"
    BOLD = "\033[1m"
    NAME_COLOR = "\033[37m"

    def format(self, record):
        message = super().format(record)

        levelname_colored = f"{self.BOLD}{self.COLORS.get(record.levelname, self.RESET)}{record.levelname}{self.RESET}"
        message = message.replace(record.levelname, levelname_colored)

        name_colored = f"{self.BOLD}{self.NAME_COLOR}{record.name}{self.RESET}"
        message = message.replace(record.name, name_colored)

        return message


def setup_logger(name="WiggleFrameStudio", level=logging.INFO):
    logger = logging.getLogger(name)
    logger.setLevel(level)

    if not logger.handlers:
        formatter = ColorFormatter(
            "%(asctime)s %(levelname)s %(name)s %(message)s"
        )

        handler = logging.StreamHandler()
        handler.setFormatter(formatter)
        logger.addHandler(handler)

    return logger
