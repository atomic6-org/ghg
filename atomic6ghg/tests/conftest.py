# pylint: disable=all
"""Configuration for testing"""
import json
import pkgutil

from jsonschema import Draft7Validator
import pytest


@pytest.fixture
def stationary_combustion_schema():
    """Provides schema validation to tests"""
    schema_file_contents = pkgutil.get_data("atomic6ghg.schemas", "stationary_combustion.json")
    schema = json.loads(schema_file_contents)
    v = Draft7Validator(schema=schema)
    return v


@pytest.fixture
def waste_gases_schema():
    """Provides schema validation to tests"""
    schema_file_contents = pkgutil.get_data("atomic6ghg.schemas", "waste_gases.json")
    schema = json.loads(schema_file_contents)
    v = Draft7Validator(schema=schema)
    return v


@pytest.fixture
def electricity_schema():
    """Provides schema validation to tests"""
    schema_file_contents = pkgutil.get_data("atomic6ghg.schemas", "electricity.json")
    schema = json.loads(schema_file_contents)
    v = Draft7Validator(schema=schema)
    return v


@pytest.fixture
def steam_schema():
    """Provides schema validation to tests"""
    schema_file_contents = pkgutil.get_data("atomic6ghg.schemas", "steam.json")
    schema = json.loads(schema_file_contents)
    v = Draft7Validator(schema=schema)
    return v


@pytest.fixture()
def refrigeration_and_ac_schema():
    """Provides schema validation to tests"""
    schema_file_contents = pkgutil.get_data("atom6ghg.schemas", "refrigeration_and_ac.json")
    schema = json.loads(schema_file_contents)
    v = Draft7Validator(schema=schema)
    return v


@pytest.fixture
def fire_suppression_schema():
    """Provides schema validation to tests"""
    schema_file_contents = pkgutil.get_data("atomic6ghg.schemas", "fire_suppression.json")
    schema = json.loads(schema_file_contents)
    v = Draft7Validator(schema=schema)
    return v


@pytest.fixture
def purchased_gases_schema():
    """Provides schema validation to tests"""
    schema_file_contents = pkgutil.get_data("atom6ghg.schemas", "purchased_gases.json")
    schema = json.loads(schema_file_contents)
    v = Draft7Validator(schema=schema)
    return v


@pytest.fixture
def business_travel_schema():
    """Provides schema validation to tests"""
    schema_file_contents = pkgutil.get_data("atomic6ghg.schemas", "business_travel.json")
    schema = json.loads(schema_file_contents)
    v = Draft7Validator(schema=schema)
    return v


@pytest.fixture
def waste_schema():
    """Provides schema validation to tests"""
    schema_file_contents = pkgutil.get_data("atomic6ghg.schemas", "waste.json")
    schema = json.loads(schema_file_contents)
    v = Draft7Validator(schema=schema)
    return v
