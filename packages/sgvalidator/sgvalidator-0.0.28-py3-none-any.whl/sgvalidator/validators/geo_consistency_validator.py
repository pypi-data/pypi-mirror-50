import us
from uszipcode import SearchEngine
from .abstract_validator import AbstractValidator
from ..color_printer import ColorPrinter
from .validator_utils import ValidatorUtils


class GeoConsistencyValidator(AbstractValidator):
    zipsearch = SearchEngine(simple_zipcode=True)
    ZIPCODE_NOT_IN_STATE = "ZIPCODE_NOT_IN_STATE"

    def __init__(self, data, debug):
        self.data = data.copy()
        self.debug = debug

    def announce(self):
        ColorPrinter.printBlue("Validating consistency of geography columns...")

    def validate(self):
        inconsistentGeoRows = self.getInconsistentGeoRows()
        if len(inconsistentGeoRows) > 0:
            debugExamples = inconsistentGeoRows.head(5)
            message = "Found {} rows with inconsistent geographies. Look at the REASON column in the output below to " \
                      "see why these rows were flagged. Examples:\n{}\n".format(len(inconsistentGeoRows), debugExamples)
            ValidatorUtils.fail(message, self.debug)

    def getInconsistentGeoRows(self):
        badGeoConsistencyReason = self.data.apply(self.getBadGeoConsistencyReason, axis=1)
        self.data["REASON"] = badGeoConsistencyReason
        dataToReturn = self.data[["location_name", "street_address", "zip", "city", "state", "latitude", "longitude",
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
