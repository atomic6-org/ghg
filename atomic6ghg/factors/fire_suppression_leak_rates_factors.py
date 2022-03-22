""" Module to wrap factors in class """
import json
import pkgutil


class FireSuppressionFactors:
    """ Wrapper class for fire_suppression_leak_rate_factors.json """
    def __init__(self):
        self.factors = json.loads(pkgutil.get_data('atomic6ghg.factors',
            'source_data/fire_suppression_leak_rates_factors.json'))

    def __getitem__(self, item):
        return self.factors.get(item)
