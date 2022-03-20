import pytest
import json

from atomic6ghg.formulas import Steam, null_replacer


@pytest.fixture
def canonical_data():
    with open("./tests/fixtures/steam_canonical_instance.json", 'r', encoding='utf-8') as canonical_instance:
        steam_document = json.load(canonical_instance)
        return steam_document


@pytest.fixture
def calculated_data(canonical_data):
    steam = Steam(wks_data=canonical_data)
    return steam


def test_make_emission_factor_data_for_steam_purchased(canonical_data, calculated_data):
    key = "emissionFactorDataForSteamPurchased"
    calculated_fuel_types = []
    canonical_fuel_types = []
    for i, canonical_row in enumerate(canonical_data[key]):
        fuel_type = canonical_row["fuelType"]
        steam_purchased = canonical_row["steamPurchased"]
        boiler_efficiency = null_replacer(canonical_row['boilerEfficiency'])
        market_based_emissions_co2_emissions = canonical_row["marketBasedEmissionsCO2Emissions"]
        market_based_emissions_ch4_emissions = canonical_row["marketBasedEmissionsCH4Emissions"]
        market_based_emissions_n2o_emissions = canonical_row["marketBasedEmissionsN2OEmissions"]
        location_based_emissions_co2_emissions = canonical_row["locationBasedEmissionsCO2Emissions"]
        location_based_emissions_ch4_emissions = canonical_row["locationBasedEmissionsCH4Emissions"]
        location_based_emissions_n2o_emissions = canonical_row["locationBasedEmissionsN2OEmissions"]

        canonical_fuel_types.append(fuel_type)

        calculated_row = calculated_data._output[key][i]
        calculated_fuel_type = calculated_row['fuelType']
        calculated_purchased_steam = calculated_row['steamPurchased']
        calculated_boiler_efficiency = null_replacer(calculated_row['boilerEfficiency'])

        if fuel_type == calculated_fuel_type and steam_purchased == calculated_purchased_steam \
                and boiler_efficiency == calculated_boiler_efficiency:
            assert abs(market_based_emissions_co2_emissions - calculated_row["marketBasedEmissionsCO2Emissions"]) \
                   < 0.0001
            assert abs(market_based_emissions_ch4_emissions - calculated_row["marketBasedEmissionsCH4Emissions"]) \
                   < 0.0001
            assert abs(market_based_emissions_n2o_emissions - calculated_row["marketBasedEmissionsN2OEmissions"]) \
                   < 0.0001
            assert abs(location_based_emissions_co2_emissions - calculated_row["locationBasedEmissionsCO2Emissions"]) \
                   < 0.0001
            assert abs(location_based_emissions_ch4_emissions - calculated_row["locationBasedEmissionsCH4Emissions"]) \
                   < 0.0001
            assert abs(location_based_emissions_n2o_emissions - calculated_row["locationBasedEmissionsN2OEmissions"]) \
                   < 0.0001
            calculated_fuel_types.append(calculated_fuel_type)
    assert calculated_fuel_types == canonical_fuel_types

    calculated_fuel_types_all = []
    for row in calculated_data._output[key]:
        calculated_fuel_types_all.append(row['fuelType'])

    assert calculated_fuel_types_all == canonical_fuel_types


def test_make_emissions_by_source_and_fuel_type(canonical_data, calculated_data):
    key = "emissionsBySourceAndFuelType"
    calculated_fuel_types = []
    canonical_fuel_types = []
    for canonical_row in canonical_data[key]:
        fuel_type = canonical_row["fuelType"]
        market_based_co2_emissions = canonical_row["locationBasedCO2Emissions"]
        market_based_ch4_emissions = canonical_row["locationBasedCH4Emissions"]
        market_based_n2o_emissions = canonical_row["locationBasedN2OEmissions"]
        location_based_co2_emissions = canonical_row["marketBasedCO2Emissions"]
        location_based_ch4_emissions = canonical_row["marketBasedCH4Emissions"]
        location_based_n2o_emissions = canonical_row["marketBasedN2OEmissions"]

        canonical_fuel_types.append(fuel_type)

        for calculated_row in calculated_data._output[key]:
            calculated_fuel_type = calculated_row['fuelType']

            if fuel_type == calculated_fuel_type:
                assert abs(market_based_co2_emissions - calculated_row["locationBasedCO2Emissions"]) < 0.0001
                assert abs(market_based_ch4_emissions - calculated_row["locationBasedCH4Emissions"]) < 0.0001
                assert abs(market_based_n2o_emissions - calculated_row["locationBasedN2OEmissions"]) < 0.0001
                assert abs(location_based_co2_emissions - calculated_row["marketBasedCO2Emissions"]) < 0.0001
                assert abs(location_based_ch4_emissions - calculated_row["marketBasedCH4Emissions"]) < 0.0001
                assert abs(location_based_n2o_emissions - calculated_row["marketBasedN2OEmissions"]) < 0.0001
                calculated_fuel_types.append(calculated_fuel_type)
    assert calculated_fuel_types == canonical_fuel_types

    calculated_fuel_types_all = set()
    for row in calculated_data._output[key]:
        calculated_fuel_types_all.add(row['fuelType'])

    assert calculated_fuel_types_all == set(canonical_fuel_types)


def test_make_co2_equivalent_emissions_location_based(canonical_data, calculated_data):
    key = "CO2EquivalentEmissionsLocationBasedElectricityEmissions"
    assert abs(null_replacer(canonical_data[key]) - calculated_data._output[key]) < 0.0001


def test_make_co2_equivalent_emissions_market_based(canonical_data, calculated_data):
    key = "CO2EquivalentEmissionsMarketBasedElectricityEmissions"
    assert abs(null_replacer(canonical_data[key]) - calculated_data._output[key]) < 0.0001


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


def test_output_schema_compliance(calculated_data, canonical_data, steam_schema):
    output = calculated_data.to_dict()
    output['version'] = canonical_data['version']
    steam_schema.validate(output)
