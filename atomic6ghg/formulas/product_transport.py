""" Product Transport models """
# pylint: disable=no-name-in-module
import logging

from atomic6ghg.formulas import Formula
from atomic6ghg.factors import product_transport_emission_factors, refrigerants_gwp_factors

logger = logging.getLogger(__name__)


class ProductTransport(Formula):
    """ Calculate emissions from vehicles used for product transport """

    vehicle_types_miles = ['mediumAndHeavyDutyTruck', 'lightDutyTruck', 'passengerCars']
    vehicle_types_short_ton = ['mediumAndHeavyDutyTruck', 'rail', 'aircraft', 'waterborneCraft']
    vehicle_types_all = set(vehicle_types_miles + vehicle_types_short_ton)

    def __init__(self, wks_data=None):
        super().__init__(wks_data=wks_data)
        self._total_emissions_by_vehicle_type_miles = {}
        self._total_emissions_by_miles = {}
        self._total_emissions_by_vehicle_type_short_ton = {}
        self._total_emissions_by_short_ton = {}
        self.recalc(self.wks_data)

    def recalc(self, wks_data: dict) -> dict:
        """Execute recalc procedure for ProductTransport"""
        self.wks_data = wks_data

        self.make_product_transport_by_vehicle_miles()
        self.make_total_by_vehicle_miles()
        self.make_product_transport_by_short_ton_miles()
        self.make_total_by_ton_miles()
        self.make_total_emissions_by_product_transport_type()
        self.make_co2_equivalent_emissions()

        return self.to_dict()

    def make_product_transport_by_vehicle_miles(self):
        """Calculate emissions (CO2, CH4, N2O) for each input row"""
        product_transport_by_vehicle_miles = []
        self._total_emissions_by_vehicle_type_miles = {vehicle_type: {'CO2': 0., 'CH4': 0., 'N2O': 0.}
                                                       for vehicle_type in self.vehicle_types_miles}
        self._total_emissions_by_miles = {'CO2': 0., 'CH4': 0., 'N2O': 0.}
        for row in self.wks_data.get('productTransportByVehicleMiles', []):
            vehicle_type = row['vehicleType']
            vehicle_miles = row['vehicleMiles']
            if not vehicle_type or not vehicle_miles:
                product_transport_by_vehicle_miles.append(row)
                continue

            co2_emissions = ProductTransport.calculate_vehicle_emissions(vehicle_type, vehicle_miles, 'co2',
                'vehicle-mile')
            ch4_emissions = ProductTransport.calculate_vehicle_emissions(vehicle_type, vehicle_miles, 'ch4',
                'vehicle-mile')
            n2o_emissions = ProductTransport.calculate_vehicle_emissions(vehicle_type, vehicle_miles, 'n2o',
                'vehicle-mile')

            self._total_emissions_by_vehicle_type_miles[vehicle_type]['CO2'] += co2_emissions
            self._total_emissions_by_vehicle_type_miles[vehicle_type]['CH4'] += ch4_emissions
            self._total_emissions_by_vehicle_type_miles[vehicle_type]['N2O'] += n2o_emissions

            self._total_emissions_by_miles['CO2'] += co2_emissions
            self._total_emissions_by_miles['CH4'] += ch4_emissions
            self._total_emissions_by_miles['N2O'] += n2o_emissions

            calculated_row = {'sourceId': row.get('sourceId'), 'sourceDescription': row.get('sourceDescription'),
                              'vehicleType': vehicle_type, 'vehicleMiles': vehicle_miles, 'CO2': co2_emissions,
                              'CH4': ch4_emissions, 'N2O': n2o_emissions}
            product_transport_by_vehicle_miles.append(calculated_row)

        self._output['productTransportByVehicleMiles'] = product_transport_by_vehicle_miles

    def make_total_by_vehicle_miles(self):
        """ Make total row for vehicle miles """
        total_by_vehicle_miles = {'CO2': self._total_emissions_by_miles['CO2'],
                                  'CH4': self._total_emissions_by_miles['CH4'],
                                  'N2O': self._total_emissions_by_miles['N2O']}

        self._output['totalForProductTransportByVehicleMiles'] = total_by_vehicle_miles

    def make_product_transport_by_short_ton_miles(self):
        """Calculate emissions (CO2, CH4, N2O) for each input row"""
        product_transport_by_short_ton_miles = []
        self._total_emissions_by_vehicle_type_short_ton = {vehicle_type: {'CO2': 0., 'CH4': 0., 'N2O': 0.}
                                                           for vehicle_type in self.vehicle_types_short_ton}
        self._total_emissions_by_short_ton = {'CO2': 0., 'CH4': 0., 'N2O': 0.}
        for row in self.wks_data.get('productTransportByTonMiles', []):
            vehicle_type = row['vehicleType']
            short_ton_miles = row['shortTonMiles']
            if not vehicle_type or not short_ton_miles:
                product_transport_by_short_ton_miles.append(row)
                continue

            co2_emissions = ProductTransport.calculate_vehicle_emissions(vehicle_type, short_ton_miles, 'co2',
                'ton-mile')
            ch4_emissions = ProductTransport.calculate_vehicle_emissions(vehicle_type, short_ton_miles, 'ch4',
                'ton-mile')
            n2o_emissions = ProductTransport.calculate_vehicle_emissions(vehicle_type, short_ton_miles, 'n2o',
                'ton-mile')

            self._total_emissions_by_vehicle_type_short_ton[vehicle_type]['CO2'] += co2_emissions
            self._total_emissions_by_vehicle_type_short_ton[vehicle_type]['CH4'] += ch4_emissions
            self._total_emissions_by_vehicle_type_short_ton[vehicle_type]['N2O'] += n2o_emissions

            self._total_emissions_by_short_ton['CO2'] += co2_emissions
            self._total_emissions_by_short_ton['CH4'] += ch4_emissions
            self._total_emissions_by_short_ton['N2O'] += n2o_emissions

            calculated_row = {'sourceId': row.get('sourceId'), 'sourceDescription': row.get('sourceDescription'),
                              'vehicleType': vehicle_type, 'shortTonMiles': short_ton_miles, 'CO2': co2_emissions,
                              'CH4': ch4_emissions, 'N2O': n2o_emissions}
            product_transport_by_short_ton_miles.append(calculated_row)

        self._output['productTransportByTonMiles'] = product_transport_by_short_ton_miles

    def make_total_by_ton_miles(self):
        """ Make total row for ton miles """
        total_by_ton_miles = {'CO2': self._total_emissions_by_short_ton['CO2'],
                              'CH4': self._total_emissions_by_short_ton['CH4'],
                              'N2O': self._total_emissions_by_short_ton['N2O']}

        self._output['totalForAllProductTransportByTonMiles'] = total_by_ton_miles

    def make_total_emissions_by_product_transport_type(self):
        """Calculate emissions for each vehicle type"""
        total_emissions_by_product_transport_type = []
        for vehicle_type in self.vehicle_types_all:
            zero_dict = {'CO2': 0., 'CH4': 0., 'N2O': 0.}
            short_ton_emissions = self._total_emissions_by_vehicle_type_short_ton.get(vehicle_type, zero_dict)
            miles_emissions = self._total_emissions_by_vehicle_type_miles.get(vehicle_type, zero_dict)

            co2_emissions = short_ton_emissions['CO2'] + miles_emissions['CO2']
            ch4_emissions = short_ton_emissions['CH4'] + miles_emissions['CH4']
            n2o_emissions = short_ton_emissions['N2O'] + miles_emissions['N2O']

            row = {'transportType': vehicle_type, 'CO2': co2_emissions, 'CH4': ch4_emissions, 'N2O': n2o_emissions}

            total_emissions_by_product_transport_type.append(row)

        self._output['totalEmissionsByProductTransportType'] = total_emissions_by_product_transport_type

    @staticmethod
    def calculate_vehicle_emissions(vehicle_type, usage, gas_emissions, units):
        """Calculate gas emissions (CO2, CH4, N2O) emissions for a vehicle"""
        ret = product_transport_emission_factors[vehicle_type][units][gas_emissions] * usage
        # Handle potential negative values
        ret = max(0., ret)
        return ret

    def make_co2_equivalent_emissions(self):
        """ Calculate co2 equivalent emissions """
        co2_total = self._total_emissions_by_miles['CO2'] + self._total_emissions_by_short_ton['CO2']
        ch4_total = self._total_emissions_by_miles['CH4'] + self._total_emissions_by_short_ton['CH4']
        n2o_total = self._total_emissions_by_miles['N2O'] + self._total_emissions_by_short_ton['N2O']

        total = (refrigerants_gwp_factors['co2'] * co2_total +
                 refrigerants_gwp_factors['ch4'] * ch4_total / 1000 +
                 refrigerants_gwp_factors['n2o'] * n2o_total / 1000) / 1000

        self._output['totalCo2EquivalentEmissions'] = total
