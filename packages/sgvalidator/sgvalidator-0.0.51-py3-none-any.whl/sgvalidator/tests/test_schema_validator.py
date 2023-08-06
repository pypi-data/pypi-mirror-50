import pandas as pd
from unittest import TestCase
from .test_data import getFakeData
from ..validators import SchemaValidator
from .test_data import TestDataFactory
from ..validators.validator_status import ValidatorStatus

dataWithGoodHeader = TestDataFactory().defaultRowsToPandasDf([
    TestDataFactory().getDefaultRow(),
    TestDataFactory().getDefaultRow(),
    TestDataFactory().getDefaultRow(),
    TestDataFactory().getDefaultRow()
])


class TestSchemaValidator(TestCase):
    def testCheckSchema(self):
        goodData = getFakeData('sample_data_good_header.csv')
        badData = getFakeData('sample_data_bad_header.csv')

        checkerGood = SchemaValidator(dataWithGoodHeader, goodData)
        checkerGood.validate()

        checkerBad = SchemaValidator(pd.DataFrame(badData), badData)
        self.assertTrue(len(checkerGood.getRequiredColumnsThatArentInData()) == 0)
        self.assertTrue(checkerBad.getRequiredColumnsThatArentInData() == {"street_address", "state"})
        # self.assertTrue(ValidatorStatus.FAIL == checkerBad.validate())
