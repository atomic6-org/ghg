import pytest
import json
import os

from atomic6ghg.formulas import WasteGases
from atomic6ghg.formulas.waste_gases import null_replacer

@pytest.fixture
def canonical_data():
    TEST_FILENAME = os.path.join(os.path.dirname(__file__), './fixtures/waste_gases_canonical_instance.json')
    with open(TEST_FILENAME, 'r', encoding='utf-8') as canonical_instance:
        waste_gases_document = json.load(canonical_instance)
        return waste_gases_document


@pytest.fixture
def calculated_data(canonical_data):
    waste_gases = WasteGases(wks_data=canonical_data)
    return waste_gases


def test_make_waste_gases(canonical_data, calculated_data):
    key = "emissionFactorForGasWasteStream"
    calculated_gasses = []
    canonical_gasses = []
    for i, canonical_row in enumerate(canonical_data[key]):
        content = canonical_row["component"]
        chemical_formula = canonical_row["chemicalFormula"]
        molar_fraction = canonical_row['molarFraction']
        molecular_weight = canonical_row['molecularWeight']
        percent_carbon = canonical_row['percentCarbon']
        carbon_content = canonical_row['carbonContent']
        canonical_gasses.append(content)

        calculated_row = calculated_data._output[key][i]
        calculated_gas = calculated_row['component']

        if content == calculated_gas:
            assert chemical_formula == calculated_row['chemicalFormula']
            if molar_fraction or calculated_row['molarFraction']:
                assert abs(molar_fraction - calculated_row['molarFraction']) < 0.0001
            assert molecular_weight == calculated_row['molecularWeight']
            assert percent_carbon == calculated_row['percentCarbon']
            assert carbon_content == calculated_row['carbonContent']
            calculated_gasses.append(calculated_gas)
    assert calculated_gasses == canonical_gasses

    calculated_gasses_all = []
    for row in calculated_data._output[key]:
        calculated_gasses_all.append(row['component'])

    assert calculated_gasses_all == canonical_gasses


def test_make_total_all_components(canonical_data, calculated_data):
    key = 'totalForAllComponents'
    canonical_values = canonical_data[key]
    calculated_values = calculated_data._output[key]
    for k in canonical_values:
        assert abs(canonical_values[k] - calculated_values[k]) < 0.000001
    assert canonical_values.keys() == calculated_values.keys()


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


def test_output_schema_compliance(calculated_data, canonical_data, waste_gases_schema):
    output = calculated_data.to_dict()
    output['version'] = canonical_data['version']
    waste_gases_schema.validate(output)
