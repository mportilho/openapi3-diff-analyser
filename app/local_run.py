from pathlib import Path

import yaml

from app.application.specification_diff import run_diff


def _load_yaml(openbk_swagger_path: Path):
    if not openbk_swagger_path.exists():
        raise Exception(f'Base comparison file "{openbk_swagger_path}" was not found')
    with open(openbk_swagger_path, 'r', encoding='utf8') as file:
        yaml_obj = yaml.safe_load(file)
    return yaml_obj


def run_local_program(base_spec_file: Path, target_spec_file: Path, output_location: Path, report_type: str = 'ERROR'):
    output_location.mkdir(exist_ok=True)
    openapi_obk = _load_yaml(base_spec_file)
    openapi_api = _load_yaml(target_spec_file)
    error_report, full_report = run_diff(openapi_obk, openapi_api)

    if report_type == 'FILE':
        with open(Path(output_location, 'complete_report.md'), 'w', encoding='utf-8') as file:
            file.write(full_report)
        with open(Path(output_location, 'error_report.md'), 'w', encoding='utf-8') as file:
            file.write(error_report)
    elif report_type == "ERROR":
        print(error_report)
    elif report_type == "FULL":
        print(full_report)
