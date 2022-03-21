import pytest
import json

from atomic6ghg.formulas import Waste


@pytest.fixture
def canonical_data():
    with open("./tests/fixtures/waste_canonical_instance.json", 'r', encoding='utf-8') as canonical_instance:
        waste_document = json.load(canonical_instance)
        return waste_document


@pytest.fixture
def calculated_data(canonical_data):
    waste = Waste(wks_data=canonical_data)
    return waste


def test_make_waste_disposal(canonical_data, calculated_data):
    key = "wasteDisposal"
    calculated_waste_materials = []
    canonical_waste_materials = []
    for i, canonical_row in enumerate(canonical_data[key]):
        waste_material = canonical_row["wasteMaterial"]
        disposal_method = canonical_row["disposalMethod"]
        weight = canonical_row["weight"]
        unit = canonical_row["unit"]
        co2_emissions = canonical_row["CO2Emissions"]
        canonical_waste_materials.append(waste_material)

        calculated_row = calculated_data._output[key][i]
        calculated_waste_material = calculated_row['wasteMaterial']
        calculated_disposal_method = calculated_row['disposalMethod']
        calculated_weight = calculated_row['weight']
        calculated_unit = calculated_row['unit']

        if waste_material == calculated_waste_material and disposal_method == calculated_disposal_method \
                and weight == calculated_weight and unit == calculated_unit:
            assert abs(co2_emissions - calculated_row["CO2Emissions"]) < 0.0001
            calculated_waste_materials.append(calculated_waste_material)
    assert calculated_waste_materials == canonical_waste_materials

    calculated_waste_materials_all = []
    for row in calculated_data._output[key]:
        calculated_waste_materials_all.append(row['wasteMaterial'])

    assert calculated_waste_materials_all == canonical_waste_materials


def test_make_total_emissions_by_disposal_method(canonical_data, calculated_data):
    key = "totalEmissionsByDisposalMethod"
    calculated_waste_materials = []
    canonical_waste_materials = []
    for canonical_row in canonical_data[key]:
        waste_material = canonical_row["wasteMaterial"]
        co2_emissions = canonical_row["CO2"]
        canonical_waste_materials.append(waste_material)

        for calculated_row in calculated_data._output[key]:
            calculated_waste_material = calculated_row['wasteMaterial']

            if waste_material == calculated_waste_material:
                assert abs(co2_emissions - calculated_row["CO2"]) <  0.0001
                calculated_waste_materials.append(calculated_waste_material)
    assert calculated_waste_materials == canonical_waste_materials

    calculated_waste_materials_all = []
    for row in calculated_data._output[key]:
        calculated_waste_materials_all.append(row['wasteMaterial'])

    assert sorted(calculated_waste_materials_all) == sorted(canonical_waste_materials)


def test_make_co2_equivalent_emissions(canonical_data, calculated_data):
    key = "totalCo2EquivalentEmissions"
    assert abs(canonical_data[key] - calculated_data._output[key]) < 0.0001


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


def test_output_schema_compliance(calculated_data, canonical_data, waste_schema):
    output = calculated_data.to_dict()
    output['version'] = canonical_data['version']
    waste_schema.validate(output)