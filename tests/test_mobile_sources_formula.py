import pytest
import json
import os

from atomic6ghg.formulas import MobileSources


@pytest.fixture
def canonical_data():
    TEST_FILENAME = os.path.join(os.path.dirname(__file__), './fixtures/mobile_sources_canonical_instance.json')
    with open(TEST_FILENAME, 'r', encoding='utf-8') as canonical_instance:
        stationary_combustion_document = json.load(canonical_instance)
        return stationary_combustion_document


@pytest.fixture
def calculated_data(canonical_data):
    mobile_sources = MobileSources(wks_data=canonical_data)
    return mobile_sources


def test_make_total_mobile_sources_fuel_usage_and_co2_emissions(canonical_data, calculated_data):
    key = "totalMobileSourcesFuelUsageAndCO2Emissions"
    calculated_fuel_types = []
    canonical_fuel_types = []
    for canonical_row in canonical_data[key]:
        fuel_type = canonical_row['fuelType']
        fuel_usage = canonical_row['fuelUsage']
        units = canonical_row['units']
        co2 = canonical_row['CO2']

        canonical_fuel_types.append(fuel_type)

        for calculated_row in calculated_data._output[key]:
            calculated_fuel_type = calculated_row['fuelType']
            if fuel_type == calculated_fuel_type:
                assert fuel_usage == calculated_row['fuelUsage']
                assert units == calculated_row['units']
                assert abs(co2 - calculated_row['CO2']) < 0.001
                calculated_fuel_types.append(calculated_fuel_type)
    assert calculated_fuel_types == canonical_fuel_types

    calculated_fuel_types_all = []
    for row in calculated_data._output[key]:
        calculated_fuel_types_all.append(row['fuelType'])

    assert calculated_fuel_types_all == canonical_fuel_types


def test_make_total_organization_wide_on_road_gasoline_mobile_source_mileage_and_emissions(canonical_data,
                                                                                           calculated_data):
    key = "totalOrganizationWideOnRoadGasolineMobileSourceMileageAndEmissions"
    calculated_vehicle_types = []
    canonical_vehicle_types = []
    canonical_vehicle_years = {}
    for canonical_row in canonical_data[key]:
        vehicle_type = canonical_row['vehicleType']
        emission_by_year = canonical_row['emissionByYear']

        canonical_vehicle_types.append(vehicle_type)
        canonical_vehicle_years[vehicle_type] = []

        for calculated_row in calculated_data._output[key]:
            calculated_vehicle_type = calculated_row['vehicleType']
            if vehicle_type == calculated_vehicle_type:
                calculated_vehicle_types.append(calculated_vehicle_type)
                calculated_emission_by_year = calculated_row['emissionByYear']

                calculated_vehicle_years = []

                for canonical_year_row in emission_by_year:
                    vehicle_year = canonical_year_row['vehicleYear']
                    mileage = canonical_year_row['mileage']
                    ch4 = canonical_year_row['CH4']
                    n2o = canonical_year_row['N2O']

                    canonical_vehicle_years[vehicle_type].append(vehicle_year)

                    for calculated_year_row in calculated_emission_by_year:
                        calculated_vehicle_year = calculated_year_row['vehicleYear']
                        if vehicle_year == calculated_vehicle_year:
                            assert mileage == calculated_year_row['mileage']
                            assert abs(ch4 - calculated_year_row['CH4']) < 0.001
                            assert abs(n2o - calculated_year_row['N2O']) < 0.001
                            calculated_vehicle_years.append(calculated_vehicle_year)

                assert calculated_vehicle_years == canonical_vehicle_years[vehicle_type]
    assert calculated_vehicle_types == canonical_vehicle_types

    calculated_vehicle_years_all = {}
    for row in calculated_data._output[key]:
        vehicle_type = row['vehicleType']
        calculated_vehicle_years_all[vehicle_type] = []
        emission_by_year = row['emissionByYear']
        for year_row in emission_by_year:
            calculated_vehicle_years_all[vehicle_type].append(year_row['vehicleYear'])
        assert set(calculated_vehicle_years_all[vehicle_type]) == set(canonical_vehicle_years[vehicle_type])
    assert set(calculated_vehicle_years_all.keys()) == set(canonical_vehicle_types)


def test_make_total_organization_wide_on_road_non_gasoline_mobile_source_mileage_and_emissions(canonical_data,
                                                                                               calculated_data):
    key = "totalOrganizationWideOnRoadNonGasolineMobileSourceMileageAndEmissions"
    calculated_vehicle_years = {}
    canonical_vehicle_years = {}
    for canonical_row in canonical_data[key]:
        vehicle_type = canonical_row['vehicleType']
        fuel_type = canonical_row['fuelType']
        emission_by_year = canonical_row['emissionByYear']

        if vehicle_type not in canonical_vehicle_years:
            canonical_vehicle_years[vehicle_type] = {}
        if fuel_type in canonical_vehicle_years[vehicle_type]:
            assert False  # There should be a unique vehicle_type, fuel_type combination

        canonical_vehicle_years[vehicle_type][fuel_type] = []

        for calculated_row in calculated_data._output[key]:
            calculated_vehicle_type = calculated_row['vehicleType']
            calculated_fuel_type = calculated_row['fuelType']

            if vehicle_type == calculated_vehicle_type and fuel_type == calculated_fuel_type:
                if vehicle_type not in calculated_vehicle_years:
                    calculated_vehicle_years[calculated_vehicle_type] = {}
                if calculated_fuel_type in calculated_vehicle_years[calculated_vehicle_type]:
                    assert False  # There should be a unique vehicle_type, fuel_type combination
                calculated_vehicle_years[calculated_vehicle_type][calculated_fuel_type] = []

                calculated_emission_by_year = calculated_row['emissionByYear']

                for canonical_year_row in emission_by_year:
                    vehicle_year = canonical_year_row['vehicleYear']
                    mileage = canonical_year_row['mileage']
                    ch4 = canonical_year_row['CH4']
                    n2o = canonical_year_row['N2O']

                    canonical_vehicle_years[vehicle_type][fuel_type].append(vehicle_year)

                    for calculated_year_row in calculated_emission_by_year:
                        calculated_vehicle_year = calculated_year_row['vehicleYear']
                        if vehicle_year == calculated_vehicle_year:
                            assert mileage == calculated_year_row['mileage']
                            assert abs(ch4 - calculated_year_row['CH4']) < 0.001
                            assert abs(n2o - calculated_year_row['N2O']) < 0.001
                            calculated_vehicle_years[calculated_vehicle_type][calculated_fuel_type]\
                                .append(calculated_vehicle_year)

                assert calculated_vehicle_years[vehicle_type][fuel_type] == \
                       canonical_vehicle_years[vehicle_type][fuel_type]

    assert set(calculated_vehicle_years.keys()) == set(canonical_vehicle_years.keys())
    for vehicle_type in canonical_vehicle_years:
        assert set(calculated_vehicle_years[vehicle_type].keys()) == set(canonical_vehicle_years[vehicle_type].keys())

    calculated_vehicle_years_all = {}
    for row in calculated_data._output[key]:
        vehicle_type = row['vehicleType']
        fuel_type = row['fuelType']
        if vehicle_type not in calculated_vehicle_years_all:
            calculated_vehicle_years_all[vehicle_type] = {}
        if fuel_type in calculated_vehicle_years_all[vehicle_type]:
            assert False  # There should be a unique vehicle_type, fuel_type combination
        calculated_vehicle_years_all[vehicle_type][fuel_type] = []

        emission_by_year = row['emissionByYear']
        for year_row in emission_by_year:
            calculated_vehicle_years_all[vehicle_type][fuel_type].append(year_row['vehicleYear'])
        assert set(calculated_vehicle_years_all[vehicle_type][fuel_type]) == \
               set(canonical_vehicle_years[vehicle_type][fuel_type])
    assert set(calculated_vehicle_years_all.keys()) == set(canonical_vehicle_years.keys())
    for vehicle_type in calculated_vehicle_years_all:
        assert set(calculated_vehicle_years_all[vehicle_type].keys()) == \
               set(canonical_vehicle_years[vehicle_type].keys())


def test_make_total_organization_wide_non_road_mobile_source_fuel_usage_and_emissions(canonical_data, calculated_data):
    key = "totalOrganizationWideNonRoadMobileSourceFuelUsageAndEmissions"
    calculated_fuel_types = {}
    canonical_fuel_types = {}
    for canonical_row in canonical_data[key]:
        vehicle_type = canonical_row['vehicleType']
        emission_by_fuel_type = canonical_row['emissionByFuelType']

        if vehicle_type not in canonical_fuel_types:
            canonical_fuel_types[vehicle_type] = []

        for calculated_row in calculated_data._output[key]:
            calculated_vehicle_type = calculated_row['vehicleType']
            if vehicle_type == calculated_vehicle_type:
                if vehicle_type not in calculated_fuel_types:
                    calculated_fuel_types[calculated_vehicle_type] = []

                calculated_emission_by_fuel_type = calculated_row['emissionByFuelType']

                for canonical_fuel_row in emission_by_fuel_type:
                    fuel_type = canonical_fuel_row['fuelType']
                    fuel_usage = canonical_fuel_row['fuelUsage']
                    ch4 = canonical_fuel_row['CH4']
                    n2o = canonical_fuel_row['N2O']

                    canonical_fuel_types[vehicle_type].append(fuel_type)

                    for calculated_year_row in calculated_emission_by_fuel_type:
                        calculated_fuel_type = calculated_year_row['fuelType']
                        if fuel_type == calculated_fuel_type:
                            assert fuel_usage == calculated_year_row['fuelUsage']
                            assert abs(ch4 - calculated_year_row['CH4']) < 0.001
                            assert abs(n2o - calculated_year_row['N2O']) < 0.001
                            calculated_fuel_types[calculated_vehicle_type].append(calculated_fuel_type)

                assert canonical_fuel_types[vehicle_type] == calculated_fuel_types[calculated_vehicle_type]
    assert set(canonical_fuel_types.keys()) == set(calculated_fuel_types.keys())

    calculated_fuel_types_all = {}
    for row in calculated_data._output[key]:
        vehicle_type = row['vehicleType']
        calculated_fuel_types_all[vehicle_type] = []
        emission_by_fuel_type = row['emissionByFuelType']
        for fuel_row in emission_by_fuel_type:
            calculated_fuel_types_all[vehicle_type].append(fuel_row['fuelType'])
        assert sorted(calculated_fuel_types_all[vehicle_type]) == sorted(canonical_fuel_types[vehicle_type])
    assert set(calculated_fuel_types_all.keys()) == set(canonical_fuel_types)


def test_make_co2_equivalent_emissions(canonical_data, calculated_data):
    key = "totalCO2EquivalentEmissions"
    assert abs(canonical_data[key] - calculated_data._output[key]) < 0.001


def test_make_total_biomass_co2_equivalent_emissions(canonical_data, calculated_data):
    key = "totalBiomassCO2EquivalentEmissions"
    assert abs(canonical_data[key] - calculated_data._output[key]) < 0.001


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


def test_output_schema_compliance(calculated_data, canonical_data, mobile_sources_schema):
    output = calculated_data.to_dict()
    output['version'] = canonical_data['version']
    mobile_sources_schema.validate(output)
