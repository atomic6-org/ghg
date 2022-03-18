""" Module to wrap factors in class """
import json
import pkgutil


class UnitConversionsFactors:
    """ Wrapper class for unit_conversions_factors.json """
    def __init__(self):
        self.factors = json.loads(pkgutil.get_data('atomic6ghg.factors',
            'source_data/unit_conversions_factors.json'))

    def __getitem__(self, item):
        return self.factors.get(item)
