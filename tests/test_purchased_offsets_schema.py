import json
import os


def test_minimum_required(purchased_offsets_schema):
    minimum_purchased_offsets_document = json.loads(
        """
        {
            "version": "purchased-offsets.1.0.0", 
            "purchasedOffsets": []
        }
        """
    )
    purchased_offsets_schema.validate(minimum_purchased_offsets_document)


def test_canonical_instance(purchased_offsets_schema):
    TEST_FILENAME = os.path.join(os.path.dirname(__file__), './fixtures/offsets_canonical_instance.json')
    with open(TEST_FILENAME, 'r', encoding='utf-8') as canonical_instance:
        canonical_purchased_offsets_schema_document = json.load(canonical_instance)
        purchased_offsets_schema.validate(canonical_purchased_offsets_schema_document)
