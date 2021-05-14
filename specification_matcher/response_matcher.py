from basic_operations.comparison_operations import add_field_comparison
from spec_metadata.analysis_metadata import ResponseAnalysis
from spec_metadata.component_metadata import ComponentMetadata
from specification_matcher.header_matcher import match_header
from specification_matcher.media_type_matcher import match_media_type


def match_response(components: dict[str, ComponentMetadata], spec_name: str, base_spec: dict,
                   target_spec: dict) -> ResponseAnalysis:
    analysis = ResponseAnalysis(spec_name)

    add_field_comparison(analysis, 'headers', base_spec, target_spec, lambda a: list(a.keys()))
    if 'headers' in base_spec and 'headers' in target_spec:
        for c_name, c_value in base_spec.items():
            if c_name in target_spec['headers']:
                analysis.headers.append(match_header(components, f"hdr[{c_name}]", base_spec, target_spec))

    add_field_comparison(analysis, 'content', base_spec, target_spec, lambda a: list(a.keys()))
    if 'content' in base_spec and 'content' in target_spec:
        for c_name, c_value in base_spec.items():
            if c_name in target_spec['content']:
                analysis.content.append(
                    match_media_type(components, f"cnt[{c_name}]", base_spec, target_spec))

    return analysis