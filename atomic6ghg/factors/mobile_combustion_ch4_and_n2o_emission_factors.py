""" Module to wrap factors in class """
import json
import pkgutil
from atomic6ghg import YearValueException, YearMapException

class MobileCombustionCh4AndN2oEmissionFactors:
    """ Wrapper class for mobile_combustion_emission_factors.json """
    def __init__(self):
        self.factors = json.loads(pkgutil.get_data('atomic6ghg.factors',
            'source_data/mobile_combustion_ch4_and_n2o_emission_factors.json'))

        self._factors = {}
        self.make_factors()

    def __getitem__(self, vehicle_type):
        return self._factors.get(vehicle_type)

    class YearHandler:
        """ Class to handle user input years to map the correct factors for a given vehicle type and fuel type """
        def __init__(self, factors_by_year):
            self.factors_by_year = {}
            self._rekey_years(factors_by_year)

            self.year_boundaries = []
            if len(self.factors_by_year) > 1:
                self.get_year_boundaries()

        def _rekey_years(self, factors_by_year):
            """ Turn string keys into integers """

            # Assume if length is one then the only key is ''
            if len(factors_by_year) == 1:
                self.factors_by_year = factors_by_year
            else:
                self.factors_by_year = {int(year): factor for year, factor in factors_by_year.items()}

        def get_year_boundaries(self):
            """ Get the minimum and maximum years that have factors """
            years = sorted([int(year) for year in self.factors_by_year])
            self.year_boundaries = [years[0], years[-1]]

        @staticmethod
        def _int_year(year):
            try:
                if isinstance(year, str):
                    assert year.isdigit()
                elif isinstance(year, float):
                    assert year.is_integer()
                else:
                    assert isinstance(year, int)
                return int(year)
            except AssertionError as e:
                raise YearValueException from e

        def __getitem__(self, year):
            # If there is only one key then the fuel type has no time dependency and has key 'default'.
            # This also ignores year, which the user can input and may be passed along to the factors.
            if len(self.factors_by_year) == 1:
                return self.factors_by_year['default']
            year = self._int_year(year)
            try:
                return self.factors_by_year[year]
            except KeyError:
                pass
            if year < self.year_boundaries[0]:
                ret = self[self.year_boundaries[0]]
            elif year > self.year_boundaries[1]:
                ret = self[self.year_boundaries[1]]
            else:
                raise YearMapException
            return ret

        def __repr__(self):
            return repr(self.factors_by_year)

        def __iter__(self):
            return iter(self.factors_by_year)

    def __repr__(self):
        return repr(self._factors)

    def __iter__(self):
        return iter(self._factors)

    def make_factors(self):
        """ Wrap year level of factors json in class YearHandler to handle user input for years of mobile vehicles"""
        for vehicle_type in self.factors:
            self._factors[vehicle_type] = {}
            for fuel_type in self.factors[vehicle_type]:
                self._factors[vehicle_type][fuel_type] = self.YearHandler(self.factors[vehicle_type][fuel_type])
