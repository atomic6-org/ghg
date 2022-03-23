import pytest
import json
import os

from atomic6ghg.formulas import ProductTransport


@pytest.fixture
def canonical_data():
    TEST_FILENAME = os.path.join(os.path.dirname(__file__), './fixtures/product_transport_canonical_instance.json')
    with open(TEST_FILENAME, 'r', encoding='utf-8') as canonical_instance:
        product_transport_document = json.load(canonical_instance)
        return product_transport_document


@pytest.fixture
def calculated_data(canonical_data):
    product_transport = ProductTransport(wks_data=canonical_data)
    return product_transport


def test_make_product_transport_by_vehicle_miles(canonical_data, calculated_data):
    key = "productTransportByVehicleMiles"
    calculated_vehicle_types = []
    canonical_vehicle_types = []
    for i, canonical_row in enumerate(canonical_data[key]):
        source_id = canonical_row['sourceId']
        vehicle_type = canonical_row["vehicleType"]
        vehicle_miles = canonical_row["vehicleMiles"]
        co2_emissions = canonical_row["CO2"]
        ch4_emissions = canonical_row["CH4"]
        n2o_emissions = canonical_row["N2O"]
        canonical_vehicle_types.append(vehicle_type)

        calculated_row = calculated_data._output[key][i]
        calculated_source_id = calculated_row['sourceId']
        calculated_vehicle_type = calculated_row['vehicleType']
        calculated_vehicle_miles = calculated_row['vehicleMiles']

        if source_id == calculated_source_id and vehicle_type == calculated_vehicle_type \
                and vehicle_miles == calculated_vehicle_miles:
            assert co2_emissions == calculated_row["CO2"]
            assert ch4_emissions == calculated_row["CH4"]
            assert n2o_emissions == calculated_row["N2O"]
            calculated_vehicle_types.append(calculated_vehicle_type)
    assert calculated_vehicle_types == canonical_vehicle_types

    calculated_vehicle_types_all = []
    for row in calculated_data._output[key]:
        calculated_vehicle_types_all.append(row['vehicleType'])

    assert calculated_vehicle_types_all == canonical_vehicle_types


def test_make_total_by_vehicle_miles(canonical_data, calculated_data):
    key = 'totalForProductTransportByVehicleMiles'
    canonical_values = canonical_data[key]
    calculated_values = calculated_data._output[key]
    for gas in canonical_values:
        assert canonical_values[gas] == calculated_values[gas]
    assert canonical_values.keys() == calculated_values.keys()


def test_make_product_transport_by_short_ton_miles(canonical_data, calculated_data):
    key = "productTransportByTonMiles"
    calculated_vehicle_types = []
    canonical_vehicle_types = []
    for i, canonical_row in enumerate(canonical_data[key]):
        source_id = canonical_row['sourceId']
        vehicle_type = canonical_row["vehicleType"]
        short_ton_miles = canonical_row["shortTonMiles"]
        co2_emissions = canonical_row["CO2"]
        ch4_emissions = canonical_row["CH4"]
        n2o_emissions = canonical_row["N2O"]
        canonical_vehicle_types.append(vehicle_type)

        calculated_row = calculated_data._output[key][i]
        calculated_source_id = calculated_row['sourceId']
        calculated_vehicle_type = calculated_row['vehicleType']
        calculated_short_ton_miles = calculated_row['shortTonMiles']

        if source_id == calculated_source_id and vehicle_type == calculated_vehicle_type \
                and short_ton_miles == calculated_short_ton_miles:
            assert co2_emissions == calculated_row["CO2"]
            assert ch4_emissions == calculated_row["CH4"]
            assert n2o_emissions == calculated_row["N2O"]
            calculated_vehicle_types.append(calculated_vehicle_type)
    assert calculated_vehicle_types == canonical_vehicle_types

    calculated_vehicle_types_all = []
    for row in calculated_data._output[key]:
        calculated_vehicle_types_all.append(row['vehicleType'])

    assert calculated_vehicle_types_all == canonical_vehicle_types


def test_make_total_by_ton_miles(canonical_data, calculated_data):
    key = 'totalForAllProductTransportByTonMiles'
    canonical_values = canonical_data[key]
    calculated_values = calculated_data._output[key]
    for gas in canonical_values:
        assert canonical_values[gas] == calculated_values[gas]
    assert canonical_values.keys() == calculated_values.keys()


def test_make_total_emissions_by_product_transport_type(canonical_data, calculated_data):
    key = "totalEmissionsByProductTransportType"
    calculated_transport_types = []
    canonical_transport_types = []
    for canonical_row in canonical_data[key]:
        transport_type = canonical_row["transportType"]
        co2_emissions = canonical_row["CO2"]
        ch4_emissions = canonical_row["CH4"]
        n2o_emissions = canonical_row["N2O"]
        canonical_transport_types.append(transport_type)

        for calculated_row in calculated_data._output[key]:
            calculated_transport_type = calculated_row['transportType']

            if transport_type == calculated_transport_type:
                assert co2_emissions == calculated_row["CO2"]
                assert ch4_emissions == calculated_row["CH4"]
                assert n2o_emissions == calculated_row["N2O"]
                calculated_transport_types.append(calculated_transport_type)
    assert calculated_transport_types == canonical_transport_types

    calculated_transport_type_all = []
    for row in calculated_data._output[key]:
        calculated_transport_type_all.append(row['transportType'])

    assert sorted(calculated_transport_type_all) == sorted(canonical_transport_types)


def test_make_co2_equivalent_emissions(canonical_data, calculated_data):
    key = "totalCo2EquivalentEmissions"
    assert abs(canonical_data[key] - calculated_data._output[key]) < 0.00001


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


def test_output_schema_compliance(calculated_data, canonical_data, product_transport_schema):
    output = calculated_data.to_dict()
    output['version'] = canonical_data['version']
    product_transport_schema.validate(output)
