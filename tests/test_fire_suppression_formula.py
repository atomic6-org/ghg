import pytest
import json
import os

from atomic6ghg.formulas import FireSuppression, null_replacer


@pytest.fixture
def canonical_data():
    TEST_FILENAME = os.path.join(os.path.dirname(__file__), './fixtures/fire_suppression_canonical_instance.json')
    with open(TEST_FILENAME, 'r', encoding='utf-8') as canonical_instance:
        fire_suppression_document = json.load(canonical_instance)
        return fire_suppression_document


@pytest.fixture
def calculated_data(canonical_data):
    fire_suppression = FireSuppression(wks_data=canonical_data)
    return fire_suppression


def test_make_material_balance(canonical_data, calculated_data):
    key = "materialBalance"
    calculated_gasses = []
    canonical_gasses = []
    for i, canonical_row in enumerate(canonical_data[key]):
        gas = canonical_row["gas"]
        gas_gwp = canonical_row["gasGWP"]
        inventory_change = null_replacer(canonical_row['inventoryChange'])
        transferred_amount = null_replacer(canonical_row['transferredAmount'])
        capacity_change = null_replacer(canonical_row['capacityChange'])
        co2_equivalent_emissions = null_replacer(canonical_row['CO2EquivalentEmissions'])
        canonical_gasses.append(gas)

        calculated_row = calculated_data._output[key][i]
        calculated_gas = calculated_row['gas']
        calculated_inventory_change = canonical_row['inventoryChange']
        calculated_transferred_amount = canonical_row['transferredAmount']
        calculated_capacity_change = canonical_row['capacityChange']

        if gas == calculated_gas and inventory_change == calculated_inventory_change and \
            transferred_amount == calculated_transferred_amount and capacity_change == calculated_capacity_change:
            assert co2_equivalent_emissions == calculated_row["CO2EquivalentEmissions"]
            assert gas_gwp == calculated_row["gasGWP"]
            calculated_gasses.append(calculated_gas)
    assert calculated_gasses == canonical_gasses

    calculated_gasses_all = []
    for row in calculated_data._output[key]:
        calculated_gasses_all.append(row['gas'])

    assert calculated_gasses_all == canonical_gasses


def test_make_simplified_material_balance(canonical_data, calculated_data):
    key = "simplifiedMaterialBalance"
    calculated_gasses = []
    canonical_gasses = []
    for i, canonical_row in enumerate(canonical_data[key]):
        gas = canonical_row["gas"]
        gas_gwp = canonical_row["gasGWP"]
        new_units_charge = null_replacer(canonical_row['newUnitsCharge'])
        new_units_capacity = null_replacer(canonical_row['newUnitsCapacity'])
        existing_units_recharge = null_replacer(canonical_row['existingUnitsRecharge'])
        disposed_units_capacity = null_replacer(canonical_row['disposedUnitsCapacity'])
        disposed_units_recovered = null_replacer(canonical_row['disposedUnitsRecovered'])
        co2_equivalent_emissions = null_replacer(canonical_row['CO2EquivalentEmissions'])
        canonical_gasses.append(gas)

        calculated_row = calculated_data._output[key][i]
        calculated_gas = calculated_row['gas']
        calculated_new_units_charge = canonical_row['newUnitsCharge']
        calculated_new_units_capacity = canonical_row['newUnitsCapacity']
        calculated_existing_units_recharge = canonical_row['existingUnitsRecharge']
        calculated_disposed_units_capacity = canonical_row['disposedUnitsCapacity']
        calculated_disposed_units_recovered = canonical_row['disposedUnitsRecovered']

        if gas == calculated_gas and new_units_charge == calculated_new_units_charge and \
            new_units_capacity == calculated_new_units_capacity and \
                existing_units_recharge == calculated_existing_units_recharge and \
                disposed_units_capacity == calculated_disposed_units_capacity and \
                disposed_units_recovered == calculated_disposed_units_recovered:
            assert co2_equivalent_emissions == calculated_row["CO2EquivalentEmissions"]
            assert gas_gwp == calculated_row["gasGWP"]
            calculated_gasses.append(calculated_gas)
    assert calculated_gasses == canonical_gasses

    calculated_gasses_all = []
    for row in calculated_data._output[key]:
        calculated_gasses_all.append(row['gas'])

    assert calculated_gasses_all == canonical_gasses


def test_make_screening_method(canonical_data, calculated_data):
    key = "screeningMethod"
    calculated_gasses = []
    canonical_gasses = []
    for i, canonical_row in enumerate(canonical_data[key]):
        gas_type = canonical_row["gasType"]
        gas_gwp = canonical_row["gasGWP"]
        unit_capacity = null_replacer(canonical_row['unitsCapacity'])
        co2_equivalent_emissions = null_replacer(canonical_row['CO2EquivalentEmissions'])
        canonical_gasses.append(gas_type)

        calculated_row = calculated_data._output[key][i]
        calculated_gas = calculated_row['gasType']
        calculated_unit_capacity = canonical_row['unitsCapacity']

        if gas_type == calculated_gas and unit_capacity == calculated_unit_capacity:
            assert co2_equivalent_emissions == calculated_row["CO2EquivalentEmissions"]
            assert gas_gwp == calculated_row["gasGWP"]
            calculated_gasses.append(calculated_gas)
    assert calculated_gasses == canonical_gasses

    calculated_gasses_all = []
    for row in calculated_data._output[key]:
        calculated_gasses_all.append(row['gasType'])

    assert calculated_gasses_all == canonical_gasses


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


def test_output_schema_compliance(calculated_data, canonical_data, fire_suppression_schema):
    output = calculated_data.to_dict()
    output['version'] = canonical_data['version']
    fire_suppression_schema.validate(output)
