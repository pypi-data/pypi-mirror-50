from .validator_utils import ValidatorUtils
from ..color_printer import ColorPrinter


def ignorable(decorated):
    def wrapper(self):
        if self.classesToIgnore and self.className() in self.classesToIgnore:
            ColorPrinter.printRedBanner("!!!!!!! Ignoring {} !!!!!!!".format(self.className()))
            return
        decorated(self)
        ValidatorUtils.printIgnoreMessage(self.className())
    return wrapper
