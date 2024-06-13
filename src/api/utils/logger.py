import logging


class Logger:
    def __init__(self, logger_name: str):
        self.logger = logging.getLogger(name=logger_name)
        self.logger.setLevel(logging.INFO)
        handler = logging.StreamHandler()
        formatter = logging.Formatter(
            fmt="[%(asctime)s] [%(name)s] | %(levelname)s -> %(message)s",
            datefmt="%Y-%m-%d %H:%M:%S",
        )
        handler.setFormatter(formatter)
        self.logger.addHandler(handler)

    def debug(self, message: str):
        return self.logger.debug(message)

    def info(self, message: str):
        return self.logger.info(message)

    def warning(self, message: str):
        return self.logger.warning(message)

    def error(self, message: str):
        return self.logger.error(message)
