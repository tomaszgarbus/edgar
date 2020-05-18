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
