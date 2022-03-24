""" Steam models """
# pylint: disable=no-name-in-module
import logging

from atomic6ghg.formulas import Formula
from atomic6ghg.factors import stationary_combustion_emission_factors, refrigerants_gwp_factors

logger = logging.getLogger(__name__)


class Steam(Formula):
    """ Calculate emissions from purchased gases """

    fuel_types = ['anthraciteCoal', 'bituminousCoal', 'coalCoke', 'distillateFuelOilNo2', 'kerosene', 'landfillGas',
                  'ligniteCoal', 'liquefiedPetroleumGases', 'mixedElectricPowerSector', 'naturalGas',
                  'residualFuelOilNo6', 'subBituminousCoal', 'woodAndWoodResiduals']
    default_boiler_efficiency_frac = 0.8

    def __init__(self, wks_data=None):
        super().__init__(wks_data=wks_data)
        self._total_emissions_by_fuel_type = {}
        self.recalc(self.wks_data)

    def recalc(self, wks_data: dict) -> dict:
        """Execute recalc procedure for Steam"""
        self.wks_data = wks_data

        self.make_emission_factor_data_for_steam_purchased()
        self.make_emissions_by_source_and_fuel_type()
        self.make_co2_equivalent_emissions_location_based()
        self.make_co2_equivalent_emissions_market_based()

        return self.to_dict()

    # pylint: disable=too-many-locals
    def make_emission_factor_data_for_steam_purchased(self):
        """Calculate emissions for each user input fuel source (each row)"""
        self._total_emissions_by_fuel_type = {fuel_type: {'locationBasedCO2Emissions': 0.,
                                                          'locationBasedCH4Emissions': 0.,
                                                          'locationBasedN2OEmissions': 0.,
                                                          'marketBasedCO2Emissions': 0.,
                                                          'marketBasedCH4Emissions': 0.,
                                                          'marketBasedN2OEmissions': 0.}
                                              for fuel_type in self.fuel_types}
        emission_factor_data_for_steam_purchased = []

        for row in self.wks_data.get('emissionFactorDataForSteamPurchased', []):
            fuel_type = row['fuelType']
            steam_purchased = row['steamPurchased']
            if not fuel_type or not steam_purchased:
                emission_factor_data_for_steam_purchased.append(row)
                continue
            boiler_efficiency = row['boilerEfficiency']
            if boiler_efficiency:
                boiler_efficiency_frac = boiler_efficiency / 100.
            else:
                boiler_efficiency_frac = self.default_boiler_efficiency_frac

            location_based_emission_factors_co2 = row['locationBasedEmissionFactorsCO2Factor']
            location_based_emission_factors_ch4 = row['locationBasedEmissionFactorsCH4Factor']
            location_based_emission_factors_n2o = row['locationBasedEmissionFactorsN2OFactor']
            market_based_emission_factors_co2 = row['marketBasedEmissionFactorsCO2Factor']
            market_based_emission_factors_ch4 = row['marketBasedEmissionFactorsCH4Factor']
            market_based_emission_factors_n2o = row['marketBasedEmissionFactorsN2OFactor']

            location_based_emissions_co2_emissions = \
                Steam.calculate_location_based_emissions_steam(steam_purchased, fuel_type,
                    location_based_emission_factors_co2, boiler_efficiency_frac, 'co2')

            location_based_emissions_ch4_emissions = \
                Steam.calculate_location_based_emissions_steam(steam_purchased, fuel_type,
                    location_based_emission_factors_ch4, boiler_efficiency_frac, 'ch4')

            location_based_emissions_n2o_emissions = \
                Steam.calculate_location_based_emissions_steam(steam_purchased, fuel_type,
                    location_based_emission_factors_n2o, boiler_efficiency_frac, 'n2o')

            market_based_emissions_co2_emissions = \
                Steam.calculate_market_based_emissions_steam(steam_purchased, fuel_type,
                    location_based_emission_factors_co2, market_based_emission_factors_co2, boiler_efficiency_frac,
                    'co2')

            market_based_emissions_ch4_emissions = \
                Steam.calculate_market_based_emissions_steam(steam_purchased, fuel_type,
                    location_based_emission_factors_ch4, market_based_emission_factors_ch4, boiler_efficiency_frac,
                    'ch4')

            market_based_emissions_n2o_emissions = \
                Steam.calculate_market_based_emissions_steam(steam_purchased, fuel_type,
                    location_based_emission_factors_n2o, market_based_emission_factors_n2o, boiler_efficiency_frac,
                    'n2o')

            self._total_emissions_by_fuel_type[fuel_type]['locationBasedCO2Emissions'] += \
                location_based_emissions_co2_emissions
            self._total_emissions_by_fuel_type[fuel_type]['locationBasedCH4Emissions'] += \
                location_based_emissions_ch4_emissions
            self._total_emissions_by_fuel_type[fuel_type]['locationBasedN2OEmissions'] += \
                location_based_emissions_n2o_emissions
            self._total_emissions_by_fuel_type[fuel_type]['marketBasedCO2Emissions'] += \
                market_based_emissions_co2_emissions
            self._total_emissions_by_fuel_type[fuel_type]['marketBasedCH4Emissions'] += \
                market_based_emissions_ch4_emissions
            self._total_emissions_by_fuel_type[fuel_type]['marketBasedN2OEmissions'] += \
                market_based_emissions_n2o_emissions

            calculated_row = {'sourceId': row['sourceId'], 'sourceDescription': row['sourceDescription'],
                              'sourceArea': row['sourceArea'], 'fuelType': fuel_type,
                              'boilerEfficiency': boiler_efficiency, 'steamPurchased': steam_purchased,
                              'locationBasedEmissionFactorsCO2Factor': location_based_emission_factors_co2,
                              'locationBasedEmissionFactorsCH4Factor': location_based_emission_factors_ch4,
                              'locationBasedEmissionFactorsN2OFactor': location_based_emission_factors_n2o,
                              'locationBasedEmissionsCO2Emissions': location_based_emissions_co2_emissions,
                              'locationBasedEmissionsCH4Emissions': location_based_emissions_ch4_emissions,
                              'locationBasedEmissionsN2OEmissions': location_based_emissions_n2o_emissions,
                              'marketBasedEmissionFactorsCO2Factor': market_based_emission_factors_co2,
                              'marketBasedEmissionFactorsCH4Factor': market_based_emission_factors_ch4,
                              'marketBasedEmissionFactorsN2OFactor': market_based_emission_factors_n2o,
                              'marketBasedEmissionsCO2Emissions': market_based_emissions_co2_emissions,
                              'marketBasedEmissionsCH4Emissions': market_based_emissions_ch4_emissions,
                              'marketBasedEmissionsN2OEmissions': market_based_emissions_n2o_emissions}
            emission_factor_data_for_steam_purchased.append(calculated_row)

        self._output['emissionFactorDataForSteamPurchased'] = emission_factor_data_for_steam_purchased

    @staticmethod
    # pylint: disable=too-many-arguments
    def calculate_market_based_emissions_steam(purchased_amount, fuel_type, location_based_factor, market_based_factor,
                                               boiler_efficiency_frac, gas_emission):
        """ Calculate gas (CO2, CH4, N2O) emissions for a fuel using market based emissions factors """
        if market_based_factor:
            ret = purchased_amount * market_based_factor / boiler_efficiency_frac
            # Handle potential negative values
            ret = max(0., ret)
        else:
            ret = Steam.calculate_location_based_emissions_steam(purchased_amount, fuel_type, location_based_factor,
                boiler_efficiency_frac, gas_emission)

        return ret

    @staticmethod
    def calculate_location_based_emissions_steam(purchased_amount, fuel_type, location_based_factor,
                                                 boiler_efficiency_frac, gas_emission):
        """ Calculate gas (CO2, CH4, N2O) emissions for a fuel using location based emissions factors """
        gas_emission_map = {'co2': 'CO2 Factor (kg / mmBtu)', 'ch4': 'CH4 Factor (g / mmBtu)',
                            'n2o': 'N2O Factor (g / mmBtu)'}

        if not location_based_factor:
            location_based_factor = stationary_combustion_emission_factors[fuel_type][gas_emission_map[gas_emission]]

        ret = purchased_amount * location_based_factor / boiler_efficiency_frac

        # Handle potential negative values
        ret = max(0., ret)
        return ret

    def make_emissions_by_source_and_fuel_type(self):
        """ Construct emissions_by_source_and_fuel_type table """
        self._total_emissions = {'locationBasedCO2Emissions': 0., 'locationBasedCH4Emissions': 0.,
                                 'locationBasedN2OEmissions': 0., 'marketBasedCO2Emissions': 0.,
                                 'marketBasedCH4Emissions': 0., 'marketBasedN2OEmissions': 0.}
        emissions_by_source_and_fuel_type = []
        for fuel_type in self._total_emissions_by_fuel_type:
            for k in self._total_emissions_by_fuel_type[fuel_type]:
                self._total_emissions[k] += self._total_emissions_by_fuel_type[fuel_type][k]
            row = {'fuelType': fuel_type, **self._total_emissions_by_fuel_type[fuel_type]}
            emissions_by_source_and_fuel_type.append(row)
        total_row = {'fuelType': 'totalEmissions', **self._total_emissions}
        emissions_by_source_and_fuel_type.append(total_row)

        self._output['emissionsBySourceAndFuelType'] = emissions_by_source_and_fuel_type

    def make_co2_equivalent_emissions_location_based(self):
        """ Calculate location based co2 equivalent emissions """
        location_based_emissions_co2_emissions = self._total_emissions['locationBasedCO2Emissions']
        location_based_emissions_ch4_emissions = self._total_emissions['locationBasedCH4Emissions']
        location_based_emissions_n2o_emissions = self._total_emissions['locationBasedN2OEmissions']
        total = (location_based_emissions_co2_emissions +
                 (location_based_emissions_ch4_emissions * refrigerants_gwp_factors['ch4'] / 1000) +
                 (location_based_emissions_n2o_emissions * refrigerants_gwp_factors['n2o'] / 1000)) / 1000

        self._output['CO2EquivalentEmissionsLocationBasedElectricityEmissions'] = total

    def make_co2_equivalent_emissions_market_based(self):
        """ Calculate market based co2 equivalent emissions """
        market_based_emissions_co2_emissions = self._total_emissions['marketBasedCO2Emissions']
        market_based_emissions_ch4_emissions = self._total_emissions['marketBasedCH4Emissions']
        market_based_emissions_n2o_emissions = self._total_emissions['marketBasedN2OEmissions']
        total = (market_based_emissions_co2_emissions +
                 (market_based_emissions_ch4_emissions * refrigerants_gwp_factors['ch4'] / 1000) +
                 (market_based_emissions_n2o_emissions * refrigerants_gwp_factors['n2o'] / 1000)) / 1000

        self._output['CO2EquivalentEmissionsMarketBasedElectricityEmissions'] = total
