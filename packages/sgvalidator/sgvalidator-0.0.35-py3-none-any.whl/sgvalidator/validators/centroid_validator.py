from ..color_printer import ColorPrinter
from .abstract_validator import AbstractValidator
from .validator_utils import ValidatorUtils
from .validator_decorators import ignorable


class CentroidValidator(AbstractValidator):
    MINIMUM_NUMBER_SIGNIFICANT_DIGITS_FOR_LAT_LNG = 5
    EITHER_LAT_OR_LNG_IS_EMPTY = "EITHER_LAT_OR_LNG_IS_EMPTY"
    EITHER_LAT_OR_LNG_NON_NUMERIC = "EITHER_LAT_OR_LNG_NON_NUMERIC"
    EITHER_LAT_OR_LNG_IS_OUTSIDE_OF_RANGE = "EITHER_LAT_OR_LNG_IS_OUTSIDE_OF_RANGE"
    EITHER_LAT_OR_LNG_IS_IMPRECISE = "EITHER_LAT_OR_LNG_IMPRECISE"

    def __init__(self, data, debug, classesToIgnore=None):
        self.data = data.copy()
        self.debug = debug
        self.classesToIgnore = classesToIgnore

    def announce(self):
        ColorPrinter.printBlueBanner("Checking for centroid quality issues...")

    @ignorable
    def validate(self):
        rowsWithBadCentroids = self.getRowsWithBadCentroids()
        if len(rowsWithBadCentroids) > 0:
            debugExamples = rowsWithBadCentroids.head(5)
            message = "We found {} rows with bad centroids. Look at the REASON column in the output below to " \
                      "see why these rows were flagged. \nNote: if you see " \
                      "`{}`, that means that either your latitude or " \
                      "longitude has fewer than {} significant figures (i.e. the number of digits trailing the dot). " \
                      "Examples:\n{}\n".format(
                len(rowsWithBadCentroids), CentroidValidator.EITHER_LAT_OR_LNG_IS_IMPRECISE,
                CentroidValidator.MINIMUM_NUMBER_SIGNIFICANT_DIGITS_FOR_LAT_LNG, debugExamples)
            ValidatorUtils.fail(message, self.debug)

    def getRowsWithBadCentroids(self):
        badCentroidReason = self.data.apply(self.getBadCentroidReason, axis=1)
        self.data["REASON"] = badCentroidReason
        dataToReturn = self.data[["location_name", "street_address", "zip", "city", "state", "latitude", "longitude",
                                  "REASON"]]
        mask = badCentroidReason.astype("bool")
        return dataToReturn[mask]

    def getBadCentroidReason(self, row):
        """
        Return a bad centroid reason if there is one, otherwise return 0
        """
        latitude, longitude = row["latitude"], row["longitude"]
        if self.bothBlank(latitude, longitude):
            return 0
        elif self.eitherLatOrLngIsEmptyButNotBoth(latitude, longitude):
            return CentroidValidator.EITHER_LAT_OR_LNG_IS_EMPTY
        elif self.eitherNonNumeric(latitude, longitude):
            return CentroidValidator.EITHER_LAT_OR_LNG_NON_NUMERIC
        elif self.eitherOutsideOfRange(latitude, longitude):
            return CentroidValidator.EITHER_LAT_OR_LNG_IS_OUTSIDE_OF_RANGE
        elif self.eitherImprecise(latitude, longitude):
            return CentroidValidator.EITHER_LAT_OR_LNG_IS_IMPRECISE
        return 0

    def eitherImprecise(self, latitude, longitude):
        return not self.isPreciseEnough(latitude) or not self.isPreciseEnough(longitude)

    @staticmethod
    def isPreciseEnough(val):
        splitted = str(val).split(".")
        if len(splitted) == 1:
            return False
        else:
            numSigfigs = len(splitted[1])
            return numSigfigs >= CentroidValidator.MINIMUM_NUMBER_SIGNIFICANT_DIGITS_FOR_LAT_LNG

    @staticmethod
    def bothBlank(latitude, longitude):
        return ValidatorUtils.is_blank(latitude) and ValidatorUtils.is_blank(longitude)

    @staticmethod
    def eitherLatOrLngIsEmptyButNotBoth(latitude, longitude):
        return (ValidatorUtils.is_blank(latitude) and ValidatorUtils.is_not_blank(longitude)) or \
               (ValidatorUtils.is_not_blank(latitude) and ValidatorUtils.is_blank(longitude))

    @staticmethod
    def eitherOutsideOfRange(latitude, longitude):
        return not (-90.0 <= float(latitude) <= 90.0) or not (-180.0 <= float(longitude) <= 180.0)

    @staticmethod
    def eitherNonNumeric(latitude, longitude):
        return not ValidatorUtils.is_number(longitude) or not ValidatorUtils.is_number(latitude)
