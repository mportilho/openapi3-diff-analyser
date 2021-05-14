from basic_operations.comparison_operations import compare_fields, add_field_comparison
from definitions import ANALYSIS_PARAMETERS_FIELDS
from spec_metadata.analysis_metadata import ParameterAnalysis
from spec_metadata.component_metadata import ComponentMetadata
from specification_matcher import schema_matcher, media_type_matcher


def match_parameter(components: dict[str, ComponentMetadata], spec_name: str, base_spec: dict,
                    target_spec: dict) -> ParameterAnalysis:
    analysis = ParameterAnalysis(spec_name)
    analysis.fields = compare_fields(ANALYSIS_PARAMETERS_FIELDS, base_spec, target_spec)

    add_field_comparison(analysis, 'schema', base_spec, target_spec, lambda a: 'Objeto Schema')
    if 'schema' in base_spec and 'schema' in target_spec:
        analysis.schema = schema_matcher.match_schema(components, base_spec['schema'], target_spec['schema'])

    add_field_comparison(analysis, 'content', base_spec, target_spec, lambda a: list(a.keys()))
    if 'content' in base_spec and 'content' in target_spec:
        for c_name, c_value in base_spec.items():
            if c_name in target_spec['content']:
                analysis.content.append(
                    media_type_matcher.match_media_type(components, f"cnt[{c_name}]", base_spec, target_spec))
    return analysis
