from logging.handlers import RotatingFileHandler
from datetime import datetime
import logging
import sys
import os


from src.constants import LoggingConstants, project_dir

log_file = f"logs/log-OBC-{datetime.now().strftime('%d-%m-%Y_%H-%M')}.log"
log_file_dir = os.path.join(project_dir, log_file)

logger = logging.getLogger(__name__)
file_handler = RotatingFileHandler(log_file_dir, maxBytes=10485760, backupCount=5)  # 10MB
file_handler.setFormatter(
    logging.Formatter("%(asctime)s - %(module)s - %(funcName)s() - line %(lineno)d - %(levelname)s - %(message)s")
)
logger.addHandler(file_handler)
logger.setLevel(LoggingConstants.LOG_LEVEL)

logging.getLogger().addHandler(logging.StreamHandler(sys.stdout))

