from pathlib import Path

import yaml

from app.application.specification_diff import run_diff
from app.definitions import ROOT_DIR


def _load_yaml(openbk_swagger_path: Path):
    if not openbk_swagger_path.exists():
        raise Exception(f'Source file "{openbk_swagger_path}" was not found')
    with open(openbk_swagger_path, 'r', encoding='utf8') as file:
        yaml_obj = yaml.safe_load(file)
    return yaml_obj


def run_local_program():
    openapi_obk = _load_yaml(Path(ROOT_DIR, "..", "resources", "specs_obk", "swagger_common_apis.yaml"))
    # openapi_obk_control = _load_yaml(Path(ROOT_DIR, "resources", "specs_obk", "swagger_channels_apis_control.yaml"))
    openapi_api = _load_yaml(Path(ROOT_DIR, "..", "resources", "specs_api", "api-comuns.yaml"))

    error_final, final = run_diff(openapi_obk, openapi_api)

    with open(Path(ROOT_DIR, '..', 'target', 'complete_report.md'), 'w', encoding='utf-8') as file:
        file.write(final)
    with open(Path(ROOT_DIR, '..', 'target', 'error_report.md'), 'w', encoding='utf-8') as file:
        file.write(error_final)


if __name__ == '__main__':
    run_local_program()
