import logging
import os
from colorlog import ColoredFormatter

LOG_LEVEL = logging.DEBUG

LOGFORMAT = "  %(log_color)s%(levelname)-8s%(reset)s | %(module)s:%(funcName)s:%(lineno)d | %(log_color)s%(message)s%(reset)s"
FILELOGFORMAT = '%(asctime)s - %(module)s:%(funcName)s:%(lineno)-d - %(levelname)s - %(message)s'

# logging.root.setLevel(LOG_LEVEL)
formatter = ColoredFormatter(LOGFORMAT)
fileFormatter = logging.Formatter(FILELOGFORMAT)

stream = logging.StreamHandler()
stream.setLevel(LOG_LEVEL)
stream.setFormatter(formatter)


logFilePath = os.path.join(os.getcwd(), 'pyLog.log')
fstream = logging.FileHandler(logFilePath)
fstream.setLevel(logging.DEBUG)
fstream.setFormatter(fileFormatter)
# print("logFilePath : ", logFilePath)

log = logging.getLogger('pythonConfig')
log.addHandler(stream)
log.addHandler(fstream)
log = log

# log.debug("A quirky message only developers care about")
# log.info("Curious users might want to know this")
# log.warning("Something is wrong and any user should be informed")
# log.error("Serious stuff, this is red for a reason")
# log.critical("OH NO everything is on fire")