""" Module to wrap factors in class """
import json
import pkgutil


class StationaryCombustionEmissionFactors:
    """ Wrapper class for stationary_combustion_emission_factors.json """
    def __init__(self):
        self.factors = json.loads(pkgutil.get_data('atomic6ghg.factors',
            'source_data/stationary_combustion_emission_factors.json'))

    def __getitem__(self, item):
        return self.factors.get(item)
