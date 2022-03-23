""" Module to wrap factors in class """
import json
import pkgutil


class MobileCombustionCo2EmissionFactors:
    """ Wrapper class for mobile_combustion_emission_factors.json """
    def __init__(self):
        self.factors = json.loads(pkgutil.get_data('atomic6ghg.factors',
            'source_data/mobile_combustion_co2_emission_factors.json'))

    def __getitem__(self, item):
        return self.factors.get(item)
