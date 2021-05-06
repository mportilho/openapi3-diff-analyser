def process(openapi) -> dict:
    component_schemas = openapi['components']['schemas']
    cache: dict = {}
    for schema_key in component_schemas:
        cache[schema_key] = _create_new_schema(schema_key, component_schemas[schema_key])
    for schema_key in component_schemas:
        _process_schema(cache[schema_key], component_schemas[schema_key], cache)
    return cache


def _process_schema(schema: dict, schema_source: dict, cache: dict) -> dict:
    if '$ref' in schema_source:
        key = schema['$ref'].removeprefix('#/components/schemas/')
        schema['$$_ref'] = cache[key]
    elif 'properties' in schema_source:
        for k in schema_source['properties']:
            property_schema = _create_new_schema(k, schema_source['properties'][k])
            schema['properties'][k] = _process_schema(property_schema, schema_source['properties'][k], cache)
    elif 'type' in schema_source and schema_source['type'] == 'array':
        if 'items' not in schema_source:
            raise Exception(f'Schema property defined as array but no "items" property attribute found ')
        array_schema = _create_new_schema('array_item', schema_source['items'])
        schema['items'] = _process_schema(array_schema, schema_source['items'], cache)

    if 'additionalProperties' in schema_source:
        if schema_source['additionalProperties'] is True or schema_source['additionalProperties'] == 'true':
            schema['additionalProperties'] = schema_source['additionalProperties']
        else:
            additional_schema = _create_new_schema('additionalProperties', schema_source['additionalProperties'])
            schema['additionalProperties'] = additional_schema
            return schema

    dynamic_attr_list = ['allOf', 'oneOf', 'anyOf', 'not']
    for attr in dynamic_attr_list:
        if attr in schema_source:
            attr_array: list = []
            for each_schema in schema_source[attr]:
                all_of_schema = _create_new_schema(attr, each_schema)
                attr_array.append(_process_schema(all_of_schema, each_schema, cache))
            schema[f'@_{attr}'] = attr_array

    return schema


def _create_new_schema(name: str, schema_source: dict = None):
    schema = {'schema_name': name}
    if schema_source is not None:
        _copy_attributes(schema, schema_source)
    return schema


def _copy_attributes(schema: dict, source: dict):
    attributes = ['title', 'required', 'type', 'enum', 'format', 'minimum', 'maximum', 'exclusiveMinimum',
                  'exclusiveMaximum', 'minLength', 'maxLength', 'pattern', 'minProperties', 'maxProperties',
                  'minItems', 'maxItems', 'default', '$ref', 'allOf', 'oneOf', 'anyOf', 'not']

    for attr in attributes:
        if attr in source:
            schema[attr] = source[attr]

    if 'properties' in source:
        schema['properties'] = {}
