import logging
from logging import FileHandler, StreamHandler, Formatter


def get_logger(name, log_file):
    logger = logging.getLogger(name)
    logger.setLevel(logging.DEBUG)

    log_format = Formatter(fmt="%(asctime)s - %(filename)s - %(levelname)s - %(message)s", datefmt="%Y-%m-%d %H:%M:%S")

    file_handler = FileHandler(log_file)
    file_handler.setFormatter(log_format)

    console_handler = StreamHandler()
    console_handler.setFormatter(log_format)

    logger.addHandler(file_handler)
    logger.addHandler(console_handler)

    return logger
