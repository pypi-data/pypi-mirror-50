import logging
import os

console = logging.StreamHandler()
logger = logging.getLogger(__name__)
logger.addHandler(console)
logger.setLevel(logging.INFO)

data_fpath = __path__[0] + os.sep + 'data' + os.sep + 'others.json'
