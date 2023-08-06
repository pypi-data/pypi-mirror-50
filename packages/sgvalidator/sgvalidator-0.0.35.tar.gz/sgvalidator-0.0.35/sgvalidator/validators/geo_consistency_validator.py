import us
from uszipcode import SearchEngine
from .abstract_validator import AbstractValidator
from ..color_printer import ColorPrinter
from .validator_utils import ValidatorUtils
from .validator_decorators import ignorable
from .country_validation_helpers.country_detector import CountryDetector


class GeoConsistencyValidator(AbstractValidator):
    zipsearch = SearchEngine(simple_zipcode=True)
    ZIPCODE_NOT_IN_STATE = "ZIPCODE_NOT_IN_STATE"

    def __init__(self, data, debug, classesToIgnore=None):
        self.data = data.copy()
        self.debug = debug
        self.classesToIgnore = classesToIgnore

    def announce(self):
        ColorPrinter.printBlueBanner("Validating consistency of geography columns...")

    @ignorable
    def validate(self):
        inconsistentGeoRows = self.getInconsistentGeoRows()
        if len(inconsistentGeoRows) > 0:
            debugExamples = inconsistentGeoRows.head(5)
            message = "Found {} rows with inconsistent geographies. Look at the REASON column in the output below to " \
                      "see why these rows were flagged. Examples:\n{}\n".format(len(inconsistentGeoRows), debugExamples)
            ValidatorUtils.fail(message, self.debug)

    def getInconsistentGeoRows(self):
        usData = self.filterToUsOnly()
        badGeoConsistencyReason = usData.apply(self.getBadGeoConsistencyReason, axis=1)
        usData["REASON"] = badGeoConsistencyReason
        dataToReturn = usData[["location_name", "street_address", "zip", "city", "state", "latitude", "longitude",
                                  "REASON"]]
        mask = badGeoConsistencyReason.astype("bool")
        return dataToReturn[mask]

    @staticmethod
    def getBadGeoConsistencyReason(row):
        """
        Return a bad consistency reason if there is one, otherwise return 0
        """
        zipcode, city, state, lat, lng = row["zip"], row["city"], row["state"], row["latitude"], row["longitude"]
        if not GeoConsistencyValidator.zipcodeInsideState(zipcode, state):
            return GeoConsistencyValidator.ZIPCODE_NOT_IN_STATE
        else:
            return 0

    @staticmethod
    def zipcodeInsideState(zipcode, state):
        inferredState = GeoConsistencyValidator.zipsearch.by_zipcode(zipcode).state
        if inferredState:
            abbr = us.states.lookup(state).abbr
            if abbr != inferredState:
                return False
            else:
                return True
        return False

    def filterToUsOnly(self):
        self.data["_detectedCC"] = self.data.apply(CountryDetector.detect, axis="columns")
        return self.data[self.data["_detectedCC"] == CountryDetector.US_COUNTRY_CODE]