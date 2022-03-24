"""Stationary combustion models"""
# pylint: disable=no-name-in-module
import logging
from atomic6ghg.formulas import Formula

from atomic6ghg.factors import heat_content_factors, stationary_combustion_emission_factors, refrigerants_gwp_factors

logger = logging.getLogger(__name__)


class StationaryCombustion(Formula):
    """ Stationary combustion includes fuels that are burned at stationary facilities. """

    fossil_fuels = ['anthraciteCoal', 'bituminousCoal', 'subBituminousCoal', 'ligniteCoal', 'naturalGas',
                    'distillateFuelOilNo2', 'residualFuelOilNo6', 'kerosene', 'liquefiedPetroleumGases']
    non_fossil_fuels = ['woodAndWoodResiduals', 'landfillGas']
    all_fuels = fossil_fuels + non_fossil_fuels

    common_units = {'anthraciteCoal': 'shortTon', 'bituminousCoal': 'shortTon',
                    'distillateFuelOilNo2': 'gallons', 'kerosene': 'gallons', 'landfillGas': 'scf',
                    'ligniteCoal': 'shortTon', 'liquefiedPetroleumGases': 'gallons', 'naturalGas': 'scf',
                    'residualFuelOilNo6': 'gallons', 'subBituminousCoal': 'shortTon',
                    'woodAndWoodResiduals': 'shortTon'}

    def __init__(self, wks_data=None):
        super().__init__(wks_data=wks_data)
        self.recalc(self.wks_data)

    def recalc(self, wks_data: dict) -> dict:
        """Execute recalc procedure for StationaryCombustion"""
        self.wks_data = wks_data

        self.make_total_combustion()
        self.make_emissions()
        self.make_co2_equivalent_emissions()
        self.make_biomass_co2_equivalent_emissions()

        # Add user data to _output
        self._output['stationarySourceFuelConsumption'] = self.wks_data.get('stationarySourceFuelConsumption', [])

        return self.to_dict()

    def make_total_combustion(self):
        """Calculate total combustion for all input rows"""
        total_combustion = {fuel: 0. for fuel in self.all_fuels}
        for row in self.wks_data.get('stationarySourceFuelConsumption', []):
            fuel = row['fuelCombusted']
            quantity_combusted = row['quantityCombusted']
            units = row['units']
            if not fuel or not quantity_combusted or not units:
                continue
            total_combustion[fuel] += heat_content_factors[fuel][units] * quantity_combusted

        # Flattening the dictionary
        total_combustion = [{'fuelType': fuel, 'quantityCombusted': quantity_combusted,
                             'units': self.common_units[fuel]} for fuel, quantity_combusted in total_combustion.items()]

        self._output['totalStationarySourceCombustion'] = total_combustion

    def make_emissions(self):
        """Calculate emissions for all fuels burned"""
        emissions = {fuel: {'CO2': 0., 'CH4': 0., 'N2O': 0.} for fuel in self.all_fuels}
        emissions['totalFossilFuelEmissions'] = {'CO2': 0., 'CH4': 0., 'N2O': 0.}
        emissions['totalNonFossilFuelEmissions'] = {'CO2': 0., 'CH4': 0., 'N2O': 0.}

        for row in self._output['totalStationarySourceCombustion']:
            fuel = row['fuelType']
            total_fuel_combustion = row['quantityCombusted']
            if not total_fuel_combustion:
                continue
            emissions[fuel]['CO2'] = StationaryCombustion.calculate_co2_emissions(fuel, total_fuel_combustion)
            emissions[fuel]['CH4'] = StationaryCombustion.calculate_ch4_emissions(fuel, total_fuel_combustion)
            emissions[fuel]['N2O'] = StationaryCombustion.calculate_n2o_emissions(fuel, total_fuel_combustion)

            # There should not be any fuels not in either list at this point
            if fuel in self.fossil_fuels:
                key = 'totalFossilFuelEmissions'
            else:
                key = 'totalNonFossilFuelEmissions'
            emissions[key]['CO2'] += emissions[fuel]['CO2']
            emissions[key]['CH4'] += emissions[fuel]['CH4']
            emissions[key]['N2O'] += emissions[fuel]['N2O']

        emissions['totalEmissionsForAllFuels'] = {gas: emissions['totalFossilFuelEmissions'][gas] +
                                                       emissions['totalNonFossilFuelEmissions'][gas]
                                                  for gas in emissions['totalFossilFuelEmissions']}

        self._total_emissions = {'totalFossilFuelEmissions': emissions['totalFossilFuelEmissions'],
                                 'totalNonFossilFuelEmissions': emissions['totalNonFossilFuelEmissions'],
                                 'totalEmissionsForAllFuels': emissions['totalEmissionsForAllFuels'],
                                 }

        # Flattening the dictionary
        emissions = [{'fuelType': fuel, **emissions[fuel]} for fuel in emissions]
        self._output['totalGhgEmissionsFromStationarySourceFuelCombustion'] = emissions

    @staticmethod
    def calculate_co2_emissions(fuel, total_fuel_combustion):
        """Calculate CO2 emissions for a fuel"""
        return stationary_combustion_emission_factors[fuel]['CO2 Factor (kg / Unit)'] * total_fuel_combustion

    @staticmethod
    def calculate_ch4_emissions(fuel, total_fuel_combustion):
        """Calculate CH4 emissions for a fuel"""
        return stationary_combustion_emission_factors[fuel]['CH4 Factor (g / unit)'] * total_fuel_combustion

    @staticmethod
    def calculate_n2o_emissions(fuel, total_fuel_combustion):
        """Calculate N2O emissions for a fuel"""
        return stationary_combustion_emission_factors[fuel]['N2O Factor (g / unit)'] * total_fuel_combustion

    def make_co2_equivalent_emissions(self):
        """ Calculate co2 equivalent emissions """
        # Units of CH4 and N2O emissions are in grams and need to be converted to kilograms
        conversions = {'CO2': 1., 'CH4': 1 / 1000., 'N2O': 1 / 1000.}
        total_fossil = sum([self._total_emissions['totalFossilFuelEmissions'][gas] *
                            refrigerants_gwp_factors[gas.lower()] * conversions[gas]
                            for gas in self._total_emissions['totalFossilFuelEmissions']])
        total_nonfossil = sum([self._total_emissions['totalNonFossilFuelEmissions'][gas] *
                               refrigerants_gwp_factors[gas.lower()] * conversions[gas]
                               for gas in self._total_emissions['totalNonFossilFuelEmissions'] if gas != 'CO2'])
        total = (total_fossil + total_nonfossil) / 1000.

        self._output['totalCo2EquivalentEmissions'] = total

    def make_biomass_co2_equivalent_emissions(self):
        """Calculate non-fossil-fuel emissions"""
        total = self._total_emissions['totalNonFossilFuelEmissions']['CO2'] / 1000.

        self._output['totalBiomassEquivalentEmissions'] = total
