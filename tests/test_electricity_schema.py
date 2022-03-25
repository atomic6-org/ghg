"""test"""
import json
import jsonschema
import pytest
import os

def test_minimum_required(electricity_schema):
    """test"""
    minimum_electricity_document = json.loads(
        """
        {
            "version": "electricity.1.0.0", 
            "totalElectricityPurchased": []
        }
        """
    )

    electricity_schema.validate(minimum_electricity_document)


def utility_get_document(source_area, electricity_purchased, market_based_emission_factors_co2_emissions,
                         market_based_emission_factors_ch4_emissions, market_based_emission_factors_n2o_emissions,
                         market_based_emissions_co2_emissions, market_based_emissions_ch4_emissions,
                         market_based_emissions_n2o_emissions, location_based_emissions_co2_emissions,
                         location_based_emissions_ch4_emissions, location_based_emissions_n2o_emissions):
    return {
            "version": "electricity.1.0.0",
            "totalElectricityPurchased": [
                {
                    "sourceId": "Source ID",
                    "sourceDescription": "Source Description",
                    "sourceArea": source_area,
                    "eGridSubregion": "akgd",
                    "electricityPurchased": electricity_purchased,
                    "marketBasedEmissionFactorsCO2Emissions": market_based_emission_factors_co2_emissions,
                    "marketBasedEmissionFactorsCH4Emissions": market_based_emission_factors_ch4_emissions,
                    "marketBasedEmissionFactorsN2OEmissions": market_based_emission_factors_n2o_emissions,
                    "marketBasedEmissionsCO2Emissions": market_based_emissions_co2_emissions,
                    "marketBasedEmissionsCH4Emissions": market_based_emissions_ch4_emissions,
                    "marketBasedEmissionsN2OEmissions": market_based_emissions_n2o_emissions,
                    "locationBasedEmissionsCO2Emissions": location_based_emissions_co2_emissions,
                    "locationBasedEmissionsCH4Emissions": location_based_emissions_ch4_emissions,
                    "locationBasedEmissionsN2OEmissions": location_based_emissions_n2o_emissions
                }
            ]
        }


def test_with_valid_number_gas_gwp(electricity_schema):
    """test"""
    minimum_electricity_document = utility_get_document(1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1)

    electricity_schema.validate(minimum_electricity_document)


def test_with_valid_null_gas_gwp(electricity_schema):
    """test"""
    minimum_electricity_document = utility_get_document(None, None, None, None, None, None, None, None, None,
                                                        None, None)

    electricity_schema.validate(minimum_electricity_document)


def test_with_invalid_gas_gwp(electricity_schema):
    """test"""
    minimum_electricity_document = utility_get_document("", "", "", "", "", "", "", "", "", "", "")

    with pytest.raises(jsonschema.exceptions.ValidationError):
        electricity_schema.validate(minimum_electricity_document)


def test_canonical_instance(electricity_schema):
    """test"""
    TEST_FILENAME = os.path.join(os.path.dirname(__file__), './fixtures/electricity_canonical_instance.json')
    with open(TEST_FILENAME, 'r', encoding='utf-8') as canonical_instance:
        canonical_electricity_document = json.load(canonical_instance)
        electricity_schema.validate(canonical_electricity_document)
