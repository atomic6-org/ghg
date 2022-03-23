import json
import os

def test_minimum_required(refrigeration_and_ac_schema):
    minimum_refrigeration_and_ac_document = json.loads(
        "{ \
            \"version\": \"refrigeration-and-ac.1.0.0\", \
            \"materialBalance\": [] \
        }"
    )

    refrigeration_and_ac_schema.validate(minimum_refrigeration_and_ac_document)


def test_canonical_instance(refrigeration_and_ac_schema):
    TEST_FILENAME = os.path.join(os.path.dirname(__file__), './fixtures/refrigeration_and_ac_canonical_instance.json')
    with open(TEST_FILENAME, 'r', encoding='utf-8') as canonical_instance:
        canonical_refrigeration_and_ac_document = json.load(canonical_instance)
        refrigeration_and_ac_schema.validate(canonical_refrigeration_and_ac_document)

