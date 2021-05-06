import copy

from definitions import POINTER_PREFIX, METADATA_SCHEMA


def _create_schema_metadata(schema: dict, name: str):
    if METADATA_SCHEMA not in schema:
        schema[METADATA_SCHEMA] = {'visited': False, 'name': name, 'all_properties': {}}


def visit(openapi) -> dict:
    component_schemas = openapi['components']['schemas']
    cache: dict = {}
    for schema_key in component_schemas:
        cache[schema_key] = copy.deepcopy(component_schemas[schema_key])
        _create_schema_metadata(cache[schema_key], schema_key)
    for schema_key in cache:
        _visit_schema(cache, cache[schema_key])
    return cache


def _visit_schema(cache: dict, schema: dict):
    metadata = schema[METADATA_SCHEMA]
    if metadata['visited']:
        return

    metadata['visited'] = True
    if '$ref' in schema:
        key = schema['$ref'].removeprefix('#/components/schemas/')
        schema[POINTER_PREFIX + '$ref'] = cache[key]
    elif 'type' in schema and schema['type'] == 'array':
        if 'items' not in schema:
            raise Exception(f'Schema property defined as array but no "items" property attribute found ')
        _create_schema_metadata(schema['items'], f"{metadata['name']}.p[items]")
        _visit_schema(cache, schema['items'])
    elif 'properties' in schema:
        for k in schema['properties']:
            _create_schema_metadata(schema['properties'][k], f"{metadata['name']}.p[{k}]")
            metadata['all_properties'][k] = schema['properties'][k]
            _visit_schema(cache, schema['properties'][k])

    if 'additionalProperties' in schema and (
            schema['additionalProperties'] is not True or schema['additionalProperties'] != 'true'):
        _create_schema_metadata(schema['additionalProperties'], f"{metadata['name']}.[additionalProperties]")
        _visit_schema(cache, schema['additionalProperties'])
        return schema

    if 'allOf' in schema:
        for curr_schema in schema['allOf']:
            key = curr_schema['$ref'].removeprefix('#/components/schemas/')
            ref_schema_props = cache[key]['properties']
            for prop in ref_schema_props:
                metadata['all_properties'][prop] = ref_schema_props[prop]
                print()

    # dynamic_attr_list = ['allOf', 'oneOf', 'anyOf', 'not']
    # for attr in dynamic_attr_list:
    #     if attr in schema:
    #         attr_array: list = []
    #         for each_schema in schema[attr]:
    #             curr_schema = _create_new_schema(attr, each_schema)
    #             attr_array.append(_process_schema(curr_schema, each_schema, cache))
    #         schema[POINTER_PREFIX + attr] = attr_array
