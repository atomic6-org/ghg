""" Business Travel Model """
# pylint: disable=no-name-in-module
import logging

from atomic6ghg.formulas import Formula, null_replacer
from atomic6ghg.factors import business_travel_factors, refrigerants_gwp_factors

logger = logging.getLogger(__name__)


class BusinessTravel(Formula):
    """ Calculate emissions from business travel """
    personal_vehicles = ['passengerCars', 'lightDutyTruck', 'motorcycle']
    rail_or_bus = ['intercityRailNortheastCorridor', 'intercityRailOtherRoutes', 'intercityRailNationalAverage',
                      'commuterRail', 'transitRail', 'bus']
    flight_length = ['shortHaul', 'mediumHaul', 'longHaul']
    vehicle_types_all = personal_vehicles + rail_or_bus + flight_length

    def __init__(self, wks_data=None):
        super().__init__(wks_data=wks_data)

        self._total_emissions_by_vehicle = {}
        self._total_emissions_by_rail_or_bus = {}
        self._total_emissions_by_air = {}

        self.recalc(self.wks_data)

    def recalc(self, wks_data: dict) -> dict:
        """Execute recalc procedure for Commuting"""
        self.wks_data = wks_data

        self.make_personal_vehicle_rental_car_or_taxi()
        self.make_personal_vehicle_total()
        self.make_rail_or_bus()
        self.make_rail_or_bus_total()
        self.make_air_business_travel()
        self.make_air_total()
        self.make_co2_emissions_by_travel_type()
        self.make_co2_equivalent_emissions()

        return self.to_dict()

    def make_personal_vehicle_rental_car_or_taxi(self):
        """Calculate CO2 equivalent emissions for each input row in Personal Vehicle, Rental Car or Taxi table"""
        personal_vehicle = []
        self._total_emissions = {
            'personalVehicleRentalCarOrTaxiBusinessTravel': {
                'CO2': 0.,
                'CH4': 0.,
                'N2O': 0.
            }
        }
        self._total_emissions_by_vehicle = {vehicle: {
            'CO2': 0.,
            'CH4': 0.,
            'N2O': 0.
        } for vehicle in self.personal_vehicles}

        for row in self.wks_data.get('personalVehicleRentalCarOrTaxiBusinessTravel', []):
            vehicle = row['vehicleType']
            if not vehicle:
                personal_vehicle.append(row)
                continue
            if vehicle:
                travel_factor_co2 = business_travel_factors[vehicle]['co2']
                travel_factor_ch4 = business_travel_factors[vehicle]['ch4']
                travel_factor_n2o = business_travel_factors[vehicle]['n2o']
            else:
                travel_factor_co2, travel_factor_ch4, travel_factor_n2o = 0., 0., 0.

            vehicle_miles = null_replacer(row['vehicleMiles'])

            co2_emissions = BusinessTravel.calculate_transportation_emissions(travel_factor_co2, vehicle_miles)
            ch4_emissions = BusinessTravel.calculate_transportation_emissions(travel_factor_ch4, vehicle_miles)
            n2o_emissions = BusinessTravel.calculate_transportation_emissions(travel_factor_n2o, vehicle_miles)

            self._total_emissions['personalVehicleRentalCarOrTaxiBusinessTravel']['CO2'] += co2_emissions
            self._total_emissions['personalVehicleRentalCarOrTaxiBusinessTravel']['CH4'] += ch4_emissions
            self._total_emissions['personalVehicleRentalCarOrTaxiBusinessTravel']['N2O'] += n2o_emissions
            self._total_emissions_by_vehicle[vehicle]['CO2'] += co2_emissions
            self._total_emissions_by_vehicle[vehicle]['CH4'] += ch4_emissions
            self._total_emissions_by_vehicle[vehicle]['N2O'] += n2o_emissions

            calculated_row = {'sourceId': row.get('sourceId'), 'sourceDescription': row.get('sourceDescription'),
                              'vehicleType': vehicle, 'vehicleMiles': vehicle_miles, 'CO2': co2_emissions,
                              'CH4': ch4_emissions, 'N2O': n2o_emissions}

            personal_vehicle.append(calculated_row)

        self._output['personalVehicleRentalCarOrTaxiBusinessTravel'] = personal_vehicle

    def make_personal_vehicle_total(self):
        """ Make total row for personal vehicles """
        personal_vehicle_total = {'CO2': self._total_emissions['personalVehicleRentalCarOrTaxiBusinessTravel']['CO2'],
                                  'CH4': self._total_emissions['personalVehicleRentalCarOrTaxiBusinessTravel']['CH4'],
                                  'N2O': self._total_emissions['personalVehicleRentalCarOrTaxiBusinessTravel']['N2O']}

        self._output['totalForAllPersonalVehicleBusinessTravel'] = personal_vehicle_total

    def make_rail_or_bus(self):
        """Calculate CO2 equivalent emissions for each input row in Rail or Bus table"""
        rail_or_bus_vehicle = []
        self._total_emissions = {
            'railOrBusBusinessTravel': {
                'CO2': 0.,
                'CH4': 0.,
                'N2O': 0.
            }
        }

        self._total_emissions_by_rail_or_bus = {rail_or_bus: {
            'CO2': 0.,
            'CH4': 0.,
            'N2O': 0.
        } for rail_or_bus in self.rail_or_bus}

        for row in self.wks_data.get('railOrBusBusinessTravel', []):
            vehicle = row['vehicleType']
            if not vehicle:
                rail_or_bus_vehicle.append(row)
                continue
            if vehicle:
                travel_factor_co2 = business_travel_factors[vehicle]['co2']
                travel_factor_ch4 = business_travel_factors[vehicle]['ch4']
                travel_factor_n2o = business_travel_factors[vehicle]['n2o']
            else:
                travel_factor_co2, travel_factor_ch4, travel_factor_n2o = 0., 0., 0.

            vehicle_miles = null_replacer(row['passengerMiles'])

            co2_emissions = BusinessTravel.calculate_transportation_emissions(travel_factor_co2, vehicle_miles)
            ch4_emissions = BusinessTravel.calculate_transportation_emissions(travel_factor_ch4, vehicle_miles)
            n2o_emissions = BusinessTravel.calculate_transportation_emissions(travel_factor_n2o, vehicle_miles)

            self._total_emissions['railOrBusBusinessTravel']['CO2'] += co2_emissions
            self._total_emissions['railOrBusBusinessTravel']['CH4'] += ch4_emissions
            self._total_emissions['railOrBusBusinessTravel']['N2O'] += n2o_emissions
            self._total_emissions_by_rail_or_bus[vehicle]['CO2'] += co2_emissions
            self._total_emissions_by_rail_or_bus[vehicle]['CH4'] += ch4_emissions
            self._total_emissions_by_rail_or_bus[vehicle]['N2O'] += n2o_emissions

            calculated_row = {'sourceId': row.get('sourceId'), 'sourceDescription': row.get('sourceDescription'),
                              'vehicleType': vehicle, 'passengerMiles': vehicle_miles, 'CO2': co2_emissions,
                              'CH4': ch4_emissions, 'N2O': n2o_emissions}

            rail_or_bus_vehicle.append(calculated_row)

        self._output['railOrBusBusinessTravel'] = rail_or_bus_vehicle

    def make_rail_or_bus_total(self):
        """ Make total row for rail or bus """
        rail_or_bus_total = {'CO2': self._total_emissions['railOrBusBusinessTravel']['CO2'],
                             'CH4': self._total_emissions['railOrBusBusinessTravel']['CH4'],
                             'N2O': self._total_emissions['railOrBusBusinessTravel']['N2O']}

        self._output['totalForAllRailAndBusBusinessTravel'] = rail_or_bus_total

    def make_air_business_travel(self):
        """Calculate CO2 equivalent emissions for each input row in Air table"""
        air_vehicle = []
        self._total_emissions = {
            'airBusinessTravel': {
                'CO2': 0.,
                'CH4': 0.,
                'N2O': 0.
            }
        }

        self._total_emissions_by_air = {flight_length: {
            'CO2': 0.,
            'CH4': 0.,
            'N2O': 0.
        } for flight_length in self.flight_length}

        for row in self.wks_data.get('airBusinessTravel', []):
            vehicle = row['flightLength']
            if not vehicle:
                air_vehicle.append(row)
                continue
            if vehicle:
                travel_factor_co2 = business_travel_factors[vehicle]['co2']
                travel_factor_ch4 = business_travel_factors[vehicle]['ch4']
                travel_factor_n2o = business_travel_factors[vehicle]['n2o']
            else:
                travel_factor_co2, travel_factor_ch4, travel_factor_n2o = 0., 0., 0.

            vehicle_miles = null_replacer(row['passengerMiles'])

            co2_emissions = BusinessTravel.calculate_transportation_emissions(travel_factor_co2, vehicle_miles)
            ch4_emissions = BusinessTravel.calculate_transportation_emissions(travel_factor_ch4, vehicle_miles)
            n2o_emissions = BusinessTravel.calculate_transportation_emissions(travel_factor_n2o, vehicle_miles)

            self._total_emissions['airBusinessTravel']['CO2'] += co2_emissions
            self._total_emissions['airBusinessTravel']['CH4'] += ch4_emissions
            self._total_emissions['airBusinessTravel']['N2O'] += n2o_emissions
            self._total_emissions_by_air[vehicle]['CO2'] += co2_emissions
            self._total_emissions_by_air[vehicle]['CH4'] += ch4_emissions
            self._total_emissions_by_air[vehicle]['N2O'] += n2o_emissions

            calculated_row = {'sourceId': row.get('sourceId'), 'sourceDescription': row.get('sourceDescription'),
                              'flightLength': vehicle, 'passengerMiles': vehicle_miles, 'CO2': co2_emissions,
                              'CH4': ch4_emissions, 'N2O': n2o_emissions}

            air_vehicle.append(calculated_row)

        self._output['airBusinessTravel'] = air_vehicle

    def make_air_total(self):
        """ Make total row for air """
        air_total = {'CO2': self._total_emissions['airBusinessTravel']['CO2'],
                     'CH4': self._total_emissions['airBusinessTravel']['CH4'],
                     'N2O': self._total_emissions['airBusinessTravel']['N2O']}

        self._output['totalForAllAirBusinessTravel'] = air_total

    def make_co2_emissions_by_travel_type(self):
        """Calculate CO2 equivalent emissions for each input row"""
        total_commuting_type_co2 = []
        self._total_emissions['total'] = {'CO2': 0., 'CH4': 0., 'N2O': 0.}
        self._total_emissions.update(self._total_emissions_by_vehicle)
        self._total_emissions.update(self._total_emissions_by_rail_or_bus)
        self._total_emissions.update(self._total_emissions_by_air)
        for transport_type in self.vehicle_types_all:
            self._total_emissions['total']['CO2'] += self._total_emissions[transport_type]['CO2']
            self._total_emissions['total']['CH4'] += self._total_emissions[transport_type]['CH4']
            self._total_emissions['total']['N2O'] += self._total_emissions[transport_type]['N2O']

            calculated_row = {'transportType': transport_type, 'CO2': self._total_emissions[transport_type]['CO2'],
                              'CH4': self._total_emissions[transport_type]['CH4'],
                              'N2O': self._total_emissions[transport_type]['N2O']}
            total_commuting_type_co2.append(calculated_row)
        self._output['totalCo2EmissionsByTravelType'] = total_commuting_type_co2

    @staticmethod
    def calculate_transportation_emissions(travel_factor, vehicle_miles):
        """Calculate emissions for a gas given travel factor and vehicle miles inputs"""
        ret = travel_factor * vehicle_miles
        # Handle potential negative values
        ret = max(0., ret)
        return ret

    def make_co2_equivalent_emissions(self):
        """Calculate co2 equivalent emissions """
        total = (self._total_emissions['total']['CO2'] +
                 (self._total_emissions['total']['CH4'] / 1000 * refrigerants_gwp_factors['ch4']) +
                 (self._total_emissions['total']['N2O'] / 1000 * refrigerants_gwp_factors['n2o'])) / 1000
        self._output['totalCo2EquivalentEmissions'] = total
