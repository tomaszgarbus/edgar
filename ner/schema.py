import json
import logging

from jsonschema import validate

schema = {
    "type": "object",
    "required": ["categories"],
    "properties": {
        "categories": {
            "type": "array",
            "description": "Categories of entities",
            "items": {
                "type": "object",
                "required": ["name", "entities"],
                "properties": {
                    "name": {
                        "type": "string",
                        "description": "Category name."
                    },
                    "entities": {
                        "type": "array",
                        "description": "Entities belonging to the category.",
                        "items": {
                            "required": ["name", "variants"],
                            "name": {
                                "type": "str",
                                "description": "Base variant of the entity name."
                            },
                            "variants": {
                                "type": "array",
                                "description": "Other variants of the entity name.",
                                "items": {
                                    "type": "str"
                                }
                            }
                        }
                    }
                }
            }
        },
        "case_sensitive": {
            "type": "boolean",
            "description": "Case-sensitive entity name matching.",
            "default": True
        }
    }
}


def validate_and_load_config(config_path: str):
    with open(config_path, 'r') as fp:
        config = json.load(fp)
    logging.info('Validating JSON schema...')
    validate(instance=config, schema=schema)
    if 'case_sensitive' not in config:
        config['case_sensitive'] = True
    return config
