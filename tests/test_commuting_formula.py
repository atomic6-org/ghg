import pytest
import json
import os

from atomic6ghg.formulas import Commuting, null_replacer


@pytest.fixture
def canonical_data():
    TEST_FILENAME = os.path.join(os.path.dirname(__file__), './fixtures/commuting_canonical_instance.json')
    with open(TEST_FILENAME, 'r', encoding='utf-8') as canonical_instance:
        commuting_document = json.load(canonical_instance)
        return commuting_document


@pytest.fixture
def calculated_data(canonical_data):
    commuting = Commuting(wks_data=canonical_data)
    return commuting


def test_make_personal_vehicle(canonical_data, calculated_data):
    key = "personalVehicle"
    calculated_transports = []
    canonical_transports = []
    for i, canonical_row in enumerate(canonical_data[key]):
        vehicle = canonical_row["vehicleType"]
        vehicle_miles = canonical_row["vehicleMiles"]
        source_id = canonical_row['sourceId']
        co2 = null_replacer(canonical_row['CO2'])
        ch4 = null_replacer(canonical_row['CH4'])
        n2o = null_replacer(canonical_row['N2O'])
        canonical_transports.append(vehicle)

        calculated_row = calculated_data._output[key][i]
        calculated_vehicle = calculated_row['vehicleType']
        calculated_vehicle_miles = calculated_row['vehicleMiles']
        calculated_source_id = calculated_row['sourceId']
        calculated_co2 = calculated_row['CO2']
        calculated_ch4 = calculated_row['CH4']
        calculated_n2o = calculated_row['N2O']

        if vehicle == calculated_vehicle and vehicle_miles == calculated_vehicle_miles and\
                source_id == calculated_source_id:
            assert co2 == calculated_co2
            assert ch4 == calculated_ch4
            assert n2o == calculated_n2o
            calculated_transports.append(calculated_vehicle)
    assert calculated_transports == canonical_transports

    calculated_transports_all = []
    for row in calculated_data._output[key]:
        calculated_transports_all.append(row['vehicleType'])

    assert calculated_transports_all == canonical_transports


def test_make_public_transportation(canonical_data, calculated_data):
    key = "publicTransportation"
    calculated_transports = []
    canonical_transports = []
    for i, canonical_row in enumerate(canonical_data[key]):
        transport = canonical_row["transportType"]
        miles = canonical_row["passengerMiles"]
        co2 = null_replacer(canonical_row['CO2'])
        ch4 = null_replacer(canonical_row['CH4'])
        n2o = null_replacer(canonical_row['N2O'])
        canonical_transports.append(transport)

        calculated_row = calculated_data._output[key][i]
        calculated_transport = calculated_row['transportType']
        calculated_miles = calculated_row['passengerMiles']
        calculated_co2 = calculated_row['CO2']
        calculated_ch4 = calculated_row['CH4']
        calculated_n2o = calculated_row['N2O']

        if transport == calculated_transport and miles == calculated_miles:
            assert co2 == calculated_co2
            assert ch4 == calculated_ch4
            assert n2o == calculated_n2o
            calculated_transports.append(calculated_transport)
    assert calculated_transports == canonical_transports

    calculated_transports_all = []
    for row in calculated_data._output[key]:
        calculated_transports_all.append(row['transportType'])

    assert calculated_transports_all == canonical_transports


def test_make_total_for_all_personal_vehicle(canonical_data, calculated_data):
    key = 'totalForAllPersonalVehicleEmployeeCommuting'
    canonical_values = canonical_data[key]
    calculated_values = calculated_data._output[key]
    for gas in canonical_values:
        assert canonical_values[gas] == calculated_values[gas]
    assert canonical_values.keys() == calculated_values.keys()


def test_make_co2_emissions_by_commuting_type(canonical_data, calculated_data):
    key = "totalCO2EmissionsByCommutingType"
    calculated_transports = []
    canonical_transports = []
    for i, canonical_row in enumerate(canonical_data[key]):
        transport_type = canonical_row["transportType"]
        co2 = null_replacer(canonical_row['CO2'])
        ch4 = null_replacer(canonical_row['CH4'])
        n2o = null_replacer(canonical_row['N2O'])
        # co2_equivalent_emissions = null_replacer(canonical_row['CO2EquivalentEmissions'])
        canonical_transports.append(transport_type)

        calculated_row = calculated_data._output[key][i]
        calculated_transport = calculated_row['transportType']
        calculated_co2 = null_replacer(calculated_row['CO2'])
        calculated_ch4 = null_replacer(calculated_row['CH4'])
        calculated_n2o = null_replacer(calculated_row['N2O'])

        if transport_type == calculated_transport:
            assert co2 == calculated_co2
            assert ch4 == calculated_ch4
            assert n2o == calculated_n2o
            calculated_transports.append(calculated_transport)
    assert calculated_transports == canonical_transports

    calculated_transports_all = []
    for row in calculated_data._output[key]:
        calculated_transports_all.append(row['transportType'])

    assert calculated_transports_all == canonical_transports


def test_make_total_for_all_public_transportation(canonical_data, calculated_data):
    key = 'totalForAllPublicTransportationEmployeeCommuting'
    canonical_values = canonical_data[key]
    calculated_values = calculated_data._output[key]
    for gas in canonical_values:
        assert canonical_values[gas] == calculated_values[gas]
    assert canonical_values.keys() == calculated_values.keys()


def test_make_co2_equivalent_emissions(canonical_data, calculated_data):
    key = "totalCO2EquivalentEmissions"
    assert canonical_data[key] == calculated_data._output[key]


def test_to_dict(calculated_data):
    output = calculated_data.to_dict()
    assert isinstance(output, dict)

    calculated_data._output = lambda x: x  # function is not serializable
    assert calculated_data.to_dict() is None


def test_to_json(calculated_data):
    output = calculated_data.to_json()
    assert isinstance(output, str)

    calculated_data._output = lambda x: x  # function is not serializable
    assert calculated_data.to_json() is None


def test_output_schema_compliance(calculated_data, canonical_data, commuting_schema):
    output = calculated_data.to_dict()
    output['version'] = canonical_data['version']
    commuting_schema.validate(output)