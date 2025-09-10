import json

defaults = {
    "tenant_id": "tenant_1234",
    "sub_tenant_id": "sub_tenant_4567",
    "memory_id": "memory_1234",
    "user_memory": "user_memory_1234",
    "query": "Which mode does user prefer",
    "user_query": "Which mode does user prefer",
    "max_count": 5,
    "web_url": "https://www.usecortex.ai/",
    "file_id": "CortexDoc1234",
    "source_id": "CortexDoc1234",
    "user_name": "John Doe"
}

OPEN_API_PATH = "./api-reference/openapi.json"

with open(OPEN_API_PATH, "r") as f:
    openapi = json.load(f)

for endpoint in openapi["paths"]:
    for method in openapi["paths"][endpoint]:
        if "parameters" in openapi["paths"][endpoint][method]:
            for param in openapi["paths"][endpoint][method]["parameters"]:
                if param["in"] == "query":
                    param["schema"]["default"] = defaults[param["name"]]

with open(OPEN_API_PATH, "w") as f:
    json.dump(openapi, f, indent=2)
    
print("Updated OpenAPI file")