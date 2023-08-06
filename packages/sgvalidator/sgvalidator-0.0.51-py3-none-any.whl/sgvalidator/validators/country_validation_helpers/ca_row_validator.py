from .country_detector import CountryDetector
from ..validator_utils import ValidatorUtils
from .abstract_country_validator import AbstractCountryValidator
from ..validator_status import ValidatorStatus


class CaRowValidator(AbstractCountryValidator):
    def __init__(self):
        pass

    def validate(self, row):
        res1 = self.validateZip(row)
        res2 = self.validateState(row)
        res3 = self.validatePhone(row)
        if res1 == ValidatorStatus.FAIL or res2 == ValidatorStatus.FAIL or res3 == ValidatorStatus.FAIL:
            return ValidatorStatus.FAIL
        return ValidatorStatus.SUCCESS

    def validateState(self, row):
        state = row["state"]
        if not ValidatorUtils.is_blank(state) and not CountryDetector.isCaState(state):
            ValidatorUtils.fail("Invalid Canadian province/territory: {}".format(state))
            return ValidatorStatus.FAIL
        return ValidatorStatus.SUCCESS

    def validatePhone(self, row):
        phone = row["phone"]
        if not ValidatorUtils.is_blank(phone) and not ValidatorUtils.is_valid_phone_number(phone, "CA"):
            ValidatorUtils.fail("Invalid Canadian phone number: {}".format(phone))
            return ValidatorStatus.FAIL
        return ValidatorStatus.SUCCESS

    def validateZip(self, row):
        zip_code = row["zip"]
        if not ValidatorUtils.is_blank(zip_code) and not CountryDetector.isCaZip(zip_code):
            ValidatorUtils.fail("Invalid Canadian postal code: {}".format(zip_code))
            return ValidatorStatus.FAIL
        return ValidatorStatus.SUCCESS
