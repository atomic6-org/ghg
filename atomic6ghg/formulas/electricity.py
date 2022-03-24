""" Electricity models """
# pylint: disable=no-name-in-module
import logging

from atomic6ghg.formulas import Formula
from atomic6ghg.factors import electricity_emission_factors, unit_conversions_factors, refrigerants_gwp_factors

logger = logging.getLogger(__name__)


class Electricity(Formula):
    """ Calculate emissions from purchased gases """

    subregions = ['akgd', 'akms', 'aznm', 'camx', 'erct', 'frcc', 'hims',
                  'hioa', 'mroe', 'mrow', 'newe', 'nwpp', 'nycw', 'nyli',
                  'nyup', 'prms', 'rfce', 'rfcm', 'rfcw', 'rmpa', 'spno',
                  'spso', 'srmv', 'srmw', 'srso', 'srtv', 'srvc']

    def __init__(self, wks_data=None):
        super().__init__(wks_data=wks_data)
        self.recalc(self.wks_data)

    def recalc(self, wks_data: dict) -> dict:
        """Execute recalc procedure for Electricity"""
        self.wks_data = wks_data

        self.make_emissions()
        self.make_total_emissions_for_all_sources()
        self.make_co2_equivalent_emissions_location_based()
        self.make_co2_equivalent_emissions_market_based()

        return self.to_dict()

    def make_emissions(self):
        """Calculate emissions for all fuels burned"""
        self._total_emissions = {'electricityPurchased': 0.,
                                 'marketBasedEmissionsCO2Emissions': 0.,
                                 'marketBasedEmissionsCH4Emissions': 0.,
                                 'marketBasedEmissionsN2OEmissions': 0.,
                                 'locationBasedEmissionsCO2Emissions': 0.,
                                 'locationBasedEmissionsCH4Emissions': 0.,
                                 'locationBasedEmissionsN2OEmissions': 0.}
        emissions = []

        for row in self.wks_data.get('totalElectricityPurchased', []):
            subregion = row['eGridSubregion']
            source_id = row.get('sourceId')
            if not subregion:
                emissions.append(row)
                continue

            electricity_purchased = row['electricityPurchased']
            market_based_emissions_factor_co2 = row["marketBasedEmissionFactorsCO2Emissions"]
            market_based_emissions_factor_ch4 = row["marketBasedEmissionFactorsCH4Emissions"]
            market_based_emissions_factor_n2o = row["marketBasedEmissionFactorsN2OEmissions"]

            market_based_emissions_co2_emissions = \
                Electricity.calculate_market_based_emissions_electricity(electricity_purchased,
                                                                         market_based_emissions_factor_co2,
                                                                         subregion,
                                                                         'co2')
            market_based_emissions_ch4_emissions = \
                Electricity.calculate_market_based_emissions_electricity(electricity_purchased,
                                                                         market_based_emissions_factor_ch4,
                                                                         subregion,
                                                                         'ch4')
            market_based_emissions_n2o_emissions = \
                Electricity.calculate_market_based_emissions_electricity(electricity_purchased,
                                                                         market_based_emissions_factor_n2o,
                                                                         subregion,
                                                                         'n2o')
            location_based_emissions_co2_emissions = \
                Electricity.calculate_location_based_emissions_electricity(electricity_purchased,
                                                                           subregion,
                                                                           'co2')
            location_based_emissions_ch4_emissions = \
                Electricity.calculate_location_based_emissions_electricity(electricity_purchased,
                                                                           subregion,
                                                                           'ch4')
            location_based_emissions_n2o_emissions = \
                Electricity.calculate_location_based_emissions_electricity(electricity_purchased,
                                                                           subregion,
                                                                           'n2o')

            self._total_emissions['electricityPurchased'] += electricity_purchased
            self._total_emissions['marketBasedEmissionsCO2Emissions'] += market_based_emissions_co2_emissions
            self._total_emissions['marketBasedEmissionsCH4Emissions'] += market_based_emissions_ch4_emissions
            self._total_emissions['marketBasedEmissionsN2OEmissions'] += market_based_emissions_n2o_emissions
            self._total_emissions['locationBasedEmissionsCO2Emissions'] += location_based_emissions_co2_emissions
            self._total_emissions['locationBasedEmissionsCH4Emissions'] += location_based_emissions_ch4_emissions
            self._total_emissions['locationBasedEmissionsN2OEmissions'] += location_based_emissions_n2o_emissions

            emissions.append({'sourceId': source_id, 'sourceDescription': row.get('sourceDescription'),
                              'sourceArea': row.get('sourceArea'), 'eGridSubregion': subregion,
                              'electricityPurchased': row['electricityPurchased'],
                              'marketBasedEmissionFactorsCO2Emissions': row['marketBasedEmissionFactorsCO2Emissions'],
                              'marketBasedEmissionFactorsCH4Emissions': row['marketBasedEmissionFactorsCH4Emissions'],
                              'marketBasedEmissionFactorsN2OEmissions': row['marketBasedEmissionFactorsN2OEmissions'],
                              'marketBasedEmissionsCO2Emissions': market_based_emissions_co2_emissions,
                              'marketBasedEmissionsCH4Emissions': market_based_emissions_ch4_emissions,
                              'marketBasedEmissionsN2OEmissions': market_based_emissions_n2o_emissions,
                              'locationBasedEmissionsCO2Emissions': location_based_emissions_co2_emissions,
                              'locationBasedEmissionsCH4Emissions': location_based_emissions_ch4_emissions,
                              'locationBasedEmissionsN2OEmissions': location_based_emissions_n2o_emissions})

        self._output['totalElectricityPurchased'] = emissions

    def make_total_emissions_for_all_sources(self):
        """ Make total row """
        total_emissions_for_all_sources = {
            'electricityPurchased': self._total_emissions['electricityPurchased'],
            'marketBasedEmissionsCO2Emissions': self._total_emissions['marketBasedEmissionsCO2Emissions'],
            'marketBasedEmissionsCH4Emissions': self._total_emissions['marketBasedEmissionsCH4Emissions'],
            'marketBasedEmissionsN2OEmissions': self._total_emissions['marketBasedEmissionsN2OEmissions'],
            'locationBasedEmissionsCO2Emissions': self._total_emissions['locationBasedEmissionsCO2Emissions'],
            'locationBasedEmissionsCH4Emissions': self._total_emissions['locationBasedEmissionsCH4Emissions'],
            'locationBasedEmissionsN2OEmissions': self._total_emissions['locationBasedEmissionsN2OEmissions']}

        self._output['totalEmissionsForAllSources'] = total_emissions_for_all_sources

    @staticmethod
    def calculate_market_based_emissions_electricity(purchased_amount, emissions_factor, subregion, fuel):
        """Calculate CO2 emissions for a gas given material balance inputs"""
        if emissions_factor:
            ret = (purchased_amount / 1000) * emissions_factor
        else:
            ret = Electricity.calculate_location_based_emissions_electricity(purchased_amount, subregion, fuel)
        # Handle potential negative values
        ret = max(0., ret)
        return ret

    @staticmethod
    def calculate_location_based_emissions_electricity(purchased_amount, subregion, fuel):
        """Calculate CO2 emissions for a gas given material balance inputs"""
        # print(subregion, electricity_emission_factors[subregion])
        if subregion:
            ret = (purchased_amount/1000) * (electricity_emission_factors[subregion][fuel])
        else:
            ret = 0
        # Handle potential negative values
        ret = max(0., ret)
        return ret

    def make_co2_equivalent_emissions_location_based(self):
        """Calculate co2 equivalent emissions """
        location_based_emissions_co2_emissions = self._total_emissions['locationBasedEmissionsCO2Emissions']
        location_based_emissions_ch4_emissions = self._total_emissions['locationBasedEmissionsCH4Emissions']
        location_based_emissions_n2o_emissions = self._total_emissions['locationBasedEmissionsN2OEmissions']
        total = ((location_based_emissions_co2_emissions +
                  (location_based_emissions_ch4_emissions * refrigerants_gwp_factors['ch4']) +
                  (location_based_emissions_n2o_emissions * refrigerants_gwp_factors['n2o'])) *
                 unit_conversions_factors['pounds']['kilogram']) / 1000

        self._output['CO2EquivalentEmissionsLocationBasedElectricityEmissions'] = total

    def make_co2_equivalent_emissions_market_based(self):
        """Calculate co2 equivalent emissions """
        market_based_emissions_co2_emissions = self._total_emissions['marketBasedEmissionsCO2Emissions']
        market_based_emissions_ch4_emissions = self._total_emissions['marketBasedEmissionsCH4Emissions']
        market_based_emissions_n2o_emissions = self._total_emissions['marketBasedEmissionsN2OEmissions']
        total = ((market_based_emissions_co2_emissions +
                  (market_based_emissions_ch4_emissions * refrigerants_gwp_factors['ch4']) +
                  (market_based_emissions_n2o_emissions * refrigerants_gwp_factors['n2o'])) *
                 unit_conversions_factors['pounds']['kilogram']) / 1000

        self._output['CO2EquivalentEmissionsMarketBasedElectricityEmissions'] = total
