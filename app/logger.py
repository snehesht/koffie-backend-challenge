import logging
import os 

default_level = os.environ.get('LOG_LEVEL', 'INFO')

logger = logging.getLogger(__name__)
logger.setLevel(default_level)

# Log to stdout and stderr

channel = logging.StreamHandler();
channel.setLevel(default_level)
formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
channel.setFormatter(formatter)

logger.addHandler(channel);