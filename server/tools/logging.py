import logging


def get_logger():
    logger_ = logging.getLogger("PlaylistsCreatorLogger")
    log_format = logging.Formatter("[%(threadName)s] %(asctime)s [%(levelname)s]  %(message)s")
    stream_handler = logging.StreamHandler()
    stream_handler.setFormatter(log_format)
    logger_.addHandler(stream_handler)

    return logger_


logger = get_logger()
