import copy

from app.basic_operations.comparison_operations import compare_fields, add_field_comparison
from app.definitions import ANALYSIS_SCHEMA_FIELDS
from app.spec_metadata.analysis_metadata import SchemaAnalysis
from app.spec_metadata.component_metadata import ComponentMetadata


def match_schema(components: dict[str, ComponentMetadata], spec_name: str, base_spec: dict,
                 target_spec: dict) -> SchemaAnalysis:
    if '$ref' in base_spec or '$ref' in target_spec:
        if '$ref' in base_spec and '$ref' in target_spec:
            analysis = SchemaAnalysis(spec_name)
            add_field_comparison(analysis, '$ref', base_spec, target_spec)
            return analysis
        elif '$ref' in base_spec:
            comp_obj = components['base'].get_component_by_ref(base_spec['$ref'])
            name = spec_name + f".$ref[{comp_obj.name}]"
            return match_schema(components, name, comp_obj.get_spec(), target_spec)
        elif '$ref' in target_spec:
            comp_obj = components['target'].get_component_by_ref(target_spec['$ref'])
            name = spec_name + f".$ref[{comp_obj.name}]"
            return match_schema(components, name, base_spec, comp_obj.get_spec())

    analysis = SchemaAnalysis(spec_name)
    analysis.fields = compare_fields(ANALYSIS_SCHEMA_FIELDS, base_spec, target_spec)

    base_properties = _compose_properties(components['base'], base_spec)
    target_properties = _compose_properties(components['target'], target_spec)
    if base_properties or target_properties:
        add_field_comparison(analysis, 'properties', {'properties': base_properties}, {'properties': target_properties},
                             lambda a: list(a.keys()))
    add_field_comparison(analysis, 'items', base_spec, target_spec, lambda a: 'Objeto "items"')

    if base_properties and target_properties:
        for p_name, prop in base_properties.items():
            if p_name in target_properties:
                name = spec_name + f".p[{prop['$$_NAME'] if '$$_NAME' in prop else p_name}]"
                prop_analysis = match_schema(components, name, base_properties[p_name], target_properties[p_name])
                analysis.properties.append(prop_analysis)
    if 'items' in base_spec and 'items' in target_spec:
        analysis.items = match_schema(components, spec_name + '.item', base_spec['items'], target_spec['items'])

    return analysis


def _compose_properties(component: ComponentMetadata, schema: dict) -> dict:
    # dynamic_field_list = ['allOf', 'oneOf', 'anyOf', 'not']
    properties = copy.deepcopy(schema['properties']) if 'properties' in schema else {}
    if 'allOf' in schema:
        for curr_schema in schema['allOf']:
            comp_metadata = component.get_component_by_ref(curr_schema['$ref'])
            ref_schema_props = comp_metadata.get_spec()['properties']
            for prop_name in ref_schema_props:
                if prop_name not in properties:
                    properties[prop_name] = ref_schema_props[prop_name]
                    properties[prop_name]['$$_NAME'] = prop_name + f":allOf({comp_metadata.name})"
    return properties
