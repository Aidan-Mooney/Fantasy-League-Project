# from os import environ
# import logging
# from pythonjsonlogger import jsonlogger


# LOG_PATH = environ["LOG_PATH"]


# logger = logging.getLogger()
# handler = logging.FileHandler(LOG_PATH)
# formatter = jsonlogger.JsonFormatter()
# handler.setFormatter(formatter)
# logger.addHandler(handler)
# logger.setLevel(logging.INFO)


def log_json(event_name, extras):
    # logger.info(event_name, extra=extras)
    "nothing to see here yet"
