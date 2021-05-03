import os
from pathlib import Path

import yaml

from processors import schema_processor


def execute_program():
    openbk_swagger_path = Path(
        os.path.join(os.path.expanduser("~"), "temp", "ram", "email openbk hml", "swagger_channels_apis.yaml"))
    if not openbk_swagger_path.exists():
        raise Exception(f'Source file "{openbk_swagger_path}" was not found')
    with open(openbk_swagger_path, 'r', encoding='utf8') as file:
        openapi_obk = yaml.safe_load(file)
    schema_processor.process(openapi_obk)


if __name__ == '__main__':
    execute_program()

# C:\Users\marce\temp\ram\email openbk hml
