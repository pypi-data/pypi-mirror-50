import pandas as pd
import itertools
from .validators.centroid_validator import CentroidValidator
from .validators.country_validator import CountryValidator
from .validators.duplication_validator import DuplicationValidator
from .validators.fill_rate_validator import FillRateValidator
from .validators.schema_validator import SchemaValidator
from .validators.trash_value_validator import TrashValueValidator
from .validators.count_validator import CountValidator
from .validators.street_address_validator import StreetAddressValidator
from .validators.geo_consistency_validator import GeoConsistencyValidator
from .validators.store_number_column_validator import StoreNumberColumnValidator
from .validators.validator_status import ValidatorStatus
from .color_printer import ColorPrinter


class ValidatorRunner:
    def __init__(self, data, classesToIgnore):
        self.rawData = data
        self.data = pd.DataFrame(data)
        self.classesToIgnore = classesToIgnore
        self.validators = [
            # Schema and FillRate run first to catch anything that will break code later on
            SchemaValidator(self.data, self.rawData),  # todo - move this off of raw data
            FillRateValidator(self.data, classesToIgnore=classesToIgnore),
            DuplicationValidator(self.data, classesToIgnore=classesToIgnore),
            CentroidValidator(self.data, classesToIgnore=classesToIgnore),
            CountryValidator(self.data, classesToIgnore=classesToIgnore),
            TrashValueValidator(self.data, classesToIgnore=classesToIgnore),
            CountValidator(self.data, classesToIgnore=classesToIgnore),
            StoreNumberColumnValidator(self.data, classesToIgnore=classesToIgnore),
            StreetAddressValidator(self.data, classesToIgnore=classesToIgnore),
            GeoConsistencyValidator(self.data, classesToIgnore=classesToIgnore)
        ]

    def run(self):
        resLists = [validator.run() for validator in self.validators]
        results = list(itertools.chain.from_iterable(resLists))
        numSuccesses = len(list(filter(lambda x: x == ValidatorStatus.SUCCESS, results)))
        numIgnored = len(list(filter(lambda x: x == ValidatorStatus.IGNORED, results)))
        numFailures = len(list(filter(lambda x: x == ValidatorStatus.FAIL, results)))
        numWarnings = len(list(filter(lambda x: x == ValidatorStatus.WARN, results)))
        self.printStatus(numSuccesses, numIgnored, numFailures, numWarnings)
        return numFailures

    @staticmethod
    def printStatus(numSuccesses, numIgnored, numFailures, numWarnings):
        ColorPrinter.printWhiteBanner("\n============= Results =============")
        ColorPrinter.printGreenBanner("======== {} checks passing ========".format(numSuccesses))
        ColorPrinter.printYellowBanner("======== {} checks ignored ========".format(numIgnored))
        ColorPrinter.printCyanBanner("======== {} checks warning ========".format(numWarnings))
        ColorPrinter.printRedBanner("======== {} checks failing ========".format(numFailures))
        ColorPrinter.printWhiteBanner("===================================\n")
        if numFailures > 0:
            ColorPrinter.printYellowBanner("Close! You still have {} check(s) that need to pass.".format(numFailures))
        else:
            ColorPrinter.printGreenBanner("Congratulations! All your checks passed.")

