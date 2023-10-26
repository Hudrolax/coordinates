import logging
from logging.handlers import RotatingFileHandler
import os
import sys
from utils import get_env_value


LOG_FORMAT = '%(name)s (%(levelname)s) %(asctime)s: %(message)s'
LOG_LEVEL = logging.INFO

LOG_TO_FILE = True if os.getenv('LOG_TO_FILE') == 'true' else False

log_dir = 'logs'
log_file = 'midjourney_api_log.txt'

handlers = []

if LOG_TO_FILE:
    if not os.path.exists(log_dir):
        os.makedirs(log_dir)
    handler = RotatingFileHandler(os.path.join(
        log_dir, log_file), maxBytes=2097152, backupCount=5)
    formatter = logging.Formatter(LOG_FORMAT)
    handler.setFormatter(formatter)
    handlers.append(handler)

console_handler = logging.StreamHandler(sys.stdout)
formatter = logging.Formatter(LOG_FORMAT)
console_handler.setFormatter(formatter)
handlers.append(console_handler)

logging.basicConfig(level=LOG_LEVEL, handlers=handlers)


PAGE_URL = get_env_value("PAGE_URL")
TOKEN = get_env_value("TOKEN")
