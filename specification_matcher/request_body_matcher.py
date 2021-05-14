from basic_operations.comparison_operations import add_field_comparison
from spec_metadata.analysis_metadata import RequestBodyAnalysis
from spec_metadata.component_metadata import ComponentMetadata
from specification_matcher import media_type_matcher


def match_request_body(components: dict[str, ComponentMetadata], spec_name: str, base_spec: dict,
                       target_spec: dict) -> RequestBodyAnalysis:
    analysis = RequestBodyAnalysis(spec_name)
    add_field_comparison(analysis, 'required', base_spec, target_spec)
    add_field_comparison(analysis, 'content', base_spec, target_spec, lambda a: list(a.keys()))
    if 'content' in base_spec and 'content' in target_spec:
        for c_name, c_value in base_spec.items():
            if c_name in target_spec['content']:
                analysis.content.append(
                    media_type_matcher.match_media_type(components, f"cnt[{c_name}]", base_spec, target_spec))
    return analysis
