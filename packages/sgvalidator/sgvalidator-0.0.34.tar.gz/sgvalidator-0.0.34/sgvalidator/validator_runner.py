import pandas as pd
from .validators.centroid_validator import CentroidValidator
from .validators.country_validator import CountryValidator
from .validators.duplication_validator import DuplicationValidator
from .validators.fill_rate_validator import FillRateValidator
from .validators.schema_validator import SchemaValidator
from .validators.trash_value_validator import TrashValueValidator
from .validators.count_validator import CountValidator
from .validators.street_address_validator import StreetAddressValidator
from .validators.geo_consistency_validator import GeoConsistencyValidator
from .validators.store_number_column_validator import StoreNumberColumnValidator


class ValidatorRunner:
    def __init__(self, data, debug, classesToIgnore):
        self.rawData = data
        self.data = pd.DataFrame(data)
        self.classesToIgnore = classesToIgnore
        self.debug = debug
        self.validators = [
            # Schema and FillRate run first to catch anything that will break code later on
            SchemaValidator(self.data, self.rawData, self.debug),  # todo - move this off of raw data
            FillRateValidator(self.data, self.debug),
            DuplicationValidator(self.data, self.debug, classesToIgnore=classesToIgnore),
            CentroidValidator(self.data, self.debug, classesToIgnore=classesToIgnore),
            CountryValidator(self.data, self.debug),
            TrashValueValidator(self.data, self.debug),
            CountValidator(self.data, self.debug, classesToIgnore=classesToIgnore),
            StoreNumberColumnValidator(self.data, self.debug),
            StreetAddressValidator(self.data, self.debug),
            GeoConsistencyValidator(self.data, self.debug)
        ]

    def run(self):
        for validator in self.validators:
            validator.run()
