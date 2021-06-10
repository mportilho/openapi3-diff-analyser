import copy

from app.basic_operations.comparison_operations import compare_fields, add_field_comparison
from app.spec_metadata.analysis_metadata import SchemaAnalysis
from app.spec_metadata.component_metadata import ComponentMetadata, ComponentMetadataObject
from definitions import ANALYSIS_SCHEMA_FIELDS


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
    base_spec = _resolve_schema_references(components['base'], base_spec)
    target_spec = _resolve_schema_references(components['target'], target_spec)

    analysis.fields = compare_fields(ANALYSIS_SCHEMA_FIELDS, base_spec, target_spec)

    base_properties = base_spec['properties']
    target_properties = target_spec['properties']
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


def _resolve_schema_references(component: ComponentMetadata, schema: dict) -> dict:
    composed_schema = copy.deepcopy(schema)
    references = _compose_schemas(component, schema)
    if 'properties' in references:
        composed_schema['properties'] = references['properties']
    if 'required' in references:
        composed_schema['required'] = references['required']
    return composed_schema


def _compose_schemas(component: ComponentMetadata, schema: dict) -> dict:
    # dynamic_field_list = ['allOf', 'oneOf', 'anyOf', 'not']
    fields = {
        'properties': schema['properties'] if 'properties' in schema else {},
        'required': schema['required'] if 'required' in schema else []
    }

    if 'allOf' in schema:
        for curr_schema in schema['allOf']:
            ref_comp_metadata = component.get_component_by_ref(curr_schema['$ref'])
            ref_schema = ref_comp_metadata.get_spec()
            ref_fields = {
                'properties': ref_schema['properties'] if 'properties' in ref_schema else {},
                'required': ref_schema['required'] if 'required' in ref_schema else []
            }
            _compose_fields(ref_comp_metadata, ref_fields, fields, 'allOf')

            # Calling transitive references
            transitive_fields = _compose_schemas(component, ref_schema)
            _compose_fields(ref_comp_metadata, transitive_fields, fields, 'allOf')

    return fields


def _compose_fields(component_metadata: ComponentMetadataObject, ref_fields: dict, target_fields: dict,
                    origin_name: str):
    # Coping 'properties' fields
    for prop_name in ref_fields['properties']:
        if prop_name not in target_fields['properties']:
            target_fields['properties'][prop_name] = ref_fields['properties'][prop_name]
            target_fields['properties'][prop_name]['$$_NAME'] = prop_name + f":{origin_name}({component_metadata.name})"

    # Coping 'required' field
    for schema_required in ref_fields['required']:
        if schema_required not in target_fields['required']:
            target_fields['required'].append(schema_required)
