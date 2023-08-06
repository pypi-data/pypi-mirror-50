import os
import sys
import logging
from logging.handlers import RotatingFileHandler

class MaxLevelFilter:
    def __init__(self, maxLevel):
        self.maxLevel = maxLevel
    def filter(self, logRecord):
        return logRecord.levelno <= self.maxLevel

def setupLogger(logName, logFolder):
    logFormatter = logging.Formatter('[%(levelname)s:%(asctime)s] %(message)s', '%Y-%m-%dT%H:%M:%S')
    logger = logging.getLogger(logName)
    if logger.handlers:
        return logger
    logger.setLevel(logging.INFO)
    infoFileHandler = RotatingFileHandler(
        filename=os.path.join(logFolder, logName+'.info.log'),
        maxBytes=3*1024*1024,
        backupCount=10
    )
    infoFileHandler.setFormatter(logFormatter)
    infoFileHandler.setLevel(logging.INFO)
    infoFileHandler.addFilter(MaxLevelFilter(logging.WARNING))
    errorFileHandler = RotatingFileHandler(
        filename=os.path.join(logFolder, logName+'.error.log'),
        maxBytes=3*1024*1024,
        backupCount=10
    )
    errorFileHandler.setFormatter(logFormatter)
    errorFileHandler.setLevel(logging.ERROR)
    logger.addHandler(infoFileHandler)
    logger.addHandler(errorFileHandler)
    # For development print to stdout and stderr
    if os.getenv('PYTHON_ENV') == 'development' or os.getenv('LOG_VERBOSE'):
        soHandler = logging.StreamHandler(sys.stdout)
        soHandler.setFormatter(logFormatter)
        soHandler.setLevel(logging.DEBUG)
        soHandler.addFilter(MaxLevelFilter(logging.WARNING))
        seHandler = logging.StreamHandler(sys.stderr)
        seHandler.setFormatter(logFormatter)
        seHandler.setLevel(logging.WARNING)
        logger.addHandler(soHandler)
        logger.addHandler(seHandler)
        logger.setLevel(logging.DEBUG)
    return logger
