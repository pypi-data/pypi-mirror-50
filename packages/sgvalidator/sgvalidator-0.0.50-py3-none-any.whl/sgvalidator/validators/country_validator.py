from ..color_printer import ColorPrinter
from .abstract_validator import AbstractValidator
from .country_validation_helpers.country_detector import CountryDetector
from .country_validation_helpers.us_row_validator import UsRowValidator
from .country_validation_helpers.ca_row_validator import CaRowValidator
from .validator_status import ValidatorStatus


class CountryValidator(AbstractValidator):
    def __init__(self, data, classesToIgnore=None):
        self.data = data
        self.classesToIgnore = classesToIgnore
        self.caRowValidator = CaRowValidator()
        self.usRowValidator = UsRowValidator()

    def announce(self):
        ColorPrinter.printBlueBanner("Validating country-specific information (states, zip codes, phone #'s)...")

    def subvalidators(self):
        return [
            self.validateCountry
        ]

    def validateCountry(self):
        numSuccesses = 0
        numFails = 0
        for index, row in self.data.iterrows():
            detectedCountryCode = CountryDetector.detect(row)
            if self.validateRow(row, detectedCountryCode) == ValidatorStatus.FAIL:
                numFails += 1
        if numFails > 0:
            return ValidatorStatus.FAIL
        return ValidatorStatus.SUCCESS

    def validateRow(self, row, detectedCountryCode):
        if detectedCountryCode == CountryDetector.US_COUNTRY_CODE:
            return self.usRowValidator.validate(row)
        elif detectedCountryCode == CountryDetector.CA_COUNTRY_CODE:
            return self.caRowValidator.validate(row)
