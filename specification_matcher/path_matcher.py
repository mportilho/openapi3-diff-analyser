from basic_operations.comparison_operations import compare_fields
from spec_metadata.analysis_metadata import PathsAnalysis
from spec_metadata.component_metadata import ComponentMetadata
from specification_matcher.path_item_matcher import match_path_item


def match_paths(components: dict[str, ComponentMetadata], spec_name: str, base_spec: dict,
                target_spec: dict) -> PathsAnalysis:
    analysis = PathsAnalysis(spec_name)
    analysis.fields = compare_fields(base_spec.keys(), base_spec, target_spec)

    for pi_name in spec_name:
        if pi_name in target_spec:
            analysis.path_items.append(
                match_path_item(components, f"ptm[{pi_name}]", base_spec[pi_name], target_spec[pi_name]))
    return analysis
