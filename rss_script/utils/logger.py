import logging


def configure_logger(log_file: str) -> logging.Logger:
    """
    Configures the logger

    Args:
        log_file: Absolute path to the log file

    Returns:
        The logger object
    """
    logger = logging.getLogger('rss_script')
    logger.setLevel(logging.DEBUG)
    # Create a file handler
    file_handler = logging.FileHandler(log_file, mode='w')
    file_handler.setLevel(logging.DEBUG)
    file_handler.setFormatter(
        logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s', "%Y-%m-%d %H:%M:%S"))
    logger.addHandler(file_handler)
    # Create a console handler and set the level to INFO with no date formatter
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.INFO)
    console_handler.setFormatter(logging.Formatter('%(name)s - %(levelname)s - %(message)s'))
    logger.addHandler(console_handler)
    return logger
