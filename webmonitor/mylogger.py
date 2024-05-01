# logger.py
import logging

def configure_logging(filename, level=logging.INFO):
    """
    Configure logging with specified filename and log level.
    """
    # Create a logger
    logger = logging.getLogger()
    logger.setLevel(level)

    # Create a file handler and set its log level
    file_handler = logging.FileHandler(filename)
    file_handler.setLevel(level)

    # Create a console handler and set its log level
    console_handler = logging.StreamHandler()
    console_handler.setLevel(level)

    # Define the log format with timestamp, log level, module name, function name, line number and log message
    formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(module)s - %(funcName)s - %(lineno)d - %(message)s')
    file_handler.setFormatter(formatter)
    console_handler.setFormatter(formatter)

    # Add the handlers to the logger
    logger.addHandler(file_handler)
    logger.addHandler(console_handler)

# Example usage:
# configure_logging('app.log')
