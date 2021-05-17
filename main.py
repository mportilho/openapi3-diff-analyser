from pathlib import Path

import yaml

from definitions import ROOT_DIR
from reporting.component_report import create_component_report, create_paths_report
from specification_matcher.components_matcher import match_components
from specification_matcher.path_matcher import match_paths


def _load_yaml(openbk_swagger_path: Path):
    if not openbk_swagger_path.exists():
        raise Exception(f'Source file "{openbk_swagger_path}" was not found')
    with open(openbk_swagger_path, 'r', encoding='utf8') as file:
        yaml_obj = yaml.safe_load(file)
    return yaml_obj


def execute_program():
    openapi_obk = _load_yaml(Path(ROOT_DIR, "resources", "specs_obk", "swagger_channels_apis.yaml"))
    openapi_obk_control = _load_yaml(Path(ROOT_DIR, "resources", "specs_obk", "swagger_channels_apis_control.yaml"))
    openapi_api = _load_yaml(Path(ROOT_DIR, "resources", "specs_api", "api-comuns.yaml"))

    component_analysis = match_components(openapi_obk, openapi_obk_control)
    paths_analysis = match_paths(component_analysis.components_metadata, 'paths', openapi_obk, openapi_obk_control)

    text = create_component_report(component_analysis)
    text_path = create_paths_report(paths_analysis)
    comps_text = '\n'.join(text.report)
    paths_text = '\n'.join(text_path.report)
    final = paths_text + '\n\n' + comps_text

    error_comps_text = '\n'.join(text.error_report)
    error_paths_text = '\n'.join(text_path.error_report)
    error_final = error_paths_text + '\n\n' + error_comps_text

    print(final, error_final)


if __name__ == '__main__':
    execute_program()
