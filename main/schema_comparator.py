from typing import Optional

from definitions import RESULT_PREFIX, METADATA_RESULT, METADATA_SCHEMA, POINTER_PREFIX
from processors import schema_visitor
from structures.comparison_result import ComparisonResult
from structures.schema_analysis import SchemaResultMetadata
from structures.schema_comparison import SchemaComparison


def _create_result_metadata(schema: dict):
    if METADATA_RESULT not in schema:
        schema[METADATA_RESULT] = SchemaResultMetadata(schema[METADATA_SCHEMA].name)


def compare_schema(source_yaml_spec, target_yaml_spec) -> SchemaComparison:
    source_schema_spec: dict = schema_visitor.visit(source_yaml_spec)
    target_schema_spec: dict = schema_visitor.visit(target_yaml_spec)
    schema_comparison = SchemaComparison(source_schema_spec, target_schema_spec)
    schema_comparison.analyse()

    for source_schema_name in schema_comparison.source:
        _compare_schemas(schema_comparison, schema_comparison.result[source_schema_name],
                         schema_comparison.target[source_schema_name])
    return schema_comparison


def _compare_schemas(schema_comparison: SchemaComparison, source_schema: dict, target_schema: dict):
    _create_result_metadata(source_schema)
    meta_result: SchemaResultMetadata = source_schema[METADATA_RESULT]
    if meta_result.analysed:
        return

    meta_result.analysed = True
    _compare_attributes(source_schema, target_schema)

    # 'allOf', 'oneOf', 'anyOf', 'not'
    if '$ref' in source_schema or '$ref' in target_schema:
        if '$ref' in source_schema and '$ref' in target_schema:
            meta_result.attributes['$ref'] = _compare_simple_attribute('$ref', source_schema, target_schema)
        elif '$ref' in source_schema:
            _compare_schemas(schema_comparison, source_schema[POINTER_PREFIX + '$ref'], target_schema)
        elif '$ref' in target_schema:
            _compare_schemas(schema_comparison, source_schema, target_schema[POINTER_PREFIX + '$ref'])
    elif 'properties' in source_schema or 'properties' in target_schema:
        _compare_properties(schema_comparison, source_schema, target_schema)
    elif 'type' in source_schema and source_schema['type'] == 'array':
        if 'items' in source_schema and 'items' in target_schema:
            _compare_schemas(schema_comparison, source_schema['items'], target_schema['items'])
        elif 'items' in source_schema:
            meta_result.attributes['items'] = _compare_simple_attribute('items', source_schema, target_schema)
        else:
            items_comp = ComparisonResult('items')
            items_comp.equivalent = False
            items_comp.set_source({})
            if 'items' in target_schema:
                items_comp.set_target(target_schema['items'])
            else:
                items_comp.set_target({})
            items_comp.reason = 'Schema type is array but no "items" attribute defined on source Schemas'
            meta_result.attributes['items'] = items_comp
    meta_result.finish_analysis()


def _compare_properties(schema_comparison: SchemaComparison, source_schema: dict, target_schema: dict):
    properties_result = ComparisonResult(source_schema[METADATA_SCHEMA].name + '.[properties]')

    if 'properties' in source_schema and 'properties' in target_schema:
        source_property: dict = source_schema[METADATA_SCHEMA].all_properties
        target_property: dict = target_schema[METADATA_SCHEMA].all_properties
        properties_result.set_source(source_property.keys())
        properties_result.set_target(target_property.keys())

        if source_property.keys() == target_property.keys():
            properties_result.equivalent = True
            properties_result.reason = 'Same properties from source to target schema'
        else:
            properties_result.equivalent = False
            sk = set(source_property.keys())
            tk = set(target_property.keys())
            diff_st = sk.difference(tk)
            diff_ts = tk.difference(sk)
            properties_result.reason = f'Properties mismatch. Diff[s,t] -> {str(diff_st)}. Diff[t,s] -> {str(diff_ts)}'
        for prop in source_property:
            if prop in target_property:
                _compare_schemas(schema_comparison, source_property[prop], target_property[prop])
    elif 'properties' in source_schema:
        if '$ref' in target_schema:
            target_ref_schema = target_schema[POINTER_PREFIX + '$ref']
            _compare_properties(schema_comparison, source_schema, target_ref_schema)
        else:
            properties_result.equivalent = False
            properties_result.set_source(source_schema['properties'])
            properties_result.reason = 'Schema Property absent on target schema'
    elif 'properties' in target_schema:
        properties_result.equivalent = False
        properties_result.set_target(target_schema['properties'])
        properties_result.reason = 'Schema Property absent on source schema'
    source_schema[METADATA_RESULT].properties = properties_result


def _compare_attributes(source_schema: dict, target_schema: dict):
    simple_attr_schema_list = ['required', 'type', 'enum', 'format', 'minimum', 'maximum', 'exclusiveMinimum',
                               'exclusiveMaximum', 'minLength', 'maxLength', 'pattern', 'minProperties',
                               'maxProperties', 'minItems', 'maxItems', 'default']
    for attr_name in simple_attr_schema_list:
        result = _compare_simple_attribute(attr_name, source_schema, target_schema)
        if result is not None:
            source_schema[METADATA_RESULT].attributes[attr_name] = result


def _compare_simple_attribute(attr_name: str, source_dict: dict, target_dict: dict) -> Optional[ComparisonResult]:
    result = ComparisonResult(attr_name)
    if attr_name in source_dict and attr_name in target_dict:
        result.set_source(source_dict[attr_name])
        result.set_target(target_dict[attr_name])
        if source_dict[attr_name] == target_dict[attr_name]:
            result.reason = f'Attribute "{attr_name}" OK'
            result.equivalent = True
        else:
            result.reason = f'Attribute "{attr_name}" with different values'
            result.equivalent = False
    elif attr_name in source_dict:
        result.reason = f'Attribute "{attr_name}" absent on target schema'
        result.set_source(source_dict[attr_name])
    elif attr_name in target_dict:
        result.reason = f'Attribute "{attr_name}" absent on source schema'
        result.set_target(target_dict[attr_name])
    else:
        return None
    return result

# result = {}
# if attr_name in source_dict and attr_name in target_dict:
#     print()
# elif attr_name in source_dict:
#     print()
# elif attr_name in target_dict:
#     print()
# return result
