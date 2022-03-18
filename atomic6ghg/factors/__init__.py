""" init """
from .unit_conversions_factors import UnitConversionsFactors
from .molecular_weights_factors import MolecularWeightsFactors
from .electricity_emission_factors import ElectricityFactors
from .refrigerants_gwp_factors import RefrigerantsGwpFactors

unit_conversions_factors = UnitConversionsFactors()
molecular_weights_factors = MolecularWeightsFactors()
electricity_emission_factors = ElectricityFactors()
refrigerants_gwp_factors = RefrigerantsGwpFactors()

