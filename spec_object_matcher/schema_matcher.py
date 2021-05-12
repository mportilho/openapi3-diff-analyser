from spec_matcher.matching_operations import compare_attributes, compare_simple_attribute
from spec_metadata.analysis_metadata import SchemaAnalysis
from spec_metadata.component_metadata import ComponentMetadata


def match_schema(component_metadata: ComponentMetadata, schema_name: str, base_spec: dict,
                 target_spec: dict) -> SchemaAnalysis:
    if '$ref' in base_spec or '$ref' in target_spec:
        if '$ref' in base_spec and '$ref' in target_spec:
            attr_matching_data = list()
            attr_matching_data.append(compare_simple_attribute('$ref', base_spec, target_spec))
            return SchemaAnalysis(schema_name, attr_matching_data)
        elif '$ref' in base_spec:
            comp_obj = component_metadata.get_component_by_ref(base_spec['$ref'])
            name = schema_name + f"[$ref:{comp_obj.name}]"
            return match_schema(component_metadata, name, comp_obj.get_spec(), target_spec)
        elif '$ref' in target_spec:
            comp_obj = component_metadata.get_component_by_ref(target_spec['$ref'])
            name = schema_name + f"[$ref:{comp_obj.name}]"
            return match_schema(component_metadata, name, base_spec, comp_obj.get_spec())

    attr_list = ['required', 'type', 'enum', 'format', 'minimum', 'maximum', 'exclusiveMinimum',
                 'exclusiveMaximum', 'minLength', 'maxLength', 'pattern', 'minProperties',
                 'maxProperties', 'minItems', 'maxItems', 'default']
    attr_matching_data = compare_attributes(attr_list, base_spec, target_spec)
    prop_matching_data = compare_simple_attribute('properties', base_spec, target_spec,
                                                  lambda attr_name, spec: list(
                                                      spec[attr_name].keys()))
    if prop_matching_data is not None:
        attr_matching_data.append(prop_matching_data)

    analysis = SchemaAnalysis(schema_name, attr_matching_data)

    if 'items' in base_spec and 'items' in target_spec:
        analysis.items = match_schema(component_metadata, schema_name + '.item', base_spec['items'],
                                      target_spec['items'])
    else:
        attr_matching_data.append(
            compare_simple_attribute('items', base_spec, target_spec, lambda a, b: 'Objeto "items"'))

    prop_analysis_list = list()
    if 'properties' in base_spec and 'properties' in target_spec:
        for prop_name in base_spec['properties']:
            if prop_name in target_spec['properties']:
                name = schema_name + f".p[{prop_name}]"
                prop_analysis = match_schema(component_metadata, name, base_spec['properties'][prop_name],
                                             target_spec['properties'][prop_name])
                prop_analysis_list.append(prop_analysis)
    analysis.properties = prop_analysis_list
    return analysis
