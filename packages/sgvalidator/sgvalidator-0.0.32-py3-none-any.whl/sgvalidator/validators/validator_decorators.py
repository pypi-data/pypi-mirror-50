from .validator_utils import ValidatorUtils


def ignorable(decorated):
    def wrapper(self):
        if self.classesToIgnore and self.className() in self.classesToIgnore:
            print("!!!!!!! Ignoring {} !!!!!!!".format(self.className()))
            return
        decorated(self)
        ValidatorUtils.printIgnoreMessage(self.className())
    return wrapper
