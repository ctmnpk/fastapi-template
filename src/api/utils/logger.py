import logging


class Logger:
    """
    Logger is a class that sets up and provides a configured logger for logging messages.
    
    Methods:
    --------
    __init__(logger_name: str):
        Initializes the Logger instance with a specified logger name.
        
    _logger_setup():
        Sets up the logging handler and formatter.
    
    _get_logger() -> logging.Logger:
        Returns the configured logger instance.
    """
    def __init__(self, logger_name: str):
        """
        Initializes the Logger instance.
        
        Parameters:
        -----------
        logger_name : str
            The name to be assigned to the logger instance.
        """
        self.logger = logging.getLogger(name=logger_name)
        self.logger.setLevel(logging.INFO)
        self._logger_setup()

    def _logger_setup(self):
        """
        Sets up the logging handler and formatter.
        
        This method configures the logger to use a StreamHandler with a specific
        format for log messages, including the timestamp, logger name, log level,
        and the message itself.
        """
        handler = logging.StreamHandler()
        formatter = logging.Formatter(
            fmt="[%(asctime)s] [%(name)s] | %(levelname)s -> %(message)s",
            datefmt="%Y-%m-%d %H:%M:%S",
        )
        handler.setFormatter(formatter)
        self.logger.addHandler(handler)

    def _get_logger(self):
        """
        Returns the configured logger instance.
        
        Returns:
        --------
        logging.Logger
            The logger instance configured with the specified name, handler, and formatter.
        """
        return self.logger
