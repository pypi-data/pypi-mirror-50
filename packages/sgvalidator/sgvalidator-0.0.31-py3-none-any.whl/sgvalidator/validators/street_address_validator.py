import usaddress
from .validator_utils import ValidatorUtils
from ..color_printer import ColorPrinter
from .abstract_validator import AbstractValidator


class StreetAddressValidator(AbstractValidator):
    def __init__(self, data, debug):
        self.data = data
        self.debug = debug

    def announce(self):
        ColorPrinter.printBlue("Validating street addresses...")

    def validate(self):
        addressesWithNoNumber = self.getAddressesWithNoNumber()
        addressesWithStateName = self.getAddressesWithStateName()
        if len(addressesWithNoNumber) > 0:
            debugExamples = addressesWithNoNumber.head(5)
            message = "Found {} addresses with no number. Examples:\n{}\n".format(len(addressesWithNoNumber),
                                                                                  debugExamples)
            ValidatorUtils.fail(message, self.debug)
        elif len(addressesWithStateName) > 0:
            debugExamples = addressesWithStateName.head(5)
            message = "Found {} addresses that contain the name of a state. Are you sure you scraped correctly? " \
                      "Examples:\n{}\n".format(len(addressesWithStateName), debugExamples)
            ValidatorUtils.fail(message, self.debug)

    def getAddressesWithNoNumber(self):
        mask = self.data.apply(lambda x: self.doesAddressHaveKey(x["street_address"], "AddressNumber"), axis=1)
        return self.data[~mask]

    def getAddressesWithStateName(self):
        mask = self.data.apply(lambda x: self.doesAddressHaveKey(x["street_address"], "StateName"), axis=1)
        return self.data[mask]

    @staticmethod
    def doesAddressHaveKey(addr, key):
        parsed = dict(usaddress.parse(addr))
        return key in parsed.values()
