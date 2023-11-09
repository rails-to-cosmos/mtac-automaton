import logging

def init_logger(name: str,
                level: int = logging.DEBUG,
                fmt: str = '%(asctime)s - %(levelname)s - %(name)s - %(message)s'):

    logger = logging.getLogger(name)
    logger.setLevel(level)

    stream_handler = logging.StreamHandler()
    stream_handler.setLevel(level)

    formatter = logging.Formatter(fmt)

    stream_handler.setFormatter(formatter)
    logger.addHandler(stream_handler)

    return logger
