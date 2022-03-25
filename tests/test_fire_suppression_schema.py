"""test"""
import json
import jsonschema
import pytest
import os


def test_minimum_required(fire_suppression_schema):
    """test"""
    minimum_fire_suppression_document = json.loads(
        "{ \
            \"version\": \"fire-suppression.1.0.0\", \
            \"screeningMethod\": [] \
        }"
    )

    fire_suppression_schema.validate(minimum_fire_suppression_document)


def utility_get_document(gasGWP, unitsCapacity, co2EquivalentEmissions):
    return {
            "version": "fire-suppression.1.0.0",
            "screeningMethod": [
                {
                    "sourceId": "Source ID",
                    "typeOfEquipment": "fixed",
                    "gasType": "co2",
                    "gasGWP": gasGWP,
                    "unitsCapacity": unitsCapacity,
                    "co2EquivalentEmissions": co2EquivalentEmissions
                }
            ]
        }


def test_with_valid_number_gas_gwp(fire_suppression_schema):
    """test"""
    minimum_fire_suppression_document = utility_get_document(1, 1, 1)

    fire_suppression_schema.validate(minimum_fire_suppression_document)


def test_with_valid_null_gas_gwp(fire_suppression_schema):
    """test"""
    minimum_fire_suppression_document = utility_get_document(None, None, None)

    fire_suppression_schema.validate(minimum_fire_suppression_document)


def test_with_invalid_gas_gwp(fire_suppression_schema):
    """test"""
    minimum_fire_suppression_document = utility_get_document("", "", "")

    with pytest.raises(jsonschema.exceptions.ValidationError):
        fire_suppression_schema.validate(minimum_fire_suppression_document)


def test_canonical_instance(fire_suppression_schema):
    """test"""
    TEST_FILENAME = os.path.join(os.path.dirname(__file__), './fixtures/fire_suppression_canonical_instance.json')
    with open(TEST_FILENAME, 'r', encoding='utf-8') as canonical_instance:
        canonical_fire_suppression_document = json.load(canonical_instance)
        fire_suppression_schema.validate(canonical_fire_suppression_document)
