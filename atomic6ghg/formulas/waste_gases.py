""" Waste Gases models """
# pylint: disable=no-name-in-module
import logging

from atomic6ghg.formulas import Formula, null_replacer
from atomic6ghg.factors import molecular_weights_factors, unit_conversions_factors

logger = logging.getLogger(__name__)


class WasteGases(Formula):
    """ Calculate emission from combustion of waste gases """

    default_gas_total_number_of_moles_per_unit_volume = 0.00255
    default_oxidation_factor = 100.

    def __init__(self, wks_data=None):
        super().__init__(wks_data=wks_data)
        self.gas_total_number_of_moles_per_unit_volume = None
        self.oxidation_factor = None
        self.recalc(self.wks_data)

    def recalc(self, wks_data):
        """ Execute recalc procedure for waste gases """
        self.wks_data = wks_data

        self.gas_total_number_of_moles_per_unit_volume = self.wks_data.get("gasTotalNumberOfMolesPerUnitVolume") \
            if self.wks_data.get("gasTotalNumberOfMolesPerUnitVolume") \
            else self.default_gas_total_number_of_moles_per_unit_volume
        self.oxidation_factor = self.wks_data.get("oxidationFactor") \
            if self.wks_data.get("oxidationFactor") else self.default_oxidation_factor

        self.make_emission_factor_for_gas_waste_stream()
        self.make_total_all_components()
        self.make_co2_equivalent_emissions()

        self._output["wasteStreamGasCombusted"] = self.wks_data['wasteStreamGasCombusted']
        self._output["gasTotalNumberOfMolesPerUnitVolume"] = self.gas_total_number_of_moles_per_unit_volume
        self._output["oxidationFactor"] = self.oxidation_factor

        return self.to_dict()

    def make_emission_factor_for_gas_waste_stream(self):
        """ Calculate emission for each inputs in factor for gases waste stream table """
        waste_gasses = []
        self._total_emissions = {'totalCarbonContent': 0., 'totalMoles': 0., 'totalMolarFraction': 0.}
        gas_total_number_of_moles_per_unit_volume = self.gas_total_number_of_moles_per_unit_volume
        for row in self.wks_data.get('emissionFactorForGasWasteStream', []):
            component = row.get('component')
            if not component:
                waste_gasses.append(row)
                continue

            molar_fraction = null_replacer(row['molarFraction'])
            if component != 'Other non-carbon':
                chemical_formula = molecular_weights_factors[component]['chemicalFormula']
                molecular_weight = molecular_weights_factors[component]['molecularWeight']
                percent_carbon = molecular_weights_factors[component]['percentCarbon']
            else:
                chemical_formula = None
                molecular_weight = 0
                percent_carbon = 0

            total_moles = WasteGases.calculate_total_moles(molar_fraction, gas_total_number_of_moles_per_unit_volume)
            carbon_content = WasteGases.calculate_carbon_content(total_moles, molecular_weight, percent_carbon)

            self._total_emissions['totalMoles'] += total_moles
            self._total_emissions['totalMolarFraction'] += molar_fraction
            self._total_emissions['totalCarbonContent'] += carbon_content

            calculated_row = {'component': component,
                              'chemicalFormula': chemical_formula,
                              'molarFraction': molar_fraction,
                              'totalMoles': total_moles,
                              'molecularWeight': molecular_weight,
                              'percentCarbon': percent_carbon,
                              'carbonContent': carbon_content
                              }
            waste_gasses.append(calculated_row)

        self._output['emissionFactorForGasWasteStream'] = waste_gasses

    def make_total_all_components(self):
        """ Make total row """
        total_all_components = {'molarFraction': self._total_emissions['totalMolarFraction'],
                                'totalMoles': self._total_emissions['totalMoles'],
                                'carbonContent': self._total_emissions['totalCarbonContent']
                                }

        self._output['totalForAllComponents'] = total_all_components

    @staticmethod
    def calculate_total_moles(molar_fraction, gas_total_number_of_moles_per_unit_volume):
        """ Calculates total moles for given component"""
        ret = molar_fraction / 100 * gas_total_number_of_moles_per_unit_volume
        ret = max(0., ret)
        return ret

    @staticmethod
    def calculate_carbon_content(total_moles, molecular_weight, percent_carbon):
        """Calculates carbon content for given component"""
        ret = total_moles * molecular_weight * percent_carbon
        ret = max(0., ret)
        return ret

    def make_co2_equivalent_emissions(self):
        """ Calculates co2 equivalent for all components """
        waste_stream_gas_combusted = self.wks_data.get('wasteStreamGasCombusted')
        if waste_stream_gas_combusted:
            total = self._total_emissions['totalCarbonContent'] * self.oxidation_factor / 100. \
                    * (44.0098 / 12.001) \
                    * waste_stream_gas_combusted * unit_conversions_factors['pounds']['kilogram'] \
                    / 1000.
        else:
            # TODO: Raise error in logging message
            total = 0.

        self._output['totalCo2EquivalentEmissions'] = total
