"""test"""
import json
import jsonschema
import pytest
import os


def test_minimum_required(business_travel_schema):
    """test"""
    minimum_business_travel_document = json.loads(
        """
        { 
            "version": "business-travel.1.0.0", 
            "personalVehicleRentalCarOrTaxiBusinessTravel": [] 
        }
        """
    )

    business_travel_schema.validate(minimum_business_travel_document)


def utility_get_document(vehicle_miles, co2, ch4, n2o):
    return {
            "version": "business-travel.1.0.0",
            "personalVehicleRentalCarOrTaxiBusinessTravel": [
                {
                    "sourceId": "Source ID Sample",
                    "sourceDescription": "Awesome source description",
                    "vehicleType": "passengerCars",
                    "vehicleMiles": vehicle_miles,
                    "CO2": co2,
                    "CH4": ch4,
                    "N2O": n2o
                }
            ]
        }


def test_with_valid_number_business_travel(business_travel_schema):
    """Test"""
    minimum_business_travel_document = utility_get_document(20, 1, 1, 1)

    business_travel_schema.validate(minimum_business_travel_document)


def test_with_valid_null_business_travel(business_travel_schema):
    """Test"""
    minimum_business_travel_document = utility_get_document(None, None, None, None)

    business_travel_schema.validate(minimum_business_travel_document)


def test_with_invalid_business_travel_schema(business_travel_schema):
    """Test"""
    minimum_business_travel_document = utility_get_document("", "", "", "")

    with pytest.raises(jsonschema.exceptions.ValidationError):
        business_travel_schema.validate(minimum_business_travel_document)


def test_canonical_instance(business_travel_schema):
    """test"""
    TEST_FILENAME = os.path.join(os.path.dirname(__file__), './fixtures/business_travel_canonical_instance.json')
    with open(TEST_FILENAME, 'r', encoding='utf-8') as canonical_instance:
        canonical_business_travel_document = json.load(canonical_instance)
        business_travel_schema.validate(canonical_business_travel_document)