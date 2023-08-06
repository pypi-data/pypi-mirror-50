from unittest import TestCase
from ..validators.validator_status import ValidatorStatus
import pandas as pd

from ..validators import DuplicationValidator
from .test_data import getFakeData

data = pd.DataFrame(getFakeData())
debugChecker = DuplicationValidator(data, debug=True)


class TestDuplicationChecker(TestCase):
    def testCheckIdentityDuplication(self):
        self.assertTrue(len(debugChecker.validateIdentityDuplicates() == 3))

    def testCheckLatLngDuplication(self):
        self.assertTrue(len(debugChecker.validateLatLngsWithMultipleAddresses() == 1))
        self.assertTrue(ValidatorStatus.FAIL == debugChecker.validate())

    def testWarnIfSameAddrHasMultipleLatLngs(self):
        res = debugChecker.warnIfSameAddrHasMultipleLatLngs()
        self.assertTrue(len(res) == 2)
