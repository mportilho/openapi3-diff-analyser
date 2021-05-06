from main.schema_comparison import SchemaComparison
from processors import schema_processor


def compare_schema(source_yaml_spec, target_yaml_spec):
    source_spec: dict = schema_processor.process(source_yaml_spec)
    target_spec: dict = schema_processor.process(target_yaml_spec)
    schema_comparison = SchemaComparison(source_spec, target_spec)

    for source_schema_name in schema_comparison.source:
        _compare_schemas(schema_comparison, schema_comparison.result[source_schema_name],
                         schema_comparison.target[source_schema_name])
    print(schema_comparison)


def _compare_schemas(schema_comparison: SchemaComparison, source_schema: dict, target_schema: dict):
    if 'analysed' in source_schema:
        return
    source_schema['analysed'] = True

    simple_attr_schema_list = ['required', 'type', 'enum', 'format', 'minimum', 'maximum', 'exclusiveMinimum',
                               'exclusiveMaximum', 'minLength', 'maxLength', 'pattern', 'minProperties',
                               'maxProperties', 'minItems', 'maxItems', 'default']
    for attr_name in simple_attr_schema_list:
        result = _compare_simple_attribute(attr_name, source_schema, target_schema)
        if result:
            source_schema[attr_name] = result

    # , '$ref', 'allOf', 'oneOf', 'anyOf', 'not'

    if '$ref' in source_schema or '$ref' in target_schema:
        if '$ref' in source_schema and '$ref' in target_schema:
            source_schema['$ref'] = _compare_simple_attribute('$ref', source_schema, target_schema)
        elif '$ref' in source_schema:
            _compare_schemas(schema_comparison, source_schema['@_$ref'], target_schema)
        elif '$ref' in target_schema:
            _compare_schemas(schema_comparison, source_schema, target_schema['@_$ref'])
    elif 'properties' in source_schema or 'properties' in target_schema:
        if 'properties' in source_schema and 'properties' in target_schema:
            source_property = source_schema['properties']
            target_property = target_schema['properties']
            for attr in source_property:
                if attr in source_property and attr in target_property:
                    _compare_schemas(schema_comparison, source_property[attr], target_property[attr])
                elif attr in source_schema:
                    print()
                elif attr in target_schema:
                    print()
        elif 'properties' in source_schema:
            _compare_schemas(schema_comparison, source_schema['@_$ref'], target_schema)
        elif 'properties' in target_schema:
            _compare_schemas(schema_comparison, source_schema, target_schema['@_$ref'])
    else:
        _compare_schemas(schema_comparison, source_schema, target_schema)
    print(source_schema)


def _compare_properties(schema_comparison: SchemaComparison, source_schema, target_schema):
    result = {}
    if 'properties' in source_schema and 'properties' in target_schema:
        source_properties = source_schema['properties']
        target_properties = target_schema['properties']
        result['source'] = source_properties
        result['target'] = target_properties
        for prop in source_properties:
            if prop in target_properties:
                _compare_schemas(schema_comparison, source_properties[prop], target_properties[prop])
                result['comparison'] = f'Schema Property "{prop}" analysed'
            else:
                result['comparison'] = f'Schema Property "{prop}" does not exist on target Schema'
    elif 'properties' in source_schema:
        result['comparison'] = f'Schema Property absent on target schema'
        result['source'] = source_schema['properties']
        result['target'] = 'absent'
    elif 'properties' in target_schema:
        result['comparison'] = f'Schema Property absent on source schema'
        result['source'] = 'absent'
        result['target'] = target_schema['properties']
    return result


def _compare_simple_attribute(attr_name: str, source_dict: dict, target_dict: dict) -> dict:
    result = {}
    if attr_name in source_dict and attr_name in target_dict:
        result['source'] = source_dict[attr_name]
        result['target'] = target_dict[attr_name]
        if source_dict[attr_name] == target_dict[attr_name]:
            result['comparison'] = f'Attribute "{attr_name}" OK'
        else:
            result['comparison'] = f'Attribute "{attr_name}" with different values'
    elif attr_name in source_dict:
        result['comparison'] = f'Attribute "{attr_name}" absent on target schema'
        result['source'] = source_dict[attr_name]
        result['target'] = 'absent'
    elif attr_name in target_dict:
        result['comparison'] = f'Attribute "{attr_name}" absent on source schema'
        result['source'] = 'absent'
        result['target'] = target_dict[attr_name]
    return result


def _is_analysed(obj: dict) -> bool:
    return 'source' in obj and 'target' in obj and 'comparison' in obj

# result = {}
# if attr_name in source_dict and attr_name in target_dict:
#     print()
# elif attr_name in source_dict:
#     print()
# elif attr_name in target_dict:
#     print()
# return result
