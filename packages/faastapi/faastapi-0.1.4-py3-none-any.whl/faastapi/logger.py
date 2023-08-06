import logging


logger = logging.getLogger("fastapi")
logger.setLevel(logging.DEBUG)

formatter = logging.Formatter("%(asctime)s :: %(levelname)s :: %(message)s")

stream_handler = logging.StreamHandler()
stream_handler.setFormatter(formatter)
stream_handler.setLevel(logging.DEBUG)

logger.addHandler(stream_handler)
