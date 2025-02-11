import argparse

from src.comet.utils.setup_logger import logging, setup_logger


def parse_args_and_setup_logging() -> logging.Logger:
    """Parse command line arguments and set up logging configuration.

    This function initializes argument parsing for command line options
    and sets up the logging configuration for the application.

    Returns
    -------
    logging.Logger
        Configured logger instance with the log level specified
        by the --log command line argument.

    """
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--log",
        default="INFO",
    )

    args = parser.parse_args()
    return setup_logger(args.log)
