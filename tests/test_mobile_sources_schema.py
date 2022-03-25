"""test"""
import json
import os


def test_minimum_required(mobile_sources_schema):
    """test"""
    minimum_mobile_sources_document = json.loads(
        "{ \
            \"version\": \"mobile-sources.1.0.0\", \
            \"mobileSourcesFuelConsumption\": [] \
        }"
    )

    mobile_sources_schema.validate(minimum_mobile_sources_document)


def test_canonical_instance(mobile_sources_schema):
    """test"""
    TEST_FILENAME = os.path.join(os.path.dirname(__file__), './fixtures/mobile_sources_canonical_instance.json')
    with open(TEST_FILENAME, 'r', encoding='utf-8') as canonical_instance:
        minimum_stationary_combustion_document = json.load(canonical_instance)
        mobile_sources_schema.validate(minimum_stationary_combustion_document)