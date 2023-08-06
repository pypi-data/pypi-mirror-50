from .validator_utils import ValidatorUtils
from ..color_printer import ColorPrinter
from .validator_status import ValidatorStatus


def ignorable(decorated):
    def wrapper(self):
        if self.classesToIgnore and self.className() in self.classesToIgnore:
            ColorPrinter.printRedBanner("!!!!!!! Ignoring {} !!!!!!!".format(self.className()))
            return
        status = decorated(self)
        if status == ValidatorStatus.FAIL:
            ValidatorUtils.printIgnoreMessage(self.className())
    return wrapper
