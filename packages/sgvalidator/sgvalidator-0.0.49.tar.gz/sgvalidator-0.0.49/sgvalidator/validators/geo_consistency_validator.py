import us
from uszipcode import SearchEngine
from .abstract_validator import AbstractValidator
from ..color_printer import ColorPrinter
from .validator_utils import ValidatorUtils
from .validator_decorators import ignorable
from .country_validation_helpers.country_detector import CountryDetector
from .validator_status import ValidatorStatus
from .dataframe_tagger import DataframeTagger


class GeoConsistencyValidator(AbstractValidator):
    zipsearch = SearchEngine(simple_zipcode=True)
    ZIPCODE_NOT_IN_STATE = "ZIPCODE_NOT_IN_STATE"

    def __init__(self, data, classesToIgnore=None):
        self.data = data.copy()
        self.classesToIgnore = classesToIgnore
        self.columnsToReturn = ["location_name", "street_address", "zip", "city", "state", "latitude", "longitude",
                                DataframeTagger.TAG_COLUMN_NAME]

    def announce(self):
        ColorPrinter.printBlueBanner("Validating consistency of geography columns...")

    def subvalidators(self):
        return [
            self.validateInconsistentGeoRows
        ]

    @ignorable
    def validateInconsistentGeoRows(self):
        inconsistentGeoRows = self.getInconsistentGeoRows()
        if len(inconsistentGeoRows) > 0:
            debugExamples = inconsistentGeoRows.head(5)
            message = "Found {} rows with inconsistent geographies. Look at the REASON column in the output below to " \
                      "see why these rows were flagged. Examples:\n{}\n".format(len(inconsistentGeoRows), debugExamples)
            ValidatorUtils.fail(message)
            return ValidatorStatus.FAIL
        return ValidatorStatus.SUCCESS

    def getInconsistentGeoRows(self):
        usData = self.filterToUsOnly()
        res = DataframeTagger.tagRows(usData, self.getBadGeoConsistencyReason)
        if res.empty:
            return res
        return res[self.columnsToReturn]

    @staticmethod
    def getBadGeoConsistencyReason(row):
        """
        Return a bad consistency reason if there is one, otherwise return 0
        """
        zipcode, city, state, lat, lng = row["zip"], row["city"], row["state"], row["latitude"], row["longitude"]
        if not GeoConsistencyValidator.zipcodeInsideState(zipcode, state):
            return GeoConsistencyValidator.ZIPCODE_NOT_IN_STATE
        return 0

    @staticmethod
    def zipcodeInsideState(zipcode, state):
        if ValidatorUtils.is_blank(zipcode):
            return True

        cleanedZipcode = GeoConsistencyValidator.cleanZip(zipcode)
        inferredState = GeoConsistencyValidator.zipsearch.by_zipcode(cleanedZipcode).state
        if inferredState:
            abbr = us.states.lookup(state.strip()).abbr
            if abbr != inferredState:
                return False
            else:
                return True
        return False

    @staticmethod
    def cleanZip(zipcode):
        stripped = zipcode.strip()
        if len(stripped) > 5:
            return stripped[:5]
        return stripped

    def filterToUsOnly(self):
        self.data["_detectedCC"] = self.data.apply(CountryDetector.detect, axis="columns")
        return self.data[self.data["_detectedCC"] == CountryDetector.US_COUNTRY_CODE]
