import sys
import logging

logger: logging.Logger = logging.getLogger("keepassxc_pwned")


def setup_logs(log_level: int = logging.INFO):
    """
    Setup the global logger
    This does not setup logs more than once.
    """
    global logger
    if logger.handlers:
        return  # logs have already been set up
    logger = logging.getLogger("keepassxc_pwned")
    sh = logging.StreamHandler(sys.stdout)
    sh.setLevel(log_level)
    sh.setFormatter(logging.Formatter("%(msg)s"))
    logger.addHandler(sh)


def set_level(log_level: int = logging.INFO):
    """
    Sets the log level for the application
    """
    global logger
    logger.setLevel(log_level)
    for handler in logger.handlers:
        handler.setLevel(log_level)
