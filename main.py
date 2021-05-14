from pathlib import Path

import yaml

from definitions import ROOT_DIR
from reporting import schema_report
from specification_matcher.components_matcher import match_components


def _load_yaml(openbk_swagger_path: Path):
    if not openbk_swagger_path.exists():
        raise Exception(f'Source file "{openbk_swagger_path}" was not found')
    with open(openbk_swagger_path, 'r', encoding='utf8') as file:
        yaml_obj = yaml.safe_load(file)
    return yaml_obj


def execute_program():
    openapi_obk = _load_yaml(Path(ROOT_DIR, "resources", "specs_obk", "swagger_common_apis.yaml"))
    openapi_obk_control = _load_yaml(Path(ROOT_DIR, "resources", "specs_obk", "swagger_channels_apis_control.yaml"))
    openapi_api = _load_yaml(Path(ROOT_DIR, "resources", "specs_api", "api-comuns.yaml"))

    component_analysis = match_components(openapi_obk, openapi_api)
    text = schema_report.create_report(component_analysis)
    print(text)


if __name__ == '__main__':
    execute_program()
