import os
from pathlib import Path

import yaml

from processors import schema_processor


def _load_yaml(openbk_swagger_path: Path):
    if not openbk_swagger_path.exists():
        raise Exception(f'Source file "{openbk_swagger_path}" was not found')
    with open(openbk_swagger_path, 'r', encoding='utf8') as file:
        yaml_obj = yaml.safe_load(file)
    return yaml_obj


def execute_program():
    openapi_obk = _load_yaml(Path(
        os.path.join(os.path.expanduser("~"), "temp", "ram", "email openbk hml", "swagger_common_apis.yaml")))
    openapi_api = _load_yaml(Path(
        os.path.join(os.path.expanduser("~"), "temp", "ram", "email openbk hml", "api-comuns.yaml")))

    # openapi_obk = _load_yaml(Path(
    #     os.path.join(os.path.expanduser("~"), "temp", "ram", "email openbk hml", "swagger_channels_apis.yaml")))
    # openapi_api = _load_yaml(Path(
    #     os.path.join(os.path.expanduser("~"), "temp", "ram", "email openbk hml", "api-canais-atendimento.yaml")))

    # openapi_obk = _load_yaml(Path(
    #     os.path.join(os.path.expanduser("~"), "temp", "ram", "email openbk hml", "swagger_channels_apis.yaml")))
    # openapi_api = _load_yaml(Path(
    #     os.path.join(os.path.expanduser("~"), "temp", "ram", "email openbk hml", "api-canais-atendimento.yaml")))

    # api-canais-atendimento.yaml
    schema_obk: dict = schema_processor.process(openapi_obk)
    schema_api: dict = schema_processor.process(openapi_api)

    print(schema_obk)
    print(schema_api)


if __name__ == '__main__':
    execute_program()

# C:\Users\marce\temp\ram\email openbk hml
