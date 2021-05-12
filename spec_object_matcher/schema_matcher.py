import copy

from spec_matcher.matching_operations import compare_attributes, compare_simple_attribute
from spec_metadata.analysis_metadata import SchemaAnalysis, SchemaAnalysisResult
from spec_metadata.component_metadata import ComponentMetadata


def match_schema_specification(components: dict[str, ComponentMetadata], base_schema_spec: dict,
                               target_schema_spec: dict) -> SchemaAnalysisResult:
    result = SchemaAnalysisResult()

    for name in base_schema_spec:
        if name in target_schema_spec:
            result.present.append(name)
            result.results[name] = match_schema(components, name, base_schema_spec[name], target_schema_spec[name])
        else:
            result.absent.append(name)

    for name in target_schema_spec:
        if name not in base_schema_spec:
            result.extra.append(name)

    return result


def match_schema(components: dict[str, ComponentMetadata], schema_name: str, base_spec: dict,
                 target_spec: dict) -> SchemaAnalysis:
    if '$ref' in base_spec or '$ref' in target_spec:
        if '$ref' in base_spec and '$ref' in target_spec:
            attr_matching_data = list()
            attr_matching_data.append(compare_simple_attribute('$ref', base_spec, target_spec))
            return SchemaAnalysis(schema_name, attr_matching_data)
        elif '$ref' in base_spec:
            comp_obj = components['base'].get_component_by_ref(base_spec['$ref'])
            name = schema_name + f"[$ref:{comp_obj.name}]"
            return match_schema(components, name, comp_obj.get_spec(), target_spec)
        elif '$ref' in target_spec:
            comp_obj = components['target'].get_component_by_ref(target_spec['$ref'])
            name = schema_name + f"[$ref:{comp_obj.name}]"
            return match_schema(components, name, base_spec, comp_obj.get_spec())

    attr_list = ['required', 'type', 'enum', 'format', 'minimum', 'maximum', 'exclusiveMinimum',
                 'exclusiveMaximum', 'minLength', 'maxLength', 'pattern', 'minProperties',
                 'maxProperties', 'minItems', 'maxItems', 'default']
    attr_matching_data = compare_attributes(attr_list, base_spec, target_spec)

    base_properties = _compose_properties(components['base'], base_spec)
    target_properties = _compose_properties(components['target'], target_spec)
    if base_properties:
        base_spec['properties'] = base_properties
    if target_properties:
        target_spec['properties'] = target_properties
    prop_matching_data = compare_simple_attribute('properties', base_spec, target_spec, lambda attr_name, spec: list(
        spec[attr_name].keys()))
    if prop_matching_data is not None:
        attr_matching_data.append(prop_matching_data)

    analysis = SchemaAnalysis(schema_name, attr_matching_data)

    if 'items' in base_spec and 'items' in target_spec:
        analysis.items = match_schema(components, schema_name + '.item', base_spec['items'], target_spec['items'])
    else:
        item_comp = compare_simple_attribute('items', base_spec, target_spec, lambda a, b: 'Objeto "items"')
        if item_comp is not None:
            attr_matching_data.append(item_comp)

    prop_analysis_list = list()
    if 'properties' in base_spec:
        for prop_name in base_spec['properties']:
            if 'properties' in target_spec and prop_name in target_spec['properties']:
                name = schema_name + f".p[{prop_name}]"
                prop_analysis = match_schema(components, name, base_spec['properties'][prop_name],
                                             target_spec['properties'][prop_name])
                prop_analysis_list.append(prop_analysis)
    analysis.properties = prop_analysis_list
    analysis.evaluate()
    return analysis


def _compose_properties(component: ComponentMetadata, schema: dict) -> dict:
    # dynamic_attr_list = ['allOf', 'oneOf', 'anyOf', 'not']
    properties = copy.deepcopy(schema['properties']) if 'properties' in schema else {}
    if 'allOf' in schema:
        for curr_schema in schema['allOf']:
            comp_metadata = component.get_component_by_ref(curr_schema['$ref'])
            ref_schema_props = comp_metadata.get_spec()['properties']
            for prop in ref_schema_props:
                if prop not in properties:
                    properties[prop] = ref_schema_props[prop]
    return properties
