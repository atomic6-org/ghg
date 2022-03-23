"""test"""
import json
import jsonschema
import pytest
import os


def test_minimum_required(product_transport_schema):
    """test"""
    minimum_product_transport_document = json.loads(
        """
        { 
            "version": "product-transport.1.0.0", 
            "productTransportByVehicleMiles": [] 
        }
        """
    )

    product_transport_schema.validate(minimum_product_transport_document)


def utility_get_document(vehicle_miles, co2, ch4, n2o):
    return {
            "version": "product-transport.1.0.0",
            "productTransportByVehicleMiles": [
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


def test_with_valid_number_product_transport(product_transport_schema):
    """Test"""
    minimum_product_transport_document = utility_get_document(0, 0, 0, 0)

    product_transport_schema.validate(minimum_product_transport_document)


def test_with_valid_null_product_transport(product_transport_schema):
    """Test"""
    minimum_product_transport_document = utility_get_document(None, None, None, None)

    product_transport_schema.validate(minimum_product_transport_document)


def test_with_invalid_product_transport_schema(product_transport_schema):
    """Test"""
    minimum_product_transport_document = utility_get_document("", "", "", "")

    with pytest.raises(jsonschema.exceptions.ValidationError):
        product_transport_schema.validate(minimum_product_transport_document)


def test_canonical_instance(product_transport_schema):
    """test"""
    TEST_FILENAME = os.path.join(os.path.dirname(__file__), './fixtures/product_transport_canonical_instance.json')
    with open(TEST_FILENAME, 'r', encoding='utf-8') as canonical_instance:
        canonical_product_transport_document = json.load(canonical_instance)
        product_transport_schema.validate(canonical_product_transport_document)
