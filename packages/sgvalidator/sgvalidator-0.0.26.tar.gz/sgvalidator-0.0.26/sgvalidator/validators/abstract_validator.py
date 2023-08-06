from abc import ABCMeta, abstractmethod


class AbstractValidator():
    __metaclass__ = ABCMeta

    @abstractmethod
    def validate(self):
        pass

    @abstractmethod
    def announce(self):
        pass
