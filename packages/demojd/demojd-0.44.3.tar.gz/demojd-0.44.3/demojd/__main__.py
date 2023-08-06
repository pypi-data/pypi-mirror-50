import sys
import getopt
import logging

# NOTE: if use the standard technique 'logging.getLogger(__name__)', the logger will not work properly
# and the debug message will not be printed.
# This happens because __name__ == __main__
from demojd import logger

from demojd.scripts.hello import hello

try:
    opts, args = getopt.getopt(sys.argv[1:], 'd', [])
except getopt.GetoptError as err:
    logger.error(err)
    logger.info(__doc__)
    sys.exit(2)

for opt, args in opts:
    if opt == '-d':
        logger.setLevel(logging.DEBUG)

hello()
