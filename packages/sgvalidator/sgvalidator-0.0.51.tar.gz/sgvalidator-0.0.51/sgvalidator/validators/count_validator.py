import os
import pandas as pd
import numpy as np
import pkg_resources
from ..color_printer import ColorPrinter
from .abstract_validator import AbstractValidator
from .country_validation_helpers.country_detector import CountryDetector
from .validator_decorators import ignorable
from .validator_status import ValidatorStatus
from .validator_utils import ValidatorUtils


class CountValidator(AbstractValidator):
    MAXIMUM_COUNT_DIFF_THRESHOLD = 5
    MAXIMUM_PERC_DIFF_THRESHOLD = 10.0
    TRUTHSET_PATH = pkg_resources.resource_filename("sgvalidator", "validators/data/brand_count_truthset.csv")

    def __init__(self, data, classesToIgnore=None):
        self.data = data.copy()  # copy so we don't mess with the global data that other validators see
        self.classesToIgnore = classesToIgnore

    def announce(self):
        ColorPrinter.printBlueBanner("Validating POI counts...")

    def subvalidators(self):
        return [
            self.validatePoiCountAgainstRawCount
        ]

    @ignorable
    def validatePoiCountAgainstRawCount(self):
        self.data = self.filterToUsOnly()
        poiCount, trueCount = self.getPoiCountAndRawCount()
        if trueCount and not self.isPoiCountWithinRangeOfTruthsetCount(poiCount, trueCount):
            message = "We think there should be around {} POI, but your file has {} POI. " \
                      "Are you sure you scraped correctly?".format(trueCount, poiCount)
            ValidatorUtils.fail(message)
            return ValidatorStatus.FAIL
        return ValidatorStatus.SUCCESS

    def filterToUsOnly(self):
        self.data["_detectedCC"] = self.data.apply(CountryDetector.detect, axis="columns")
        return self.data[self.data["_detectedCC"] == CountryDetector.US_COUNTRY_CODE]

    def getPoiCountAndRawCount(self, domain=None):
        truthset = CountValidator.loadTruthset()
        if not domain:
            domain = self.getDomain()
        else:
            domain = domain

        dataLen = len(self.data)
        res = truthset[truthset["domain"] == domain]["raw_count"]
        if len(res) == 0:
            return dataLen, None
        elif len(res) == 1:
            return dataLen, res.item()
        elif len(res) == 2:  # if we have counts from both mobius and mozenda
            return dataLen, res.mean()

    @staticmethod
    def isPoiCountWithinRangeOfTruthsetCount(poiCount, rawCount):
        upperPerc = 1.0 + CountValidator.MAXIMUM_PERC_DIFF_THRESHOLD / 100.0
        lowerPerc = 1.0 - CountValidator.MAXIMUM_PERC_DIFF_THRESHOLD / 100.0
        isPoiCountWithinPercRange = int(rawCount * upperPerc) >= poiCount >= int(rawCount * lowerPerc)
        isPoiCountWithinAbsRange = np.abs(poiCount - rawCount) <= CountValidator.MAXIMUM_COUNT_DIFF_THRESHOLD
        return isPoiCountWithinPercRange or isPoiCountWithinAbsRange

    @staticmethod
    def getDomain():
        encodedDomain = os.getcwd().split("/")[-1]
        return encodedDomain.replace("_", ".")

    @staticmethod
    def loadTruthset():
        return pd.read_csv(CountValidator.TRUTHSET_PATH)
