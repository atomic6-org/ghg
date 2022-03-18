""" Module to wrap factors in class """
import json
import pkgutil


class RefrigerantsGwpFactors:
    """ Wrapper class for heat_content_factors.json """
    def __init__(self):
        self.factors = json.loads(pkgutil.get_data('atomic6ghg.factors',
            'source_data/refrigerants_gwp_factors.json'))

    def __getitem__(self, item):
        return self.factors.get(item)
