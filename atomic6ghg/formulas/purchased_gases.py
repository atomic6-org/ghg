""" Purchased gases models """
# pylint: disable=no-name-in-module
import logging

from atomic6ghg.formulas import Formula, null_replacer
from atomic6ghg.factors import refrigerants_gwp_factors, unit_conversions_factors

logger = logging.getLogger(__name__)


class PurchasedGases(Formula):
    """ Calculate emissions from purchased gases """

    def __init__(self, wks_data=None):
        super().__init__(wks_data=wks_data)
        self.recalc(self.wks_data)

    def recalc(self, wks_data: dict) -> dict:
        """Execute recalc procedure for PurchasedGases"""
        self.wks_data = wks_data

        self.make_purchased_gases()
        self.make_co2_equivalent_emissions()

        return self.to_dict()

    def make_purchased_gases(self):
        """Calculate CO2 equivalent emissions for each input row"""
        purchased_gases = []
        self._total_emissions['purchasedGases'] = 0.
        for row in self.wks_data.get('purchasedGases', []):
            gas = row['gas']
            if not gas:
                purchased_gases.append(row)
                continue

            gwp = refrigerants_gwp_factors[gas]

            purchased_amount = null_replacer(row['purchasedAmount'])
            co2_equivalent_emissions = PurchasedGases.calculate_co2_emissions_purchased_gases(gwp,
                                                                                              purchased_amount)

            self._total_emissions['purchasedGases'] += co2_equivalent_emissions
            calculated_row = {'gas': gas, 'gasGWP': gwp, 'purchasedAmount': purchased_amount,
                              'co2EquivalentEmissions': co2_equivalent_emissions}
            purchased_gases.append(calculated_row)

        self._output['purchasedGases'] = purchased_gases


    @staticmethod
    def calculate_co2_emissions_purchased_gases(gwp, purchased_amount):
        """Calculate CO2 emissions for a gas given material balance inputs"""
        ret = gwp * purchased_amount
        # Handle potential negative values
        ret = max(0., ret)
        return ret


    def make_co2_equivalent_emissions(self):
        """ Calculate co2 equivalent emissions """
        total = (unit_conversions_factors['pounds']['kilogram'] * (self._total_emissions['purchasedGases'])) / 1000.

        self._output['totalCo2EquivalentEmissions'] = total
