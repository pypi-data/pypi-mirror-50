from abc import ABCMeta, abstractmethod


class AbstractValidator:
    __metaclass__ = ABCMeta

    def run(self):
        self.announce()
        self.validate()

    @abstractmethod
    def announce(self):
        pass

    @abstractmethod
    def validate(self):
        pass

    def className(self):
        return self.__class__.__name__
