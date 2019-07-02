import logging

class BemihoLogger:
    def __init__(self, name):
        self.logger = logging.getLogger(name)
        self.init_handlers()

    def init_handlers(self):
        streamHandler = logging.StreamHandler()
        fileHandler = logging.FileHandler('file.log')
        formatter = logging.Formatter('%(asctime)s %(name)-6s %(levelname)-6s %(message)s')
        streamHandler.setFormatter(formatter)
        fileHandler.setFormatter(formatter)
        self.logger.addHandler(fileHandler)
        self.logger.addHandler(streamHandler)
        self.logger.setLevel(logging.WARNING)
        self.logger.setLevel(logging.DEBUG)

    def get_logger(self):
        return self.logger