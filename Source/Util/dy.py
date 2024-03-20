import logging
import os.path

# referenced https://stackoverflow.com/questions/384076/how-can-i-color-python-logging-output
LOG_LEVEL = logging.DEBUG
LOGFORMAT = "  %(log_color)s%(levelname)-8s%(reset)s | %(log_color)s%(message)s%(reset)s"
from colorlog import ColoredFormatter
logging.root.setLevel(LOG_LEVEL)
formatter = ColoredFormatter(LOGFORMAT)
stream = logging.StreamHandler()
stream.setLevel(LOG_LEVEL)
stream.setFormatter(formatter)
log = logging.getLogger('pythonConfig')
log.setLevel(LOG_LEVEL)
log.addHandler(stream)


def read_text(file_path):

    if not os.path.exists(file_path):
        log.error(f"File not found: {file_path}")
        return ""

    with open(file_path, 'r') as file:
        return file.read()