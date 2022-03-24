""" Commuting models """
# pylint: disable=no-name-in-module
import logging

from atomic6ghg.formulas import Formula, null_replacer
from atomic6ghg.factors import business_travel_factors, refrigerants_gwp_factors

logger = logging.getLogger(__name__)


class Commuting(Formula):
    """ Calculate emissions from commuting equipment """

    personal_vehicles = ['passengerCars', 'lightDutyTruck', 'motorcycle']
    public_transit = ['intercityRailNortheastCorridor', 'intercityRailOtherRoutes', 'intercityRailNationalAverage',
                      'commuterRail', 'transitRail', 'bus']
    all_vehicles = personal_vehicles + public_transit

    def __init__(self, wks_data=None):
        super().__init__(wks_data=wks_data)
        self._total_emissions_by_vehicle = {}
        self._total_emissions_by_transit = {}
        self.recalc(self.wks_data)

    def recalc(self, wks_data: dict) -> dict:
        """Execute recalc procedure for Commuting"""
        self.wks_data = wks_data

        self.make_personal_vehicle()
        self.make_total_for_all_personal_vehicle()
        self.make_public_transportation()
        self.make_total_for_all_public_transportation()
        self.make_emissions_by_commuting_type()
        self.make_co2_equivalent_emissions()

        return self.to_dict()

    def make_personal_vehicle(self):
        """Calculate CO2 equivalent emissions for each input row in Personal Vehicle table"""
        personal_vehicle = []
        self._total_emissions = {
            'personalVehicle': {
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

        for row in self.wks_data.get('personalVehicle', []):
            vehicle_type = row['vehicleType']
            vehicle_miles = row['vehicleMiles']
            if not vehicle_type or not vehicle_miles:
                personal_vehicle.append(row)
                continue
            if vehicle_type:
                travel_factor_co2 = business_travel_factors[vehicle_type]['co2']
                travel_factor_ch4 = business_travel_factors[vehicle_type]['ch4']
                travel_factor_n2o = business_travel_factors[vehicle_type]['n2o']
            else:
                travel_factor_co2, travel_factor_ch4, travel_factor_n2o = 0., 0., 0.

            vehicle_miles = null_replacer(row['vehicleMiles'])

            co2_emissions = Commuting.calculate_transportation_emissions(travel_factor_co2, vehicle_miles)
            ch4_emissions = Commuting.calculate_transportation_emissions(travel_factor_ch4, vehicle_miles)
            n2o_emissions = Commuting.calculate_transportation_emissions(travel_factor_n2o, vehicle_miles)

            self._total_emissions['personalVehicle']['CO2'] += co2_emissions
            self._total_emissions['personalVehicle']['CH4'] += ch4_emissions
            self._total_emissions['personalVehicle']['N2O'] += n2o_emissions
            self._total_emissions_by_vehicle[vehicle_type]['CO2'] += co2_emissions
            self._total_emissions_by_vehicle[vehicle_type]['CH4'] += ch4_emissions
            self._total_emissions_by_vehicle[vehicle_type]['N2O'] += n2o_emissions

            calculated_row = {'sourceId': row.get('sourceId'), 'sourceDescription': row.get('sourceDescription'),
                              'vehicleType': vehicle_type, 'vehicleMiles': vehicle_miles, 'CO2': co2_emissions,
                              'CH4': ch4_emissions, 'N2O': n2o_emissions}

            personal_vehicle.append(calculated_row)

        self._output['personalVehicle'] = personal_vehicle

    def make_total_for_all_personal_vehicle(self):
        """ Make total row """
        total_for_all_personal_vehicle = {
                     'CO2': self._total_emissions['personalVehicle']['CO2'],
                     'CH4': self._total_emissions['personalVehicle']['CH4'],
                     'N2O': self._total_emissions['personalVehicle']['N2O']}

        self._output['totalForAllPersonalVehicleEmployeeCommuting'] = total_for_all_personal_vehicle

    def make_public_transportation(self):
        """Calculate emissions for each input row in Public Transportation table"""
        public_transportation = []
        self._total_emissions.update({
            'publicTransportation': {
                'CO2': 0.,
                'CH4': 0.,
                'N2O': 0.
            }
        })

        self._total_emissions_by_transit = {transit: {
            'CO2': 0.,
            'CH4': 0.,
            'N2O': 0.
        } for transit in self.public_transit}

        for row in self.wks_data.get('publicTransportation', []):
            transport = row['transportType']
            passenger_miles = row['passengerMiles']
            if not transport or not passenger_miles:
                public_transportation.append(row)
                continue
            if transport:
                travel_factor_co2 = business_travel_factors[transport]['co2']
                travel_factor_ch4 = business_travel_factors[transport]['ch4']
                travel_factor_n2o = business_travel_factors[transport]['n2o']
            else:
                travel_factor_co2, travel_factor_ch4, travel_factor_n2o = 0., 0., 0.

            passenger_miles = null_replacer(row['passengerMiles'])

            co2_emissions = Commuting.calculate_transportation_emissions(travel_factor_co2, passenger_miles)
            ch4_emissions = Commuting.calculate_transportation_emissions(travel_factor_ch4, passenger_miles)
            n2o_emissions = Commuting.calculate_transportation_emissions(travel_factor_n2o, passenger_miles)

            self._total_emissions['publicTransportation']['CO2'] += co2_emissions
            self._total_emissions['publicTransportation']['CH4'] += ch4_emissions
            self._total_emissions['publicTransportation']['N2O'] += n2o_emissions
            self._total_emissions_by_transit[transport]['CO2'] += co2_emissions
            self._total_emissions_by_transit[transport]['CH4'] += ch4_emissions
            self._total_emissions_by_transit[transport]['N2O'] += n2o_emissions

            calculated_row = {'sourceId': row['sourceId'], 'sourceDescription': row['sourceDescription'],
                              'transportType': transport, 'passengerMiles': passenger_miles, 'CO2': co2_emissions,
                              'CH4': ch4_emissions, 'N2O': n2o_emissions}

            public_transportation.append(calculated_row)

        self._output['publicTransportation'] = public_transportation

    def make_total_for_all_public_transportation(self):
        """ Make total row """
        total_for_all_public_transportation = {
                     'CO2': self._total_emissions['publicTransportation']['CO2'],
                     'CH4': self._total_emissions['publicTransportation']['CH4'],
                     'N2O': self._total_emissions['publicTransportation']['N2O']}

        self._output['totalForAllPublicTransportationEmployeeCommuting'] = total_for_all_public_transportation

    def make_emissions_by_commuting_type(self):
        """Calculate CO2 equivalent emissions for each input row"""
        total_commuting_type_co2 = []
        self._total_emissions['total'] = {'CO2': 0., 'CH4': 0., 'N2O': 0.}
        self._total_emissions.update(self._total_emissions_by_vehicle)
        self._total_emissions.update(self._total_emissions_by_transit)
        for transport_type in self.all_vehicles:

            self._total_emissions['total']['CO2'] += self._total_emissions[transport_type]['CO2']
            self._total_emissions['total']['CH4'] += self._total_emissions[transport_type]['CH4']
            self._total_emissions['total']['N2O'] += self._total_emissions[transport_type]['N2O']

            calculated_row = {'transportType': transport_type, 'CO2': self._total_emissions[transport_type]['CO2'],
                              'CH4': self._total_emissions[transport_type]['CH4'],
                              'N2O': self._total_emissions[transport_type]['N2O']}
            total_commuting_type_co2.append(calculated_row)
        self._output['totalCO2EmissionsByCommutingType'] = total_commuting_type_co2

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
        self._output['totalCO2EquivalentEmissions'] = total
