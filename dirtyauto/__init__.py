import logging
import logging.config
import sys

logger = logging.getLogger(__name__)
logger.addHandler(logging.NullHandler)

# def singleton(cls):
#    instances = {}
#    def get_instance():
#        if cls not in instances:
#            instances[cls] = cls()
#        return instances[cls]
#    return get_instance()

# @singleton
# class Logger():
#    def __init__(self, className=None):
logging.config.dictConfig({
    'version': 1,
    'disable_existing_loggers': False,  # this fixes the problem

    'formatters': {
        'standard': {
            'format': '%(asctime)s [%(levelname)s] [%(name)s] %(message)s'
        },
    },
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
            'level': 'DEBUG',
            'formatter': 'standard',
            'stream': 'ext://sys.stdout',
        },
        'file': {
            'level': 'INFO',
            'class': 'logging.FileHandler',
            'formatter': 'standard',
            'filename': 'dirtyauto.log',
        },
    },
    'loggers': {
        '': {
            'handlers': ['file', 'console', ],
            'level': 'DEBUG',
            'propagate': True
        }
    }
})


def log(class_name):
    return logging.getLogger(class_name)

    # formatter = logging.Formatter('%(asctime)s::%(name)s::%(levelname)s::%(message)s')
    # filehandler = logging.FileHandler('log.txt')
    # filehandler.setLevel(logging.INFO)
    # filehandler.setFormatter(formatter)
    # logger.addHandler(filehandler)

    # ch = logging.StreamHandler(sys.stdout)
    # ch.setFormatter(formatter)
    # logger.addHandler(ch)
