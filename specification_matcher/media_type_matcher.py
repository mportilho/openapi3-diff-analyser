from basic_operations.comparison_operations import add_field_comparison
from spec_metadata.analysis_metadata import MediaTypeAnalysis
from spec_metadata.component_metadata import ComponentMetadata
from specification_matcher import schema_matcher


def match_media_type(components: dict[str, ComponentMetadata], spec_name: str, base_spec: dict, target_spec: dict):
    analysis = MediaTypeAnalysis(spec_name)
    if 'schema' in base_spec and 'schema' in target_spec:
        analysis.schema = schema_matcher.match_schema(components, f"mt[{spec_name}]", base_spec, target_spec)
    else:
        add_field_comparison(analysis, 'schema', base_spec, target_spec, lambda a: 'Objeto Schema')
    return analysis
