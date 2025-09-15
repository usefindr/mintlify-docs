import json

defaults = {
    "tenant_id": "tenant_1234",
    "sub_tenant_id": "sub_tenant_4567",
    "memory_id": "memory_1234",
    "user_memory": "I prefer detailed technical explanations and works in the Pacific timezone",
    "query": "Which mode does user prefer",
    "user_query": "Which mode does user prefer",
    "max_count": 5,
    "web_url": "https://www.usecortex.ai/",
    "file_id": "CortexDoc1234",
    "source_id": "CortexDoc1234",
    "user_name": "John Doe",
    "message": "<string>",
    "embeddings": [[0.123413, 0.655367, 0.987654, 0.123456, 0.789012], [0.123413, 0.655367, 0.987654, 0.123456, 0.789012]],
    "question": "What is Cortex AI",
    "session_id": "chat_session_1234",
    "tenant_metadata_schema": [
        {
            "key": "department",
            "type": "string",
            "searchable": True,
            "filterable": True
        },
        {
            "key": "compliance_framework",
            "type": "string",
            "searchable": True,
            "filterable": False
        },
        {
            "key": "data_classification",
            "type": "string",
            "searchable": False,
            "filterable": True
        }
    ],
    "operator": "and"
}

full_text_query = "John Smith Jake"

update_embeddings_emb = {
    "CortexEmbeddings123_0": [0.123413, 0.655367, 0.987654, 0.123456, 0.789012],
    "CortexEmbeddings123_1": [0.123413, 0.655367, 0.987654, 0.123456, 0.789012]
}

OPEN_API_PATH = "./api-reference/openapi.json"

with open(OPEN_API_PATH, "r") as f:
    openapi = json.load(f)

print("Adding default values to query params")
for endpoint in openapi["paths"]:
    for method in openapi["paths"][endpoint]:
        if "parameters" in openapi["paths"][endpoint][method]:
            for param in openapi["paths"][endpoint][method]["parameters"]:
                if param["in"] == "query":
                    param["schema"]["default"] = defaults.get(
                        param["name"], f"<{type(param['name']).__name__}>")
print("Default values added to query params.")

print("Adding default values to components.schemas")
if "components" in openapi and "schemas" in openapi["components"]:
    for schema_name, schema_def in openapi["components"]["schemas"].items():
        if "properties" in schema_def:
            for prop_name, prop_def in schema_def["properties"].items():
                # Special case for FullTextSearchRequest query property
                if schema_name == "FullTextSearchRequest" and prop_name == "query":
                    prop_def["default"] = full_text_query
                elif schema_name == "EmbeddingsUpdateRequest" and prop_name == "embeddings":
                    prop_def["default"] = update_embeddings_emb
                elif prop_name in defaults:
                    prop_def["default"] = defaults[prop_name]
                elif "type" in prop_def:
                    if prop_def["type"] == "string":
                        prop_def["default"] = f"<{prop_name}>"
                    elif prop_def["type"] == "integer":
                        prop_def["default"] = 1
                    elif prop_def["type"] == "number":
                        prop_def["default"] = 1.0
                    elif prop_def["type"] == "boolean":
                        prop_def["default"] = True
                    elif prop_def["type"] == "array":
                        prop_def["default"] = []
print("Default values added to components.schemas.")


property_tag_to_hide = "x-cortex-docs-hide"


def recursive_filter(data):
    """
    Recursively filters a Python object (dict or list) to remove elements
    containing the property_tag_to_hide.
    """
    # If the data is a dictionary...
    if isinstance(data, dict):
        # Base case: If the hide tag is in the current dictionary,
        # return None to signal its removal.
        if property_tag_to_hide in data:
            return None

        # Recursive step: Build a new dictionary
        new_dict = {}
        for key, value in data.items():
            # Recursively filter the value
            filtered_value = recursive_filter(value)
            # Only add the key-value pair if the value was not filtered out
            if filtered_value is not None:
                new_dict[key] = filtered_value
        return new_dict

    # If the data is a list...
    elif isinstance(data, list):
        # Recursive step: Build a new list
        new_list = []
        for item in data:
            # Recursively filter the item
            filtered_item = recursive_filter(item)
            # Only add the item if it was not filtered out
            if filtered_item is not None:
                new_list.append(filtered_item)
        return new_list

    # If the data is any other type (string, int, etc.), return it as is.
    else:
        return data


# Process the original openapi spec
final_open_api_spec = recursive_filter(openapi)

with open(OPEN_API_PATH, "w") as f:
    json.dump(final_open_api_spec, f, indent=2)

print("Updated OpenAPI file")
