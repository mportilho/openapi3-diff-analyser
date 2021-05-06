from pathlib import Path
from definitions import ROOT_DIR

import yaml

from main import spec_comparator


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

    # openapi_obk = _load_yaml(Path(
    #     os.path.join(os.path.expanduser("~"), "temp", "ram", "email openbk hml", "swagger_channels_apis.yaml")))
    # openapi_api = _load_yaml(Path(
    #     os.path.join(os.path.expanduser("~"), "temp", "ram", "email openbk hml", "api-canais-atendimento.yaml")))

    # openapi_obk = _load_yaml(Path(
    #     os.path.join(os.path.expanduser("~"), "temp", "ram", "email openbk hml", "swagger_channels_apis.yaml")))
    # openapi_api = _load_yaml(Path(
    #     os.path.join(os.path.expanduser("~"), "temp", "ram", "email openbk hml", "api-canais-atendimento.yaml")))

    spec_comparator.compare_specs(openapi_obk, openapi_obk_control)


if __name__ == '__main__':
    execute_program()

    # a = {'a1': 1, 'a2': 2}
    # a. {'b1': 3, 'b2': 4}
    # print(a)

    # x = set(['A1', 'A2', 'A3', 'A4', 'B1'])
    # y = set(['A1', 'A2', 'A3', 'A4', 'A5'])
    #
    # print("List first: " + str(x))
    # print("List second: " + str(y))
    #
    # equal = x == y
    # print(f'Equals: {equal}')
    # print(str(x.difference(y)))
    # print(str(y.difference(x)))

# C:\Users\marce\temp\ram\email openbk hml
