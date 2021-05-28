import getopt
import sys
from functools import reduce
from pathlib import Path

import yaml

import app.api_server as server
import app.local_run as local_program
from app.application.specification_diff import run_diff
from definitions import ROOT_DIR

cmd_example = 'main.py -i <inputfile> -o <outputfile>'


def _load_yaml(openbk_swagger_path: Path):
    if not openbk_swagger_path.exists():
        raise Exception(f'Source file "{openbk_swagger_path}" was not found')
    with open(openbk_swagger_path, 'r', encoding='utf8') as file:
        yaml_obj = yaml.safe_load(file)
    return yaml_obj


def run_local_program():
    openapi_obk = _load_yaml(Path(ROOT_DIR, 'app', "resources", "specs_obk", "swagger_channels_apis.yaml"))
    # openapi_obk_control = _load_yaml(Path(ROOT_DIR, "resources", "specs_obk", "swagger_channels_apis_control.yaml"))
    openapi_api = _load_yaml(Path(ROOT_DIR, "app", "resources", "specs_api", "api-canais-atendimento.yaml"))

    error_final, final = run_diff(openapi_obk, openapi_api)

    with open(Path(ROOT_DIR, '..', 'target', 'complete_report.md'), 'w', encoding='utf-8') as file:
        file.write(final)
    with open(Path(ROOT_DIR, '..', 'target', 'error_report.md'), 'w', encoding='utf-8') as file:
        file.write(error_final)


def run_local(opts):
    input_file = ''
    output_file = ''
    for opt, arg in opts:
        if opt in ('-h', '--help'):
            print(cmd_example)
            sys.exit()
        elif opt in ("-b", "--base"):
            input_file = arg
        elif opt in ("-t", "--target"):
            output_file = arg
    print('Input file is "', input_file)
    print('Output file is "', output_file)
    local_program.run_local_program(Path(input_file), Path(output_file), Path(ROOT_DIR, 'target'))


def main(argv: list[str]):
    short_ops = ''.join(['h', 'b:', 't:'])
    long_ops = ['help', 'base_file=', 'target_file=', 'server']
    try:
        opts, args = getopt.getopt(argv, short_ops, long_ops)
    except getopt.GetoptError:
        print(cmd_example)
        sys.exit(2)

    run_on_server = reduce(lambda a, b: a or b, map(lambda c: c[0] == '--server', opts), False)
    if run_on_server:
        server.app.run(host='0.0.0.0')
    else:
        run_local(opts)


if __name__ == '__main__':
    main(sys.argv[1:])
