from unittest import TestCase
from .test_data import TestDataFactory
from ..validators.validator_status import ValidatorStatus
from ..validators import StreetAddressValidator

dataWithBadAddresses = TestDataFactory().defaultRowsToPandasDf([
    TestDataFactory().getDefaultRow(),
    TestDataFactory().getDefaultRow(),
    TestDataFactory().getDefaultRow().copy(street_address="Mission St"),
    TestDataFactory().getDefaultRow().copy(street_address="Corner of 8th and Bryant")
])

dataWithGoodAddresses = TestDataFactory().defaultRowsToPandasDf([
    TestDataFactory().getDefaultRow(),
    TestDataFactory().getDefaultRow(),
    TestDataFactory().getDefaultRow().copy(street_address="1322 Mission St"),
    TestDataFactory().getDefaultRow().copy(street_address="70 Albion St")
])

streetAddressValidator = StreetAddressValidator(dataWithBadAddresses, debug=True)


class TestStreetAddressValidator(TestCase):
    def testDoesAddressHaveNumber(self):
        self.assertTrue(streetAddressValidator.doesAddressHaveKey("1543 Mission St", "AddressNumber"))
        self.assertTrue(streetAddressValidator.doesAddressHaveKey("101 Main St", "AddressNumber"))
        self.assertTrue(streetAddressValidator.doesAddressHaveKey("1372 Mission St", "AddressNumber"))
        self.assertTrue(streetAddressValidator.doesAddressHaveKey("18 Market St", "AddressNumber"))

        self.assertFalse(streetAddressValidator.doesAddressHaveKey("Mission St", "AddressNumber"))
        self.assertFalse(streetAddressValidator.doesAddressHaveKey("Corner of 8th and Bryant", "AddressNumber"))
        self.assertFalse(streetAddressValidator.doesAddressHaveKey("4th St", "AddressNumber"))

    def testGetAddressesWithNoNumber(self):
        res = streetAddressValidator.getAddressesWithNoNumber()
        self.assertTrue(len(res) == 2)

    def testValidate(self):
        StreetAddressValidator(dataWithGoodAddresses, debug=False).validate()
        self.assertTrue(ValidatorStatus.FAIL == streetAddressValidator.validate())
