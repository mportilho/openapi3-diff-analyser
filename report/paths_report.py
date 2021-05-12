def create_report(paths) -> str:
    report = ''
    report += '# Paths\n\n'
    operations = ['get', 'put', 'post', 'delete', 'options', 'head', 'patch', 'trace']

    for path_name in paths:
        report += f"## Path {path_name}\n\n"
        for op_name in operations:
            if op_name in paths[path_name]:
                report += _report_operation(op_name, paths[path_name][op_name])

    return report


def _report_operation(op_name: str, operation: dict) -> str:
    report = f"### Operation '{op_name}'\n\n"
    return report


def _report_response(response: dict) -> str:
    print()


def _report_parameter(parameter: dict) -> str:
    print()
