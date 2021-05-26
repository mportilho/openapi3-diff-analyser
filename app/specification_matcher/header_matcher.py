from app.basic_operations.comparison_operations import add_field_comparison
from app.spec_metadata.analysis_metadata import HeaderAnalysis
from app.spec_metadata.component_metadata import ComponentMetadata
from app.specification_matcher import schema_matcher


def match_header(components: dict[str, ComponentMetadata], spec_name: str, base_spec: dict,
                 target_spec: dict) -> HeaderAnalysis:
    analysis = HeaderAnalysis(spec_name)
    add_field_comparison(analysis, 'schema', base_spec, target_spec, lambda a: 'Objeto Schema')
    if 'schema' in base_spec and 'schema' in target_spec:
        analysis.schema = schema_matcher.match_schema(components, spec_name, base_spec['schema'], target_spec['schema'])
    return analysis
