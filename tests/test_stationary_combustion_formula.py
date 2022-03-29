import pytest
import json
import os

from atomic6ghg.formulas import StationaryCombustion


@pytest.fixture
def canonical_data():
    TEST_FILENAME = os.path.join(os.path.dirname(__file__), './fixtures/stationary_combustion_canonical_instance.json')
    with open(TEST_FILENAME, 'r', encoding='utf-8') as canonical_instance:
        stationary_combustion_document = json.load(canonical_instance)
        return stationary_combustion_document


@pytest.fixture
def calculated_data(canonical_data):
    stationary_combustion = StationaryCombustion(wks_data=canonical_data)
    return stationary_combustion


def test_quantity_combusted(canonical_data, calculated_data):
    key = "totalStationarySourceCombustion"
    canonical_fuel_types = set()
    calculated_fuel_types = set()
    for canonical_row in canonical_data[key]:
        fuel_type = canonical_row["fuelType"]
        quantity_combusted = canonical_row['quantityCombusted']
        for calculated_row in calculated_data._output[key]:
            calculated_fuel_type = calculated_row['fuelType']
            if calculated_row['fuelType'] == fuel_type:
                assert quantity_combusted == calculated_row["quantityCombusted"]
            calculated_fuel_types.add(calculated_fuel_type)
        canonical_fuel_types.add(fuel_type)
    assert calculated_fuel_types == canonical_fuel_types


def test_emissions(canonical_data, calculated_data):
    key = "totalGhgEmissionsFromStationarySourceFuelCombustion"
    canonical_fuel_types = set()
    calculated_fuel_types = set()
    for canonical_row in canonical_data[key]:
        fuel_type = canonical_row["fuelType"]
        co2 = canonical_row['CO2']
        ch4 = canonical_row['CH4']
        n2o = canonical_row['N2O']
        for calculated_row in calculated_data._output[key]:
            calculated_fuel_type = calculated_row['fuelType']
            if calculated_row['fuelType'] == fuel_type:
                assert co2 == calculated_row["CO2"]
                assert ch4 == calculated_row["CH4"]
                assert n2o == calculated_row["N2O"]
            calculated_fuel_types.add(calculated_fuel_type)
        canonical_fuel_types.add(fuel_type)
    assert calculated_fuel_types == canonical_fuel_types


def test_co2_emissions(canonical_data, calculated_data):
    key = "totalCO2EquivalentEmissions"
    assert canonical_data[key] == calculated_data._output[key]


def test_biomass_co2_emissions(canonical_data, calculated_data):
    key = "totalBiomassEquivalentEmissions"
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


def test_output_schema_compliance(calculated_data, canonical_data, stationary_combustion_schema):
    output = calculated_data.to_dict()
    output['version'] = canonical_data['version']
    stationary_combustion_schema.validate(output)
