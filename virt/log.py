import logging
import sys

import config


class STDOutFilter(logging.Filter): # Only log WARN and below messages to stdout
    def filter(self, record):
        if (record.levelno >= logging.ERROR): return 0
        return 1

def init_logger(log_level):
    l = logging.getLogger(config.get_config()["app-name"])
    l.setLevel(log_level)

    formatter = logging.Formatter("%(asctime)s [%(levelname)-5s]: %(message)s")

    ch = logging.StreamHandler(sys.stdout)
    ch.setLevel(log_level)
    ch.setFormatter(formatter)
    ch.addFilter(STDOutFilter())
    l.addHandler(ch)

    ch_err = logging.StreamHandler(sys.stderr) # Log ERROR and above messages to stderr
    ch_err.setLevel(logging.ERROR)
    ch_err.setFormatter(formatter)
    l.addHandler(ch_err)

    if (config.get_config()["log-file-enabled"]):
        fh = logging.FileHandler(config.get_config()["log-file-path"])
        fh.setLevel(log_level)
        fh.setFormatter(formatter)
        l.addHandler(fh)

    l.debug("Logger initialized")
    return l
