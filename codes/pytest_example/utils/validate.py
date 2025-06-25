from jsonschema import Draft7Validator


def create_schema(validate):
    """
    Create a JSON schema from the validation rules.
    
    :param validate: The validation rules for the response.
    :return: A JSON schema object.
    """
    
    schema = {
        "type": "object",
        "properties": {}
    }
    
    bodys = validate.get("body", {})
    for key, value in bodys.items():
        if isinstance(value, str):
            key_type = "string"
        elif isinstance(value, int):
            key_type = "integer"
        elif isinstance(value, bool):
            key_type = "boolean"
        # ....
        
        schema["properties"][key] = {
            "type": key_type,
            "const": value 
        }
    
    return schema


def validate_response(response, validate):
    """
    Validate JSON data against a given schema.
    
    :param json_data: The JSON data to validate.
    :param schema: The JSON schema to validate against.
    :return: True if valid, raises ValidationError if invalid.
    """
    
    schema = create_schema(validate)
    validator = Draft7Validator(schema)
    errors = list(validator.iter_errors(response.json()))
    
    if errors:
        error_details = []
        for error in errors:
            error_details.append(
                f"Error: {error.message}, Schema Path: {list(error.schema_path)}, Instance Value: {error.instance}"
            )

        return error_details
    
    elif response.status_code != 200:
        return f"Request failed with status code: {response.status_code}"
    
    else:
        return None