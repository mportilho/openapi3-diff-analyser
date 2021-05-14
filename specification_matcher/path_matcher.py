from basic_operations.comparison_operations import compare_fields
from spec_metadata.analysis_metadata import PathsAnalysis
from spec_metadata.component_metadata import ComponentMetadata
from specification_matcher.path_item_matcher import match_path_item


def match_paths(components: dict[str, ComponentMetadata], spec_name: str, base_spec: dict,
                target_spec: dict) -> PathsAnalysis:
    analysis = PathsAnalysis(spec_name)
    analysis.fields = compare_fields('paths', base_spec, target_spec, lambda a: list(a.keys()))

    for pi_name in base_spec['paths']:
        if pi_name in target_spec['paths']:
            analysis.path_items.append(
                match_path_item(components, f"ptm[{pi_name}]", base_spec['paths'][pi_name],
                                target_spec['paths'][pi_name]))
    return analysis
