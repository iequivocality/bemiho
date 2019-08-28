from utilities.singleton import Singleton

class BemihoService(metaclass=Singleton):
    def start(self, **kwargs):
        raise NotImplementedError()

    def is_required(self):
        return True

    def stop(self):
        raise NotImplementedError()