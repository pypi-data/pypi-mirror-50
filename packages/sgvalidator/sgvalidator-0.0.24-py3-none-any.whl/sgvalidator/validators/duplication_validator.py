import termcolor

from .abstract_validator import AbstractValidator
from .validator_utils import ValidatorUtils


class DuplicationValidator(AbstractValidator):
    def __init__(self, data, debug):
        self.data = data
        self.debug = debug
        self.identityKeys = ["location_name", "street_address", "city", "state", "zip", "country_code", "location_type"]
        self.latLngKeys = ["latitude", "longitude"]

    def announce(self):
        print(termcolor.colored("Checking for duplication issues...", "blue"))

    def validate(self):
        self.validateIdentityDuplicates()
        self.validateLatLngsWithMultipleAddresses()
        self.warnIfSameAddrHasMultipleLatLngs()

    def validateLatLngsWithMultipleAddresses(self):
        """
        This check will work slightly differently than checkForIdentityDuplicates because we don't want to drop
        duplicates here. The reason is because you might have a case where 2 POI share an address but have a different
        lat/lng (e.g. for a walmart and a walmart pharmarcy), in which case dropping duplicates will give you different
        results based on which of the duplicates you keep in your result set.

        So, a better strategy here is to group by <lat, lng> and see how many difference addresses belong to each
        one. If the number greater than 1, something is wrong.
        """
        resUnfiltered = self.data.groupby(self.latLngKeys)["street_address"].apply(set).reset_index()
        resUnfiltered["num_addrs"] = resUnfiltered["street_address"].apply(len)
        blankMask = resUnfiltered["latitude"].apply(ValidatorUtils.is_not_blank) & resUnfiltered["longitude"]\
            .apply(ValidatorUtils.is_not_blank)
        res = resUnfiltered[blankMask & (resUnfiltered["num_addrs"] > 1)].sort_values("num_addrs", ascending=False)
        if len(res) > 0:
            ValidatorUtils.fail("Found {} <lat, lng> pair(s) that belong to multiple addresses. Examples:\n{}\n"
                                .format(len(res), res.head(10)), self.debug)
        return res

    def validateIdentityDuplicates(self):
        duplicateRows = self.getDuplicateRows(self.data, self.identityKeys)
        debugExamples = duplicateRows[self.identityKeys].head(10)
        if len(duplicateRows) > 0:
            ValidatorUtils.fail("Found {} duplicate rows in data. Examples:\n{}\n"
                                .format(len(duplicateRows), debugExamples), self.debug)
        return duplicateRows

    @staticmethod
    def getDuplicateRows(df, keys):
        return df[df.duplicated(subset=keys)]

    def warnIfSameAddrHasMultipleLatLngs(self):
        """
        nunique() only counts by lat/lng separately. So if the same address has 2 lats but only 1
        lng, that will get flagged here.
        """
        resUnfiltered = self.data.groupby(["street_address"])[self.latLngKeys].nunique().reset_index()
        res = resUnfiltered[(resUnfiltered["latitude"] > 1) | (resUnfiltered["longitude"] > 1)] \
            .sort_values("latitude", ascending=False) \
            .rename({"latitude": "same_lat_count", "longitude": "same_lng_count"}, axis="columns")
        if len(res) > 0:
            message = "WARNING: We found {} cases where a single address has multiple <lat, lngs>. Are you sure you" \
                      " scraped correctly? Examples:\n{}\n".format(len(res), res.head(10))
            print(termcolor.colored(message, "yellow"))
        return res
