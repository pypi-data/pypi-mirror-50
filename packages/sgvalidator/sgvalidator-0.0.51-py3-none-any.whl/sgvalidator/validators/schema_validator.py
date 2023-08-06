from ..color_printer import ColorPrinter
from .abstract_validator import AbstractValidator
from .validator_utils import ValidatorUtils
from .validator_status import ValidatorStatus


class SchemaValidator(AbstractValidator):
    def __init__(self, data, rawData):
        self.data = data
        self.rawData = rawData
        self.requiredColumns = {"locator_domain", "location_name", "street_address", "city", "state", "zip",
                                "country_code", "store_number", "phone", "location_type", "latitude", "longitude",
                                "hours_of_operation"}

    def announce(self):
        ColorPrinter.printBlueBanner("Checking for schema issues...")

    def subvalidators(self):
        return [
            self.validateSchema
        ]

    def validateSchema(self):
        requiredColsNotInData = self.getRequiredColumnsThatArentInData()
        if len(requiredColsNotInData) > 0:
            ValidatorUtils.fail("Data does not contain the following required columns {}.\n"
                                "Failing because the remainder of the checks won't be able to complete.\n"
                                .format(requiredColsNotInData))
            exit(0)

        # todo - transition this to pandas
        for row in self.rawData:
            for column in row:
                if type(row[column]) not in [type(None), type(''), type(u''), type(0), type(0.0), type(True)]:
                    message = "row {} contains unexpected data type {}".format(row, type(row[column]))
                    ValidatorUtils.fail(message)
                    return ValidatorStatus.FAIL
        return ValidatorStatus.SUCCESS

    def getRequiredColumnsThatArentInData(self):
        return self.requiredColumns.difference(self.data.columns)
