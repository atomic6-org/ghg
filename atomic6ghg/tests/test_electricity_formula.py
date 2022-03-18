import pytest
import json

from atomic6ghg.formulas import Electricity, null_replacer

@pytest.fixture
def canonical_data():
    with open("./tests/fixtures/electricity_canonical_instance.json", 'r', encoding='utf-8') as canonical_instance:
        electricity_document = json.load(canonical_instance)
        return electricity_document


@pytest.fixture
def calculated_data(canonical_data):
    electricity = Electricity(wks_data=canonical_data)
    return electricity


def test_make_electricity(canonical_data, calculated_data):
    key = "totalElectricityPurchased"
    calculated_subregions = []
    canonical_subregions = []
    for i, canonical_row in enumerate(canonical_data[key]):
        subregion = canonical_row["eGridSubregion"]
        electricity_purchased = canonical_row["electricityPurchased"]
        market_based_emissions_co2_emissions = canonical_row["marketBasedEmissionsCO2Emissions"]
        market_based_emissions_ch4_emissions = canonical_row["marketBasedEmissionsCH4Emissions"]
        market_based_emissions_n2o_emissions = canonical_row["marketBasedEmissionsN2OEmissions"]
        location_based_emissions_co2_emissions = canonical_row["locationBasedEmissionsCO2Emissions"]
        location_based_emissions_ch4_emissions = canonical_row["locationBasedEmissionsCH4Emissions"]
        location_based_emissions_n2o_emissions = canonical_row["locationBasedEmissionsN2OEmissions"]

        canonical_subregions.append(subregion)

        calculated_row = calculated_data._output[key][i]
        calculated_subregion = calculated_row['eGridSubregion']
        calculated_purchased_electricity = calculated_row['electricityPurchased']

        if subregion == calculated_subregion and electricity_purchased == calculated_purchased_electricity:
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
            calculated_subregions.append(calculated_subregion)
    assert calculated_subregions == canonical_subregions

    calculated_subregions_all = []
    for row in calculated_data._output[key]:
        calculated_subregions_all.append(row['eGridSubregion'])

    assert calculated_subregions_all == canonical_subregions


def test_make_total_emissions_for_all_sources(canonical_data, calculated_data):
    key = 'totalEmissionsForAllSources'
    canonical_values = canonical_data[key]
    calculated_values = calculated_data._output[key]
    for gas in canonical_values:
        assert canonical_values[gas] == calculated_values[gas]
    assert canonical_values.keys() == calculated_values.keys()


def test_make_co2_equivalent_emissions_location_based(canonical_data, calculated_data):
    key = "CO2EquivalentEmissionsLocationBasedElectricityEmissions"
    assert null_replacer(canonical_data[key]) == calculated_data._output[key]


def test_make_co2_equivalent_emissions_market_based(canonical_data, calculated_data):
    key = "CO2EquivalentEmissionsMarketBasedElectricityEmissions"
    assert null_replacer(canonical_data[key]) == calculated_data._output[key]


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


def test_output_schema_compliance(calculated_data, canonical_data, electricity_schema):
    output = calculated_data.to_dict()
    output['version'] = canonical_data['version']
    electricity_schema.validate(output)
