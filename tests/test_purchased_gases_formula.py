import pytest
import json
import os

from atomic6ghg.formulas import PurchasedGases
from atomic6ghg.formulas.purchased_gases import null_replacer


@pytest.fixture
def canonical_data():
    TEST_FILENAME = os.path.join(os.path.dirname(__file__), './fixtures/purchased_gases_canonical_instance.json')
    with open(TEST_FILENAME, 'r', encoding='utf-8') as canonical_instance:
        purchased_gases_document = json.load(canonical_instance)
        return purchased_gases_document


@pytest.fixture
def calculated_data(canonical_data):
    purchased_gases = PurchasedGases(wks_data=canonical_data)
    return purchased_gases


def make_purchased_gases(canonical_data, calculated_data):
    key = "purchasedGases"
    calculated_gasses = []
    canonical_gasses = []
    for i, canonical_row in enumerate(canonical_data[key]):
        gas = canonical_row["gas"]
        gas_gwp = canonical_row["gasGWP"]
        purchased_amount = null_replacer(canonical_row['purchasedAmount'])
        co2_equivalent_emissions = null_replacer(canonical_row['CO2EquivalentEmissions'])
        canonical_gasses.append(gas)

        calculated_row = calculated_data._output[key][i]
        calculated_gas = calculated_row['gas']
        calculated_purchased_amount = canonical_row['purchasedAmount']

        if gas == calculated_gas and purchased_amount == calculated_purchased_amount:
            assert co2_equivalent_emissions == calculated_row["CO2EquivalentEmissions"]
            assert gas_gwp == calculated_row["gasGWP"]
            calculated_gasses.append(calculated_gas)
    assert calculated_gasses == canonical_gasses

    calculated_gasses_all = []
    for row in calculated_data._output[key]:
        calculated_gasses_all.append(row['gas'])

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


def test_output_schema_compliance(calculated_data, canonical_data, purchased_gases_schema):
    output = calculated_data.to_dict()
    output['version'] = canonical_data['version']
    purchased_gases_schema.validate(output)
