from definitions import RESULT_PREFIX, CMP_OID_REF, METADATA_RESULT, METADATA_SCHEMA
from main.comparison_result import ComparisonResult
from main.schema_comparison import SchemaComparison
from processors import schema_visitor


def _create_result_metadata(schema: dict):
    if METADATA_RESULT not in schema:
        schema[METADATA_RESULT] = {'analysed': False, 'name': schema[METADATA_SCHEMA]['name'], 'attributes': {}}


def compare_schema(source_yaml_spec, target_yaml_spec):
    source_spec: dict = schema_visitor.visit(source_yaml_spec)
    target_spec: dict = schema_visitor.visit(target_yaml_spec)
    schema_comparison = SchemaComparison(source_spec, target_spec)

    for source_schema_name in schema_comparison.source:
        _compare_schemas(schema_comparison, schema_comparison.result[source_schema_name],
                         schema_comparison.target[source_schema_name])
    print(schema_comparison)


def _compare_schemas(schema_comparison: SchemaComparison, source_schema: dict, target_schema: dict):
    _create_result_metadata(source_schema)
    meta_result = source_schema[METADATA_RESULT]
    if meta_result['analysed']:
        return

    source_schema['analysed'] = True
    _compare_attributes(source_schema, target_schema)

    # 'allOf', 'oneOf', 'anyOf', 'not'
    if '$ref' in source_schema or '$ref' in target_schema:
        if '$ref' in source_schema and '$ref' in target_schema:
            source_schema[RESULT_PREFIX + '$ref'] = _compare_simple_attribute('$ref', source_schema, target_schema)
        elif '$ref' in source_schema:
            _compare_schemas(schema_comparison, source_schema[CMP_OID_REF], target_schema)
        elif '$ref' in target_schema:
            _compare_schemas(schema_comparison, source_schema, target_schema[CMP_OID_REF])
    elif 'properties' in source_schema or 'properties' in target_schema:
        _compare_properties(schema_comparison, source_schema, target_schema)
    elif 'type' in source_schema and source_schema['type'] == 'array':
        items_comp = ComparisonResult('items')
        if 'items' in source_schema and 'items' in target_schema:
            items_comp.equivalent = True
            items_comp.set_source(source_schema['items'])
            items_comp.set_target(target_schema['items'])
            items_comp.reason = 'Schema attribute "items" found on source and target Schemas'
        elif 'items' in source_schema:
            items_comp.equivalent = False
            items_comp.set_source(source_schema['items'])
            items_comp.reason = 'Schema type is array but no "items" attribute defined on source Schema'
        elif 'items' in target_schema:
            items_comp.equivalent = False
            items_comp.set_target(target_schema['items'])
            items_comp.reason = 'Schema type is array but no "items" attribute defined on target Schema'
        else:
            items_comp.equivalent = False
            items_comp.reason = 'Schema type is array but no "items" attribute defined on source and target Schemas'
        source_schema[RESULT_PREFIX + 'items'] = items_comp
    else:
        _compare_schemas(schema_comparison, source_schema, target_schema)
    print(source_schema)


def _compare_properties(schema_comparison: SchemaComparison, source_schema: dict, target_schema: dict):
    source_metadata = source_schema[METADATA_SCHEMA]
    target_metadata = target_schema[METADATA_SCHEMA]
    properties_result = ComparisonResult(source_metadata['name'] + '.[properties]')

    if 'properties' in source_schema and 'properties' in target_schema:
        source_property: dict = source_metadata['all_properties']
        target_property: dict = target_metadata['all_properties']
        source_schema[RESULT_PREFIX + 'properties'] = properties_result

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
        properties_result.set_source(source_schema['properties'])
        properties_result.reason = 'Schema Property absent on target schema'
    elif 'properties' in target_schema:
        properties_result.set_target(target_schema['properties'])
        properties_result.reason = 'Schema Property absent on source schema'
    source_schema[RESULT_PREFIX + 'properties'] = properties_result


def _compare_attributes(source_schema: dict, target_schema: dict):
    simple_attr_schema_list = ['required', 'type', 'enum', 'format', 'minimum', 'maximum', 'exclusiveMinimum',
                               'exclusiveMaximum', 'minLength', 'maxLength', 'pattern', 'minProperties',
                               'maxProperties', 'minItems', 'maxItems', 'default']
    for attr_name in simple_attr_schema_list:
        result: ComparisonResult = _compare_simple_attribute(attr_name, source_schema, target_schema)
        if result.equivalent is not None:
            source_schema[METADATA_RESULT]['attributes'] = result


def _compare_simple_attribute(attr_name: str, source_dict: dict, target_dict: dict) -> ComparisonResult:
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
    return result

# result = {}
# if attr_name in source_dict and attr_name in target_dict:
#     print()
# elif attr_name in source_dict:
#     print()
# elif attr_name in target_dict:
#     print()
# return result
