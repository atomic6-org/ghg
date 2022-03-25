"""test"""
import json
import jsonschema
import pytest
import os


def test_minimum_required(steam_schema):
    """test"""
    minimum_steam_document = json.loads(
        """
        {
            "version": "steam.1.0.0", 
            "emissionFactorDataForSteamPurchased": []
        }
        """
    )

    steam_schema.validate(minimum_steam_document)


def utility_get_document(source_area, boiler_efficiency, steam_purchased, location_based_emission_factors_co2_factor,
                         location_based_emission_factors_ch4_factor, location_based_emission_factors_n2o_factor,
                         location_based_emissions_co2_emissions, location_based_emissions_ch4_emissions,
                         location_based_emissions_n2o_emissions, market_based_emission_factors_co2_factor,
                         market_based_emission_factors_ch4_factor, market_based_emission_factors_n2o_factor,
                         market_based_emissions_co2_emissions, market_based_emissions_ch4_emissions,
                         market_based_emissions_n2o_emissions):
    return {
            "version": "steam.1.0.0",
            "emissionFactorDataForSteamPurchased": [
                {
                    "sourceId": "Source ID",
                    "sourceDescription": "Source Description",
                    "sourceArea": source_area,
                    "fuelType": "anthraciteCoal",
                    "boilerEfficiency": boiler_efficiency,
                    "steamPurchased": steam_purchased,
                    "locationBasedEmissionFactorsCO2Factor": location_based_emission_factors_co2_factor,
                    "locationBasedEmissionFactorsCH4Factor": location_based_emission_factors_ch4_factor,
                    "locationBasedEmissionFactorsN2OFactor": location_based_emission_factors_n2o_factor,
                    "locationBasedEmissionsCO2Emissions": location_based_emissions_co2_emissions,
                    "locationBasedEmissionsCH4Emissions": location_based_emissions_ch4_emissions,
                    "locationBasedEmissionsN2OEmissions": location_based_emissions_n2o_emissions,
                    "marketBasedEmissionFactorsCO2Factor": market_based_emission_factors_co2_factor,
                    "marketBasedEmissionFactorsCH4Factor": market_based_emission_factors_ch4_factor,
                    "marketBasedEmissionFactorsN2OFactor": market_based_emission_factors_n2o_factor,
                    "marketBasedEmissionsCO2Emissions": market_based_emissions_co2_emissions,
                    "marketBasedEmissionsCH4Emissions": market_based_emissions_ch4_emissions,
                    "marketBasedEmissionsN2OEmissions": market_based_emissions_n2o_emissions
                }
            ]
        }


def test_with_valid_number_inputs(steam_schema):
    """test"""
    minimum_steam_document = utility_get_document(1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1)

    steam_schema.validate(minimum_steam_document)


def test_with_valid_null_inputs(steam_schema):
    """test"""
    minimum_steam_document = utility_get_document(None, None, None, None, None, None, None, None, None,
                                                        None, None, None, None, None, None)

    steam_schema.validate(minimum_steam_document)


def test_with_invalid_inputs(steam_schema):
    """test"""
    minimum_steam_document = utility_get_document("", "", "", "", "", "", "", "", "", "", "", "", "", "", "")

    with pytest.raises(jsonschema.exceptions.ValidationError):
        steam_schema.validate(minimum_steam_document)


def test_canonical_instance(steam_schema):
    """test"""
    TEST_FILENAME = os.path.join(os.path.dirname(__file__), './fixtures/steam_canonical_instance.json')
    with open(TEST_FILENAME, 'r', encoding='utf-8') as canonical_instance:
        canonical_steam_document = json.load(canonical_instance)
        steam_schema.validate(canonical_steam_document)
