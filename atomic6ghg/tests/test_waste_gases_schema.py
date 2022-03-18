"""test"""
import json
import jsonschema
import pytest


def test_minimum_required(waste_gases_schema):
    """test"""
    minimum_waste_gases_document = json.loads(
        """
        {
            "version": "waste-gases.1.0.0",
            "wasteStreamGasCombusted": 5000.0,
            "gasTotalNumberOfMolesPerUnitVolume": null,
            "emissionFactorForGasWasteStream": [],
            "oxidationFactor": null
        }
        """
    )

    waste_gases_schema.validate(minimum_waste_gases_document)


def utility_get_document(molarFraction):
    return {
            "version": "waste-gases.1.0.0",
            "wasteStreamGasCombusted": 5000.0,
            "gasTotalNumberOfMolesPerUnitVolume": None,
            "emissionFactorForGasWasteStream": [
                {
                    "component": "Carbon Monoxide",
                    "chemicalFormula": "CO",
                    "molarFraction": molarFraction,
                    "totalMoles": 0.00051,
                    "molecularWeight": 28,
                    "percentCarbon": 43,
                    "carbonContent": 0.0061
                }
            ],
            "oxidationFactor": None
        }


def test_with_valid_number_emission_factors_for_gas_waste_stream(waste_gases_schema):
    """Test"""
    minimum_waste_gases_document = utility_get_document(20)

    waste_gases_schema.validate(minimum_waste_gases_document)


def test_with_valid_null_emission_factors_for_gas_waste_stream(waste_gases_schema):
    """Test"""
    minimum_waste_gases_document = utility_get_document(None)

    waste_gases_schema.validate(minimum_waste_gases_document)


def test_with_invalid_emission_factors_for_gas_waste_stream(waste_gases_schema):
    """Test"""
    minimum_waste_gases_document = utility_get_document("")

    with pytest.raises(jsonschema.exceptions.ValidationError):
        waste_gases_schema.validate(minimum_waste_gases_document)


def test_canonical_instance(waste_gases_schema):
    """test"""
    with open("./tests/fixtures/waste_gases_canonical_instance.json", 'r', encoding='utf-8') as \
            canonical_instance:
        canonical_waste_gases_document = json.load(canonical_instance)
        waste_gases_schema.validate(canonical_waste_gases_document)