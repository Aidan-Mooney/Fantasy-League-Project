# from os import environ
from datetime import datetime, timezone
# import logging
# from pythonjsonlogger import jsonlogger


# LOG_PATH = environ["LOG_PATH"]


# logger = logging.getLogger()
# handler = logging.FileHandler(LOG_PATH)
# formatter = jsonlogger.JsonFormatter()
# handler.setFormatter(formatter)
# logger.addHandler(handler)
# logger.setLevel(logging.INFO)


def log_json(event_type, **log_info):
    # log_info["time"] = datetime.now(timezone.utc).isoformat(timespec="milliseconds")
    # logger.info(event_type, extra=log_info)
    "nothing to see here yet"
