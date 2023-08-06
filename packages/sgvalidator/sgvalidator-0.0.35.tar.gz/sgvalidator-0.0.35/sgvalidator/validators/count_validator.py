import termcolor
import os
import pandas as pd
import numpy as np
import pkg_resources
from ..color_printer import ColorPrinter
from .abstract_validator import AbstractValidator
from .country_validation_helpers.country_detector import CountryDetector
from .validator_decorators import ignorable


class CountValidator(AbstractValidator):
    MAXIMUM_COUNT_DIFF_THRESHOLD = 5
    MAXIMUM_PERC_DIFF_THRESHOLD = 10.0
    TRUTHSET_PATH = pkg_resources.resource_filename("sgvalidator", "validators/data/brand_count_truthset.csv")

    def __init__(self, data, debug, classesToIgnore=None):
        self.data = data.copy()  # copy so we don't mess with the global data that other validators see
        self.debug = debug
        self.classesToIgnore = classesToIgnore

    def announce(self):
        ColorPrinter.printBlueBanner("Validating POI counts...")

    @ignorable
    def validate(self):
        try:
            self.data = self.filterToUsOnly()
            poiCount, trueCount = self.getPoiCountAndRawCount()
            if not self.isPoiCountWithinRangeOfTruthsetCount(poiCount, trueCount):
                message = "WARNING: We think there should be around {} POI, but your file has {} POI. " \
                          "Are you sure you scraped correctly?".format(trueCount, poiCount)
                ColorPrinter.printYellow(message)
            else:
                message = "POI counts look good!"
                ColorPrinter.printGreen(message)
            return True
        except Exception as e:
            pass

    def filterToUsOnly(self):
        self.data["_detectedCC"] = self.data.apply(CountryDetector.detect, axis="columns")
        return self.data[self.data["_detectedCC"] == CountryDetector.US_COUNTRY_CODE]

    def getPoiCountAndRawCount(self, domain=None):
        truthset = CountValidator.loadTruthset()
        if not domain:
            domain = self.getDomain()
        else:
            domain = domain

        try:
            dataLen = len(self.data)
            res = truthset[truthset["domain"] == domain]["raw_count"]
            if len(res) == 0:
                raise Exception
            elif len(res) == 1:
                return dataLen, res.item()
            elif len(res) == 2:  # if we have counts from both mobius and mozenda
                return dataLen, res.mean()
            else:
                ColorPrinter.printYellow(
                    "Whoops! We got ourselves an error. Please paste this message in #sg-crawlers-external "
                    "so that Noah or Tenzing can fix it. Thanks!")
                raise Exception
        except Exception:
            raise Exception

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
