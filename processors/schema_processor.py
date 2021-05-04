from openapi3_structs.schema import Schema


def process(openapi):
    component_schemas = openapi['components']['schemas']
    cache: dict = {}

    for schema_key in component_schemas:
        cache[schema_key] = _create_new_schema(schema_key, component_schemas[schema_key])

    for schema_key in component_schemas:
        _process_schema(cache[schema_key], component_schemas[schema_key], cache)

    print(cache)


def _process_schema(schema: Schema, schema_source: dict, cache: dict):
    print(schema_source)
    if '$ref' in schema_source:
        key = schema['$ref'].removeprefix('#/components/schemas/')
        schema['$$_ref'] = cache[key]
        return cache[key]
    elif 'properties' in schema_source:
        for k in schema_source['properties']:
            property_schema = _create_new_schema(k, schema_source['properties'][k])
            schema['properties'][k] = _process_schema(property_schema, schema_source['properties'][k], cache)
        return schema
    elif 'type' in schema_source and schema_source['type'] == 'array':
        if 'items' not in schema_source:
            raise Exception(f'Schema property defined as array but no "items" property attribute found ')
        array_schema = _create_new_schema('array_item', schema_source['items'])
        schema['items'] = _process_schema(array_schema, schema_source['items'], cache)
    # elif schema_source['type'] == 'object':
    #     raise Exception(f'Schema type is object but no "$ref" or "properties" attributes defined')

    if 'additionalProperties' in schema_source:
        if schema_source['additionalProperties'] is True or schema_source['additionalProperties'] == 'true':
            schema['additionalProperties'] = schema_source['additionalProperties']
        else:
            additional_schema = _create_new_schema('additionalProperties', schema_source['additionalProperties'])
            schema['additionalProperties'] = additional_schema
            return schema

    if 'allOf' in schema_source:
        all_of_schema = _create_new_schema('allOf', schema_source['allOf'])
        schema['$$_allOf'] = _process_schema(all_of_schema, schema_source['allOf'], cache)

    if 'oneOf' in schema_source:
        one_of_schema = _create_new_schema('oneOf', schema_source['oneOf'])
        schema['$$_oneOf'] = _process_schema(one_of_schema, schema_source['oneOf'], cache)

    if 'anyOf' in schema_source:
        any_of_schema = _create_new_schema('anyOf', schema_source['anyOf'])
        schema['$$_anyOf'] = _process_schema(any_of_schema, schema_source['anyOf'], cache)

    if 'not' in schema_source:
        not_of_schema = _create_new_schema('not', schema_source['not'])
        schema['$$_not'] = _process_schema(not_of_schema, schema_source['not'], cache)

    return schema


def _create_new_schema(name: str, schema_source: dict = None):
    schema = Schema()
    schema['schema_name'] = name
    if schema_source is not None:
        _copy_attributes(schema, schema_source)
    return schema


def _copy_attributes(schema: Schema, source: dict):
    attributes = ['title', 'required', 'type', 'enum', 'format', 'minimum', 'maximum', 'exclusiveMinimum',
                  'exclusiveMaximum', 'minLength', 'maxLength', 'pattern', 'minProperties', 'maxProperties',
                  'minItems', 'maxItems', 'default', '$ref', 'allOf', 'oneOf', 'anyOf', 'not']

    for attr in attributes:
        if attr in source:
            schema[attr] = source[attr]

    if 'properties' in source:
        schema['properties'] = {}
