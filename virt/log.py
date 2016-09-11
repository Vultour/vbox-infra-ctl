import logging

import config


def init_logger(log_level):
    l = logging.getLogger(config.get_config()["app-name"])
    l.setLevel(log_level)

    formatter = logging.Formatter("%(asctime)s [%(levelname)-5s]: %(message)s")

    ch = logging.StreamHandler()
    ch.setLevel(log_level)
    ch.setFormatter(formatter)
    l.addHandler(ch)

    if (config.get_config()["log-file-enabled"]):
        fh = logging.FileHandler(config.get_config()["log-file-path"])
        fh.setLevel(log_level)
        fh.setFormatter(formatter)
        l.addHandler(fh)

    l.debug("Logger initialized")
    return l
