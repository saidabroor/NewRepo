import logging
from datetime import datetime
import os

LOG_FILE = f"{datetime.now().strftime('%m_%d,%_Y,%_H,%_M,_%_S')}.log"

log_path = os.path.join(os.getcwd(),'logs',LOG_FILE)

os.makedirs(log_path, exist_ok=True)

logging.basicConfig(
  filename=LOG_FILE,
  format="[%(asctime)s] %(lineno)d %(name)s - %(levelname)s - %(message)s",
  level=logging.INFO
)