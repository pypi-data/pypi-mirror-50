import usaddress
from .validator_utils import ValidatorUtils
from ..color_printer import ColorPrinter
from .abstract_validator import AbstractValidator
from .validator_status import ValidatorStatus
from .validator_decorators import ignorable
from .country_validator import CountryDetector


class StreetAddressValidator(AbstractValidator):
    def __init__(self, data, classesToIgnore=None):
        self.data = data
        self.classesToIgnore = classesToIgnore

    def announce(self):
        ColorPrinter.printBlueBanner("Validating street addresses...")

    def subvalidators(self):
        return [
            self.validateStreetAddress
        ]

    @ignorable
    def validateStreetAddress(self):
        usData = self.filterToUsOnly()
        addressesWithNoNumber = self.getAddressesWithNoNumber(usData)
        addressesWithStateName = self.getAddressesWithStateName(usData)
        if len(addressesWithNoNumber) > 0:
            debugExamples = addressesWithNoNumber.head(5)
            message = "Found {} addresses with no number. Examples:\n{}\n".format(len(addressesWithNoNumber),
                                                                                  debugExamples)
            ValidatorUtils.fail(message)
            return ValidatorStatus.FAIL
        elif len(addressesWithStateName) > 0:
            debugExamples = addressesWithStateName.head(5)
            message = "Found {} addresses that contain the name of a state. Are you sure you scraped correctly? " \
                      "Examples:\n{}\n".format(len(addressesWithStateName), debugExamples)
            ValidatorUtils.fail(message)
            return ValidatorStatus.FAIL
        return ValidatorStatus.SUCCESS

    def getAddressesWithNoNumber(self, usData):
        mask = usData.apply(lambda x: self.doesAddressHaveKey(x["street_address"], "AddressNumber"), axis=1)
        return usData[~mask]

    def getAddressesWithStateName(self, usData):
        mask = usData.apply(lambda x: self.doesAddressHaveKey(x["street_address"], "StateName"), axis=1)
        return usData[mask]

    @staticmethod
    def doesAddressHaveKey(addr, key):
        parsed = dict(usaddress.parse(addr))
        return key in parsed.values()

    def filterToUsOnly(self):
        self.data["_detectedCC"] = self.data.apply(CountryDetector.detect, axis="columns")
        return self.data[self.data["_detectedCC"] == CountryDetector.US_COUNTRY_CODE]
