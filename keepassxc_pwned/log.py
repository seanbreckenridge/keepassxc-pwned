import sys
import logging

logger = None

if logger is None:
    # log_level = logging.ERROR
    # log_level = logging.INFO
    log_level = logging.DEBUG
    logger = logging.getLogger("keepassxc_pwned_logger")
    sh = logging.StreamHandler(sys.stdout)
    sh.setLevel(log_level)
    logging.getLogger().setLevel(
        log_level
    )  # https://stackoverflow.com/questions/32681289
    sh.setFormatter(logging.Formatter("%(msg)s"))
    logger.addHandler(sh)
