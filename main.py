from pathlib import Path

import yaml

from definitions import ROOT_DIR
from reporting import schema_report
from spec_metadata.component_metadata import analyse_components
from specification_matcher import schema_matcher


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

    components = {'base': analyse_components(openapi_obk), 'target': analyse_components(openapi_api)}

    schema_result = schema_matcher.match_schema_specification(components, openapi_obk['components']['schemas'],
                                                              openapi_api['components']['schemas'])
    text = schema_report.create_report(schema_result)
    print(text)


if __name__ == '__main__':
    execute_program()
