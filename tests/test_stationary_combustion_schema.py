"""test"""
import json
import jsonschema
import pytest
import os


def test_minimum_required(stationary_combustion_schema):
    """test"""
    minimum_stationary_combustion_document = json.loads(
        "{ \
            \"version\": \"stationary-combustion.1.0.0\", \
            \"stationarySourceFuelConsumption\": [] \
        }"
    )

    stationary_combustion_schema.validate(minimum_stationary_combustion_document)


def utility_get_document(source_area, quantity_combusted):
    return {
            "version": "stationary-combustion.1.0.0",
            "stationarySourceFuelConsumption": [
                {
                    "sourceId": "Source ID",
                    "sourceDescription": "Source Description",
                    "sourceArea": source_area,
                    "fuelCombusted": "anthraciteCoal",
                    "quantityCombusted": quantity_combusted,
                    "units": "mmbtu"
                }
            ]
        }


def test_with_valid_number_fuel_consumption(stationary_combustion_schema):
    """test"""
    minimum_stationary_combustion_document = utility_get_document(1, 1)

    stationary_combustion_schema.validate(minimum_stationary_combustion_document)


def test_with_valid_null_fuel_consumption(stationary_combustion_schema):
    """test"""
    minimum_stationary_combustion_document = utility_get_document(None, None)

    stationary_combustion_schema.validate(minimum_stationary_combustion_document)


def test_with_invalid_fuel_consumption(stationary_combustion_schema):
    """test"""
    minimum_stationary_combustion_document = utility_get_document("", "")

    with pytest.raises(jsonschema.exceptions.ValidationError):
        stationary_combustion_schema.validate(minimum_stationary_combustion_document)


def test_canonical_instance(stationary_combustion_schema):
    """test"""
    TEST_FILENAME = os.path.join(os.path.dirname(__file__), './fixtures/stationary_combustion_canonical_instance.json')
    with open(TEST_FILENAME, 'r', encoding='utf-8') as canonical_instance:
        canonical_stationary_combustion_document = json.load(canonical_instance)
        stationary_combustion_schema.validate(canonical_stationary_combustion_document)
