from ..color_printer import ColorPrinter
from .abstract_validator import AbstractValidator
from .validator_utils import ValidatorUtils
from .validator_status import ValidatorStatus

class FillRateValidator(AbstractValidator):
    """
    Checks the percentage of each columns which is null or blank and warns if it's greater than some cutoff.
    To add a new fill rate check, just define a boolean mask and pass to `checkFillRateInner`
    """
    PERC_CUTOFF = 40

    def __init__(self, data, classesToIgnore=None):
        self.data = data
        self.classesToIgnore = classesToIgnore
        self.colsThatNeedToBeTotallyFilled = ["location_name", "street_address", "zip", "city", "state"]

    def announce(self):
        ColorPrinter.printBlueBanner("Checking for fill rate issues...")

    def subvalidators(self):
        return [
            self.validateNullFillRate,
            self.validateBlankFillRate,
        ]

    def validateNullFillRate(self):
        percNullDf = self.data.isna().mean() * 100
        return self.validateInner(percNullDf, "null")

    def validateBlankFillRate(self):
        percBlankDf = self.data.astype(str).apply(lambda x: x == "", axis=0).mean() * 100
        return self.validateInner(percBlankDf, "blanks")

    def validateInner(self, mask, desc):
        colsWithAtLeastOneEmptyCell = FillRateValidator \
            .getConcerningColsWithPercentages(mask, 0.0)

        concerningColsWithPercentages = FillRateValidator\
            .getConcerningColsWithPercentages(mask, FillRateValidator.PERC_CUTOFF)

        for strictCol in self.colsThatNeedToBeTotallyFilled:
            if strictCol in colsWithAtLeastOneEmptyCell:
                message = "We expect {} column to be totally filled, but the column in your data is only " \
                         "partially filled.".format(strictCol)
                ValidatorUtils.fail(message)
                exit(0)  # fail here or else downstream checks will break

        if len(concerningColsWithPercentages) > 0:
            message = "WARNING: {} columns have a high percentage (> {}%) of {}. " \
                      "Are you sure you scraped correctly?\n{}\n"\
                .format(len(concerningColsWithPercentages), FillRateValidator.PERC_CUTOFF, desc,
                        concerningColsWithPercentages)
            ColorPrinter.printYellow(message)
            return ValidatorStatus.WARN
        return ValidatorStatus.SUCCESS

    @staticmethod
    def getConcerningColsWithPercentages(mask, percCutoff):
        return mask[mask > percCutoff]
