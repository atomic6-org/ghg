""" Mobile Sources models """
# pylint: disable=no-name-in-module
import logging

from atomic6ghg.formulas import Formula
from atomic6ghg.factors import mobile_combustion_co2_emission_factors, mobile_combustion_ch4_and_n2o_emission_factors, \
    refrigerants_gwp_factors
from atomic6ghg import YearMapException, YearValueException

logger = logging.getLogger(__name__)


class MobileSources(Formula):
    """ Calculate emissions from mobile source vehicles """

    co2_fuels_units = {'gasoline': 'gallons', 'diesel': 'gallons', 'residualFuelOil': 'gallons',
                       'aviationGasoline': 'gallons', 'jetFuel': 'gallons', 'lpg': 'gallons',
                       'ethanol': 'gallons', 'biodiesel': 'gallons', 'lng': 'gallons', 'cng': 'scf'}
    co2_fuel_map = {'gasoline2Stroke': 'gasoline', 'gasoline4Stroke': 'gasoline', 'methanol': 'ethanol'}
    non_biomass_co2_fuel_map = {'ethanol': 'gasoline', 'biodiesel': 'diesel'}
    road_vehicles = ['heavyDutyVehicles', 'lightDutyTrucks', 'motorcycles', 'passengerCars', 'buses', 'heavyDutyTrucks',
                     'lightDutyCars', 'mediumAndHeavyDutyVehicles', 'mediumDutyTrucks']
    nonroad_vehicles = ['agriculturalEquipment', 'agriculturalOffroadTrucks', 'aircraft', 'airportEquipment',
                        'constructionMiningEquipment', 'constructionMiningOffroadTrucks',
                        'industrialCommercialEquipment', 'lawnAndGardenEquipment', 'locomotives', 'loggingEquipment',
                        'railroadEquipment', 'recreationalEquipment', 'shipsAndBoats']

    def __init__(self, wks_data=None):
        super().__init__(wks_data=wks_data)

        self.biodiesel_percent = 20
        self.ethanol_percent = 80

        self.total_fuel_usage_and_co2_emissions = {}
        self.total_useage_and_ch4_and_n2o_emissions = {}

        self.recalc(self.wks_data)

    def recalc(self, wks_data: dict) -> dict:
        """ Execute recalc procedure for MobileSources """
        self.wks_data = wks_data

        self._total_emissions = {'CO2': 0., 'CH4': 0., 'N2O': 0.}

        self.total_fuel_usage_and_co2_emissions = {fuel_type: {'fuelUsage': 0, 'CO2': 0.}
                                                   for fuel_type in self.co2_fuels_units}

        self.total_useage_and_ch4_and_n2o_emissions = \
            {vehicle_type: {fuel_type: {
                mobile_combustion_ch4_and_n2o_emission_factors[vehicle_type][fuel_type][year]['year_display']:
                    {'N2O': 0., 'CH4': 0., 'mileage': 0., 'fuelUsage': 0.}
                for year in mobile_combustion_ch4_and_n2o_emission_factors[vehicle_type][fuel_type]}
                for fuel_type in mobile_combustion_ch4_and_n2o_emission_factors[vehicle_type]}
                for vehicle_type in mobile_combustion_ch4_and_n2o_emission_factors
            }

        # If these keys aren't in wks_data then default to original wks_data values
        self.biodiesel_percent = self.wks_data.get('biodieselPercent', 20)
        self.ethanol_percent = self.wks_data.get('ethanolPercent', 80)

        self.tabulate_subtable_data()

        self.make_total_mobile_sources_fuel_usage_and_co2_emissions()
        self.make_total_organization_wide_on_road_gasoline_mobile_source_mileage_and_emissions()
        self.make_total_organization_wide_on_road_non_gasoline_mobile_source_mileage_and_emissions()
        self.make_total_organization_wide_non_road_mobile_source_fuel_usage_and_emissions()
        self.make_total_co2_equivalent_emissions()
        self.make_total_biomass_co2_equivalent_emissions()

        # Add user data to _output
        self._output['mobileSourcesFuelConsumption'] = self.wks_data.get('mobileSourcesFuelConsumption', [])
        self._output['biodieselPercent'] = self.biodiesel_percent
        self._output['ethanolPercent'] = self.ethanol_percent

        return self.to_dict()

    def tabulate_subtable_data(self):
        """ Loop over user input data and make all sub-tables. """

        for row in self.wks_data.get('mobileSourcesFuelConsumption', []):
            vehicle_type = row['vehicleType']
            fuel_usage = row['fuelUsage']
            miles_traveled = row['milesTraveled']
            fuel_type = row['fuelType']
            vehicle_year = row['vehicleYear']
            if not fuel_type:
                continue
            if fuel_usage:
                self.tabulate_total_mobile_sources_fuel_usage_and_co2_emissions(fuel_type, fuel_usage)
            if vehicle_type:
                self.tabulate_mobile_source_use_and_emissions_by_vehicle_type(vehicle_type, fuel_type, vehicle_year,
                    fuel_usage, miles_traveled)

    def tabulate_total_mobile_sources_fuel_usage_and_co2_emissions(self, fuel_type, fuel_usage):
        """Calculate CO2 equivalent emissions for each input fuel_type and fuel_usage"""

        co2_fuel_type = self.co2_fuel_map.get(fuel_type, fuel_type)
        co2_fuel_usage = self.get_fuel_usage(co2_fuel_type, fuel_usage)
        non_biomass_co2_fuel_type = self.non_biomass_co2_fuel_map.get(co2_fuel_type, co2_fuel_type)

        co2_equivalent_emissions = MobileSources.calculate_co2_emissions(non_biomass_co2_fuel_type, co2_fuel_usage)

        self.total_fuel_usage_and_co2_emissions[co2_fuel_type]['fuelUsage'] += fuel_usage
        self.total_fuel_usage_and_co2_emissions[co2_fuel_type]['CO2'] += co2_equivalent_emissions

        self._total_emissions['CO2'] += co2_equivalent_emissions

    def get_fuel_usage(self, fuel_type, fuel_usage):
        """ Get non biomass fuel usage for each fuel type """
        if fuel_type == 'ethanol':
            ret = fuel_usage * ((100 - self.ethanol_percent) / 100)
        elif fuel_type == 'biodiesel':
            ret = fuel_usage * ((100 - self.biodiesel_percent) / 100)
        else:
            ret = fuel_usage
        return ret

    # pylint: disable=too-many-arguments
    def tabulate_mobile_source_use_and_emissions_by_vehicle_type(self, vehicle_type, fuel_type, vehicle_year,
                                                                 fuel_usage, miles_traveled):
        """ Calculate total fuel usage, total mileage, and CH4 and N2O emissions for vehicles """

        if vehicle_type in self.road_vehicles:
            usage = miles_traveled
        else:
            usage = fuel_usage

        try:
            ch4_emissions = MobileSources.calculate_ch4_emissions(vehicle_type, fuel_type, usage, vehicle_year)
        except (YearMapException, YearValueException) as e:
            logger.error(e)
            ch4_emissions = 0.

        try:
            n2o_emissions = MobileSources.calculate_n2o_emissions(vehicle_type, fuel_type, usage, vehicle_year)
        except (YearMapException, YearValueException) as e:
            logger.error(e)
            n2o_emissions = 0.

        year_display = \
            mobile_combustion_ch4_and_n2o_emission_factors[vehicle_type][fuel_type][vehicle_year]['year_display']
        self.total_useage_and_ch4_and_n2o_emissions[vehicle_type][fuel_type][year_display]['CH4'] += ch4_emissions
        self.total_useage_and_ch4_and_n2o_emissions[vehicle_type][fuel_type][year_display]['N2O'] += n2o_emissions
        self.total_useage_and_ch4_and_n2o_emissions[vehicle_type][fuel_type][year_display]['mileage'] += miles_traveled
        self.total_useage_and_ch4_and_n2o_emissions[vehicle_type][fuel_type][year_display]['fuelUsage'] += fuel_usage

        self._total_emissions['CH4'] += ch4_emissions
        self._total_emissions['N2O'] += n2o_emissions

    def make_total_mobile_sources_fuel_usage_and_co2_emissions(self):
        """ Format total_fuel_usage_and_co2_emissions data for schema """
        total_fuel_usage_and_co2_emissions = \
            [{'fuelType': fuel_type,
              'fuelUsage': self.total_fuel_usage_and_co2_emissions[fuel_type]['fuelUsage'],
              'units': self.co2_fuels_units[fuel_type],
              'CO2': self.total_fuel_usage_and_co2_emissions[fuel_type]['CO2']}
             for fuel_type in self.total_fuel_usage_and_co2_emissions]

        self._output['totalMobileSourcesFuelUsageAndCO2Emissions'] = total_fuel_usage_and_co2_emissions

    def make_total_organization_wide_on_road_gasoline_mobile_source_mileage_and_emissions(self):
        """ Select gasoline on road vehicle data and format total_useage_and_ch4_and_n2o_emissions for schema """

        total_on_road_gasoline_mileage_and_emissions = \
            [{'vehicleType': vehicle_type,
              'emissionByYear': [
                  {'vehicleYear': year,
                   'mileage': self.total_useage_and_ch4_and_n2o_emissions[vehicle_type][fuel_type][year]['mileage'],
                   'CH4': self.total_useage_and_ch4_and_n2o_emissions[vehicle_type][fuel_type][year]['CH4'],
                   'N2O': self.total_useage_and_ch4_and_n2o_emissions[vehicle_type][fuel_type][year]['N2O']}
                  for year in self.total_useage_and_ch4_and_n2o_emissions[vehicle_type][fuel_type]]}
             for vehicle_type in self.total_useage_and_ch4_and_n2o_emissions
             for fuel_type in self.total_useage_and_ch4_and_n2o_emissions[vehicle_type]
             if vehicle_type in self.road_vehicles and fuel_type == 'gasoline']

        self._output['totalOrganizationWideOnRoadGasolineMobileSourceMileageAndEmissions'] = \
            total_on_road_gasoline_mileage_and_emissions

    def make_total_organization_wide_on_road_non_gasoline_mobile_source_mileage_and_emissions(self):
        """ Select non-gasoline on road vehicle data and format total_useage_and_ch4_and_n2o_emissions for schema """

        total_on_road_non_gasoline_mileage_and_emissions = \
            [{'vehicleType': vehicle_type,
              'fuelType': fuel_type,
              'emissionByYear': [
                  {'vehicleYear': year,
                   'mileage': self.total_useage_and_ch4_and_n2o_emissions[vehicle_type][fuel_type][year]['mileage'],
                   'CH4': self.total_useage_and_ch4_and_n2o_emissions[vehicle_type][fuel_type][year]['CH4'],
                   'N2O': self.total_useage_and_ch4_and_n2o_emissions[vehicle_type][fuel_type][year]['N2O']}
                  for year in self.total_useage_and_ch4_and_n2o_emissions[vehicle_type][fuel_type]]}
             for vehicle_type in self.total_useage_and_ch4_and_n2o_emissions
             for fuel_type in self.total_useage_and_ch4_and_n2o_emissions[vehicle_type]
             if vehicle_type in self.road_vehicles and fuel_type != 'gasoline']

        self._output['totalOrganizationWideOnRoadNonGasolineMobileSourceMileageAndEmissions'] = \
            total_on_road_non_gasoline_mileage_and_emissions

    def make_total_organization_wide_non_road_mobile_source_fuel_usage_and_emissions(self):
        """ Select non-road vehicle data and format total_useage_and_ch4_and_n2o_emissions for schema """

        total_on_road_non_gasoline_mileage_and_emissions = \
            [{'vehicleType': vehicle_type,
              'emissionByFuelType': [
                  {'fuelType': fuel_type,
                   'fuelUsage': self.total_useage_and_ch4_and_n2o_emissions[vehicle_type][fuel_type]['']['fuelUsage'],
                   'CH4': self.total_useage_and_ch4_and_n2o_emissions[vehicle_type][fuel_type]['']['CH4'],
                   'N2O': self.total_useage_and_ch4_and_n2o_emissions[vehicle_type][fuel_type]['']['N2O']}
                  for fuel_type in self.total_useage_and_ch4_and_n2o_emissions[vehicle_type]]}
             for vehicle_type in self.total_useage_and_ch4_and_n2o_emissions
             if vehicle_type in self.nonroad_vehicles]

        self._output['totalOrganizationWideNonRoadMobileSourceFuelUsageAndEmissions'] = \
            total_on_road_non_gasoline_mileage_and_emissions

    @staticmethod
    def calculate_co2_emissions(fuel_type, fuel_usage):
        """ Calculate CO2 emissions for a mobile source fuel """
        ret = mobile_combustion_co2_emission_factors[fuel_type] * fuel_usage
        return ret

    @staticmethod
    def calculate_ch4_emissions(vehicle_type, fuel_type, usage, vehicle_year):
        """ Calculate CH4 emissions for a mobile source vehicle. usage is either fuel_usage or miles_traveled depending
        on if the vehicle_type is non-road or on road, respectively. """
        ret = mobile_combustion_ch4_and_n2o_emission_factors[vehicle_type][fuel_type][vehicle_year]['ch4_factor'] * \
              usage
        return ret

    @staticmethod
    def calculate_n2o_emissions(vehicle_type, fuel_type, usage, vehicle_year):
        """ Calculate CH4 emissions for a mobile source vehicle. usage is either fuel_usage or miles_traveled depending
        on if the vehicle_type is non-road or on road, respectively. """
        ret = mobile_combustion_ch4_and_n2o_emission_factors[vehicle_type][fuel_type][vehicle_year]['n2o_factor'] * \
              usage
        return ret

    def make_total_co2_equivalent_emissions(self):
        """ Calculate total CO2 equivalent emissions """
        total = (self._total_emissions['CO2'] + refrigerants_gwp_factors['ch4'] * self._total_emissions['CH4'] / 1000. +
                 refrigerants_gwp_factors['n2o'] * self._total_emissions['N2O'] / 1000.) / 1000.

        self._output['totalCo2EquivalentEmissions'] = total

    def make_total_biomass_co2_equivalent_emissions(self):
        """ Calculate total biomass CO2 equivalent emissions """
        total = (self.total_fuel_usage_and_co2_emissions['ethanol']['fuelUsage'] * self.ethanol_percent / 100. *
                 mobile_combustion_co2_emission_factors['ethanol'] +
                 self.total_fuel_usage_and_co2_emissions['biodiesel']['fuelUsage'] * self.biodiesel_percent / 100. *
                 mobile_combustion_co2_emission_factors['biodiesel']) / 1000.

        self._output['totalBiomassCo2EquivalentEmissions'] = total
