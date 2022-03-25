import json
import pytest
import pkgutil
import os


def test_minimum_required(purchased_gases_schema):
    minimum_purchased_gases_document = json.loads(
        """
        {
            "version": "purchased-gases.1.0.0", 
            "purchasedGases": []
        }
        """
    )

    purchased_gases_schema.validate(minimum_purchased_gases_document)


def test_canonical_instance(purchased_gases_schema):
    TEST_FILENAME = os.path.join(os.path.dirname(__file__), './fixtures/purchased_gases_canonical_instance.json')
    with open(TEST_FILENAME, 'r', encoding='utf-8') as canonical_instance:
        canonical_purchased_gases_schema_document = json.load(canonical_instance)
        purchased_gases_schema.validate(canonical_purchased_gases_schema_document)

