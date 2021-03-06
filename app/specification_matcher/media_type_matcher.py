from app.basic_operations.comparison_operations import add_field_comparison
from app.spec_metadata.analysis_metadata import MediaTypeAnalysis
from app.spec_metadata.component_metadata import ComponentMetadata
from app.specification_matcher import schema_matcher


def match_media_type(components: dict[str, ComponentMetadata], spec_name: str, base_spec: dict,
                     target_spec: dict) -> MediaTypeAnalysis:
    analysis = MediaTypeAnalysis(spec_name)
    add_field_comparison(analysis, 'schema', base_spec, target_spec, lambda a: 'Objeto Schema')
    if 'schema' in base_spec and 'schema' in target_spec:
        analysis.schema = schema_matcher.match_schema(components, spec_name, base_spec['schema'], target_spec['schema'])
    return analysis
