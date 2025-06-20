import logging

from config import setting

logging.basicConfig(
    filename=f"{setting.LOG_DIR}/basic_chat.log",
    level=logging.INFO,
    format="%(levelname)s - %(asctime)s - %(filename)s - %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S"
)