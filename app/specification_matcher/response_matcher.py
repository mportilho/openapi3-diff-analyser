from app.basic_operations.comparison_operations import add_field_comparison
from app.spec_metadata.analysis_metadata import ResponseAnalysis
from app.spec_metadata.component_metadata import ComponentMetadata
from app.specification_matcher.header_matcher import match_header
from app.specification_matcher.media_type_matcher import match_media_type


def match_response(components: dict[str, ComponentMetadata], spec_name: str, base_spec: dict,
                   target_spec: dict, fields=None) -> ResponseAnalysis:
    analysis = ResponseAnalysis(spec_name)

    add_field_comparison(analysis, 'headers', base_spec, target_spec, lambda a: list(a.keys()))
    if 'headers' in base_spec and 'headers' in target_spec:
        for c_name, c_value in base_spec.items():
            if c_name in target_spec['headers']:
                analysis.headers.append(
                    match_header(components, c_name, base_spec['headers'][c_name],
                                 target_spec['headers'][c_name]))

    add_field_comparison(analysis, 'content', base_spec, target_spec, lambda a: list(a.keys()))
    if 'content' in base_spec and 'content' in target_spec:
        for c_name, c_value in base_spec['content'].items():
            if c_name in target_spec['content']:
                analysis.content.append(
                    match_media_type(components, c_name, base_spec['content'][c_name], target_spec['content'][c_name]))

    return analysis
