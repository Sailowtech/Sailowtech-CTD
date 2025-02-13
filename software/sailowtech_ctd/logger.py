import logging
import sys


class ColoredFormatter(logging.Formatter):
    grey = "\x1b[38;20m"
    yellow = "\x1b[33;20m"
    red = "\x1b[31;20m"
    green = "\x1b[32;20m"
    cyan = "\x1b[36;20m"
    bold_red = "\x1b[31;1m"
    reset = "\x1b[0m"
    format = "%(levelname)s: " + reset + "%(asctime)s - %(message)s"
    datefmt = "%d.%m.%Y %H:%M:%S"

    FORMATS = {
        logging.DEBUG: cyan + format,
        logging.INFO: green + format,
        logging.WARNING: yellow + format,
        logging.ERROR: red + format,
        logging.CRITICAL: bold_red + format
    }

    def format(self, record):
        log_fmt = self.FORMATS.get(record.levelno)
        formatter = logging.Formatter(log_fmt)
        return formatter.format(record)


logger = logging.getLogger("Sailowtech CTD")
ch = logging.StreamHandler(sys.stdout)
ch.setFormatter(ColoredFormatter())
logger.setLevel(logging.DEBUG)
logger.addHandler(ch)
