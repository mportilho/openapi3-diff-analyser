import copy

from definitions import METADATA_SCHEMA
from structures.schema_analysis import SchemaMetadata


def _create_schema_metadata(schema: dict, name: str):
    if METADATA_SCHEMA not in schema:
        schema[METADATA_SCHEMA] = SchemaMetadata(name)


def _copy_schema(schema: dict, name: str) -> dict:
    copy_schema: dict = copy.deepcopy(schema)
    if METADATA_SCHEMA in copy_schema:
        copy_schema.pop(METADATA_SCHEMA)
    _create_schema_metadata(copy_schema, name)
    return copy_schema


def process(openapi) -> dict:
    component_schemas = openapi['components']['schemas']
    cache: dict = {}
    for schema_key in component_schemas:
        cache[schema_key] = copy.deepcopy(component_schemas[schema_key])
        _create_schema_metadata(cache[schema_key], schema_key)
    for schema_key in cache:
        _visit_schema(cache, cache[schema_key])
    return cache


def _visit_schema(cache: dict, schema: dict):
    metadata: SchemaMetadata = schema[METADATA_SCHEMA]
    if metadata.visited:
        return

    if metadata.name == 'BankingAgentPostalAddress':
        print()

    metadata.visited = True
    if '$ref' in schema:
        key = schema['$ref'].removeprefix('#/components/schemas/')
        metadata.ref = _copy_schema(cache[key], f"{metadata.name}.ref[{key}]")
        _visit_schema(cache, metadata.ref)
    elif 'items' in schema:
        _create_schema_metadata(schema['items'], f"{metadata.name}.[items]")
        metadata.items = schema['items']
        _visit_schema(cache, schema['items'])
    elif 'properties' in schema:
        for k in schema['properties']:
            _create_schema_metadata(schema['properties'][k], f"{metadata.name}.p[{k}]")
            metadata.all_properties[k] = schema['properties'][k]
            _visit_schema(cache, schema['properties'][k])
    if 'additionalProperties' in schema and (
            schema['additionalProperties'] is not True or schema['additionalProperties'] != 'true'):
        _create_schema_metadata(schema['additionalProperties'], f"{metadata.name}.[additionalProperties]")
        _visit_schema(cache, schema['additionalProperties'])
        return schema

    # dynamic_attr_list = ['allOf', 'oneOf', 'anyOf', 'not']
    if 'allOf' in schema:
        for curr_schema in schema['allOf']:
            key = curr_schema['$ref'].removeprefix('#/components/schemas/')
            ref_schema_props = cache[key]['properties']
            for prop in ref_schema_props:
                if prop not in metadata.all_properties:
                    metadata.all_properties[prop] = _copy_schema(ref_schema_props[prop],
                                                                 f"{metadata.name}.p(allOf:{key})[{prop}]")
                    _visit_schema(cache, metadata.all_properties[prop])
