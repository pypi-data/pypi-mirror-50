import termcolor
from .validator_utils import ValidatorUtils
from .abstract_validator import AbstractValidator
from ..color_printer import ColorPrinter


class StoreNumberColumnValidator(AbstractValidator):
    def __init__(self, data, debug):
        self.data = data
        self.debug = debug
        self.series = self.data["store_number"]
        self.storeNumberKey = "store_number"
        self.storeNumberKeyList = [self.storeNumberKey]
        self.storeNumberData = self.data[self.storeNumberKeyList]

    def announce(self):
        ColorPrinter.printBlueBanner("Validating store number column...")

    def validate(self):
        if self.isColumnPartiallyFilled():
            message = "Store number column is only partially filled."
            ValidatorUtils.fail(message, self.debug)
        elif not self.isColumnTotallyBlank():
            duplicateStoreNumbers = self.getDuplicateStoreNumbers()
            if len(duplicateStoreNumbers) > 0:
                debugExamples = duplicateStoreNumbers.head(5)
                message = "Store number column contains duplicate store numbers. Examples:\n{}\n".format(debugExamples)
                ValidatorUtils.fail(message, self.debug)

    @staticmethod
    def countNumBlanks(series):
        return series.apply(ValidatorUtils.is_blank).sum()

    def isColumnTotallyBlank(self):
        return self.countNumBlanks(self.series) == len(self.series)

    def isColumnPartiallyFilled(self):
        return 0 < self.countNumBlanks(self.series) < len(self.series)

    def getDuplicateStoreNumbers(self):
        duplicateRows = self.getDuplicateRows(self.data, self.storeNumberKeyList)
        return duplicateRows[self.storeNumberKeyList]

    @staticmethod
    def getDuplicateRows(df, keys):
        return df[df.duplicated(subset=keys)]
