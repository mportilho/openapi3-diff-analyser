from pathlib import Path

import yaml

from definitions import ROOT_DIR
from spec_metadata.component_metadata import analyse_components
from spec_object_matcher import schema_matcher


def _load_yaml(openbk_swagger_path: Path):
    if not openbk_swagger_path.exists():
        raise Exception(f'Source file "{openbk_swagger_path}" was not found')
    with open(openbk_swagger_path, 'r', encoding='utf8') as file:
        yaml_obj = yaml.safe_load(file)
    return yaml_obj


def execute_program():
    openapi_obk = _load_yaml(Path(ROOT_DIR, "resources", "specs_obk", "swagger_channels_apis.yaml"))
    openapi_obk_control = _load_yaml(Path(ROOT_DIR, "resources", "specs_obk", "swagger_channels_apis_control.yaml"))
    openapi_api = _load_yaml(Path(ROOT_DIR, "resources", "specs_api", "api-canais-atendimento.yaml"))

    # spec_comparator.compare_specs(openapi_obk, openapi_obk_control)

    components_metadata = analyse_components(openapi_obk)
    schema_matcher.match_schema(components_metadata, openapi_obk['components']['schemas']['ResponseBankingAgentsList'],
                                openapi_obk['components']['schemas']['ResponseBankingAgentsList'])
    print()


if __name__ == '__main__':
    execute_program()
