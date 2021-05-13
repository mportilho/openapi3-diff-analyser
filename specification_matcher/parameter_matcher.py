from basic_operations import comparison_operations
from basic_operations.comparison_operations import compare_simple_field
from spec_metadata.analysis_metadata import ParameterAnalysis
from spec_metadata.component_metadata import ComponentMetadata
from specification_matcher import schema_matcher


def match_parameter(components: dict[str, ComponentMetadata], spec_name: str, base_spec: dict, target_spec: dict):
    field_list = ['name', 'in', 'required', 'deprecated', 'allowEmptyValue', 'allowReserved']
    analysis = ParameterAnalysis(spec_name)
    analysis.fields = comparison_operations.compare_fields(field_list, base_spec, target_spec)
    if 'schema' in base_spec and 'schema' in target_spec:
        analysis.schema = schema_matcher.match_schema(components, base_spec['schema'], target_spec['schema'])
    else:
        prop_matching_data = compare_simple_field('schema', base_spec, target_spec)
        if prop_matching_data is not None:
            analysis.fields.append(prop_matching_data)

    if 'content' in base_spec and 'content' in target_spec:
        raise Exception('not yet')

    print()
