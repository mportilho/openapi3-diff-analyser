import getopt
import sys
from pathlib import Path

import app.api_server as server
import app.local_run as local_program
from definitions import ROOT_DIR


def print_usage():
    text = """
OpenAPI3 Diff Analyser

Compares a OpenAPI3 base specification to a target specification. It can run as a standalone CLI Program or a REST API \
server 

USAGE: CLI Program:
    py main.py -b <base_file> -t <target_file> [-o <output_dir>]

USAGE: REST API Server:
    py main.py --server

Options:
    --server=[]: Starts up a REST API Server listening on port 5000 by default or a given port number.
    -rt, --report_type: 
        FILE: creates error and full reports on the output_dir
        ERROR: returns the error report to the console
        FULL: returns the full report to the console
    -b, --base: Path to the OpenAPI3 specification base file for comparison.
    -t, --target: Path to the OpenAPI3 specification target file for comparison.
    -o, --output_dir: Optional directory for writing comparison reports. Defaults to './target'. 
    -h, --help: prints help doc
    """
    print(text)


def run_local(opts):
    base_file = ''
    target_file = ''
    output_dir = ''
    report_type = 'ERROR'
    for opt, arg in opts:
        if opt in ('-h', '--help'):
            print_usage()
            sys.exit()
        elif opt in ("-b", "--base"):
            base_file = arg
        elif opt in ("-t", "--target"):
            target_file = arg
        elif opt in ("-o", "--output_dir"):
            output_dir = arg
        elif opt in ("-rt", "--report_type"):
            output_dir = arg
    output_dir = Path(output_dir) if output_dir != '' else Path(ROOT_DIR, 'target')
    local_program.run_local_program(Path(base_file), Path(target_file), output_dir, report_type)


def main(argv: list[str]):
    short_ops = ''.join(['h', 'b:', 't:', 'rt:', 'o:'])
    long_ops = ['help', 'base_file=', 'target_file=', 'output_dir=', 'server=', 'report_type=']
    try:
        opts, args = getopt.getopt(argv, short_ops, long_ops)
    except getopt.GetoptError:
        print_usage()
        sys.exit(2)

    server_opts = [server_opt for server_opt in opts if server_opt[0] == '--server']
    if server_opts:
        server.app.run(host='0.0.0.0', port=server_opts[0][1])
    else:
        run_local(opts)


if __name__ == '__main__':
    main(sys.argv[1:])
