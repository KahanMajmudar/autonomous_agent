import logging


class Logger:

    def setup_log():
        format = "%(asctime)s: %(message)s"
        logging.basicConfig(format=format, level=logging.INFO, datefmt="%H:%M:%S")
        logger = logging.getLogger(__name__)
        return logger


logger = Logger.setup_log()
