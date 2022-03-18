""" init """
from .heat_content_factors import HeatContentFactors
from .stationary_combustion_emission_factors import StationaryCombustionEmissionFactors
from .refrigerants_gwp_factors import RefrigerantsGwpFactors
from .unit_conversions_factors import UnitConversionsFactors
from .molecular_weights_factors import MolecularWeightsFactors
from .electricity_emission_factors import ElectricityFactors
from .refrigerants_gwp_factors import RefrigerantsGwpFactors

heat_content_factors = HeatContentFactors()
stationary_combustion_emission_factors = StationaryCombustionEmissionFactors()
refrigerants_gwp_factors = RefrigerantsGwpFactors()
unit_conversions_factors = UnitConversionsFactors()
molecular_weights_factors = MolecularWeightsFactors()
electricity_emission_factors = ElectricityFactors()
refrigerants_gwp_factors = RefrigerantsGwpFactors()

