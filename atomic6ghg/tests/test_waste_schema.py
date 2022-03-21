"""test"""
import json
import jsonschema
import pytest


def test_minimum_required(waste_schema):
    """test"""
    minimum_waste_document = json.loads(
        """
        { 
            "version": "waste.1.0.0", 
            "wasteDisposal": [] 
        }
        """
    )

    waste_schema.validate(minimum_waste_document)


def utility_get_document(weight, co2):
    return {
            "version": "waste.1.0.0",
            "wasteDisposal": [
                {
                    "sourceId": "Source ID",
                    "sourceDescription": "Source description",
                    "wasteMaterial": "aluminumCans",
                    "disposalMethod": "recycled",
                    "weight": weight,
                    "unit": "gram",
                    "CO2Emissions": co2
                }
            ]
        }


def test_with_valid_number_waste(waste_schema):
    """Test"""
    minimum_waste_document = utility_get_document(0, 0)

    waste_schema.validate(minimum_waste_document)


def test_with_valid_null_waste(waste_schema):
    """Test"""
    minimum_waste_document = utility_get_document(None, None)

    waste_schema.validate(minimum_waste_document)


def test_with_invalid_waste_schema(waste_schema):
    """Test"""
    minimum_waste_document = utility_get_document("", "")

    with pytest.raises(jsonschema.exceptions.ValidationError):
        waste_schema.validate(minimum_waste_document)


def test_canonical_instance(waste_schema):
    """test"""
    with open("./tests/fixtures/waste_canonical_instance.json", 'r', encoding='utf-8') as \
            canonical_instance:
        canonical_waste_document = json.load(canonical_instance)
        waste_schema.validate(canonical_waste_document)