from app.reporting.component_report import create_component_report, create_paths_report
from app.specification_matcher.components_matcher import match_components
from app.specification_matcher.path_matcher import match_paths


def run_diff(openapi_obk: dict, openapi_api: dict) -> tuple[str, str]:
    component_analysis = match_components(openapi_obk, openapi_api)
    paths_analysis = match_paths(component_analysis.components_metadata, 'paths', openapi_obk, openapi_api)

    text = create_component_report(component_analysis)
    text_path = create_paths_report(paths_analysis)
    comps_text = '\n'.join(text.report)
    paths_text = '\n'.join(text_path.report)
    final = paths_text + '\n\n' + comps_text

    error_comps_text = '\n'.join(text.error_report)
    error_paths_text = '\n'.join(text_path.error_report)
    error_final = error_paths_text + '\n\n' + error_comps_text
    return error_final, final
