""" Waste models """
# pylint: disable=no-name-in-module
import logging

from atomic6ghg.formulas import Formula
from atomic6ghg.factors import waste_emission_factors, unit_conversions_factors

logger = logging.getLogger(__name__)


class Waste(Formula):
    """ Calculate emissions from waste materials """

    disposal_methods = ["recycled", "landfilled", "combusted", "composted", "anaerobicallyDigestedDry",
                       "anaerobicallyDigestedWet"]

    def __init__(self, wks_data=None):
        super().__init__(wks_data=wks_data)
        self.recalc(self.wks_data)

    def recalc(self, wks_data: dict) -> dict:
        """Execute recalc procedure for Waste"""
        self.wks_data = wks_data

        self.make_waste_disposal()
        self.make_total_emissions_by_disposal_method()
        self.make_co2_equivalent_emissions()

        return self.to_dict()

    def make_waste_disposal(self):
        """Calculate CO2 equivalent emissions for each input row"""
        waste_disposal = []
        self._total_emissions = {disposal_method: 0. for disposal_method in self.disposal_methods}
        for row in self.wks_data.get('wasteDisposal', []):
            waste_material = row['wasteMaterial']
            disposal_method = row['disposalMethod']
            weight = row['weight']
            unit = row['unit']
            if not waste_material or not disposal_method or not weight or not unit:
                waste_disposal.append(row)
                continue

            co2_emissions = Waste.calculate_co2_emissions(waste_material, disposal_method, weight, unit)

            self._total_emissions[disposal_method] += co2_emissions

            calculated_row = {'sourceId': row['sourceId'], 'sourceDescription': row['sourceDescription'],
                              'wasteMaterial': waste_material, 'disposalMethod': disposal_method, 'weight': weight,
                              'unit': unit, 'CO2Emissions': co2_emissions}
            waste_disposal.append(calculated_row)

        self._output['wasteDisposal'] = waste_disposal

    def make_total_emissions_by_disposal_method(self):
        """Calculate CO2 equivalent emissions for each input row"""
        total_emissions_by_disposal_method = [{'wasteMaterial': disposal_method, 'CO2': co2_emissions}
                                              for disposal_method, co2_emissions in self._total_emissions.items()]
        self._output['totalEmissionsByDisposalMethod'] = total_emissions_by_disposal_method

    @staticmethod
    def calculate_co2_emissions(waste_material, disposal_method, weight, unit):
        """Calculate CO2 emissions for a waste material given the disposal method weight and units"""
        ret = waste_emission_factors[waste_material][disposal_method] * \
              unit_conversions_factors[unit]['shortTon'] * weight * 1000
        # Handle potential negative values
        ret = max(0., ret)
        return ret

    def make_co2_equivalent_emissions(self):
        """ Calculate co2 equivalent emissions """
        total = sum(self._total_emissions.values()) / 1000

        self._output['totalCo2EquivalentEmissions'] = total
