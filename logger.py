import logging
import inspect

from utilities.reflect import get_qualified_name
from logging import StreamHandler, Formatter, getLogger, DEBUG, INFO
from logging.handlers import TimedRotatingFileHandler

class BemihoLogger:
    def __init__(self, name_or_class):
        self.logger = getLogger(self.get_name(name_or_class))
        self.logger.setLevel(DEBUG)
        self.init_handlers()

    def get_name(self, name_or_class):
        name = ''
        if (inspect.isclass(name_or_class) or inspect.isfunction(name_or_class)):
            name = get_qualified_name(name_or_class)
        else:
            name = str(name_or_class)
        return name

    def init_handlers(self):
        formatter = Formatter('%(asctime)s %(name)-4s %(levelname)-4s %(message)s')

        stream_handler = StreamHandler()
        stream_handler.setLevel(logging.INFO)
        stream_handler.setFormatter(formatter)

        file_handler = TimedRotatingFileHandler(filename = 'log/bemiho.log', when='midnight', backupCount = 5)
        file_handler.setFormatter(formatter)
        file_handler.setLevel(logging.DEBUG)

        self.logger.addHandler(file_handler)
        self.logger.addHandler(stream_handler)

    def get_logger(self):
        return self.logger