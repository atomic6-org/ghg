"""test"""
import json
import jsonschema
import pytest
import os


def test_minimum_required(commuting_schema):
    """test"""
    minimum_commuting_document = json.loads(
        """
        { 
            "version": "commuting.1.0.0", 
            "personalVehicle": [] 
        }
        """
    )

    commuting_schema.validate(minimum_commuting_document)


def utility_get_document(vehicle_miles, co2, ch4, n2o):
    return {
            "version": "commuting.1.0.0",
            "personalVehicle": [
                {
                    "sourceId": "Source ID",
                    "sourceDescription": "Source description",
                    "vehicleType": "passengerCars",
                    "vehicleMiles": vehicle_miles,
                    "CO2": co2,
                    "CH4": ch4,
                    "N2O": n2o
                }
            ]
        }


def test_with_valid_number_commuting(commuting_schema):
    """Test"""
    minimum_commuting_document = utility_get_document(0, 0, 0, 0)

    commuting_schema.validate(minimum_commuting_document)


def test_with_valid_null_commuting(commuting_schema):
    """Test"""
    minimum_commuting_document = utility_get_document(None, None, None, None)

    commuting_schema.validate(minimum_commuting_document)


def test_with_invalid_commuting_schema(commuting_schema):
    """Test"""
    minimum_commuting_document = utility_get_document("", "", "", "")

    with pytest.raises(jsonschema.exceptions.ValidationError):
        commuting_schema.validate(minimum_commuting_document)


def test_canonical_instance(commuting_schema):
    """test"""
    TEST_FILENAME = os.path.join(os.path.dirname(__file__), './fixtures/commuting_canonical_instance.json')
    with open(TEST_FILENAME, 'r', encoding='utf-8') as canonical_instance:
        canonical_commuting_document = json.load(canonical_instance)
        commuting_schema.validate(canonical_commuting_document)
