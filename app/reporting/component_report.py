from pathlib import Path
from typing import cast, Optional

from app.definitions import ROOT_DIR
from app.spec_metadata.analysis_metadata import FieldMatchingData, SchemaAnalysis, ComponentsAnalysis, PathsAnalysis, \
    ParameterAnalysis, MediaTypeAnalysis, OperationAnalysis, ResponseAnalysis, HeaderAnalysis, ResponsesAnalysis, \
    RequestBodyAnalysis


class Reporting(object):
    def __init__(self):
        self.report: list[str] = []
        self.error_report: list[str] = []

    def all(self, text: str):
        self.report.append(text)
        self.error_report.append(text)


def _indent(indentation: int):
    if indentation > 6:
        indentation = 6
    return str(f"{{:#^{indentation}}}").format('')


def create_field_report(fields: list[FieldMatchingData]) -> Reporting:
    content = Reporting()
    for field in fields:
        c_list: list[str] = [f"- Campo: **`{field.field_name}`**",
                             f"- Estado: {'**correto**' if field.is_matching else '**incorreto**'}",
                             f"- Razão: {field.reason}", f"- Dados Esperados: `{field.get_expected_value()}`",
                             f"- Dados Encontrados: `{field.get_current_value()}`  \n&nbsp;\n"]
        content.report.extend(c_list)
        if not field.is_matching:
            content.error_report.extend(c_list)
    return content


def _add_error_report(header: str, error_report: list[str], f_content: Reporting):
    if len(error_report) > 0:
        if len(f_content.error_report) == 0:
            f_content.error_report.append(header)
        f_content.error_report.extend(error_report)


def _create_schema_report(indent: int, schema: SchemaAnalysis, is_root=True, prev_is_root=False) -> Reporting:
    if not is_root and prev_is_root:
        indent += 1
    header = f"""{_indent(indent)} {'Schema' if is_root else 'Sub-Schema'} *{schema.name}*\n"""
    content = Reporting()
    content.report.append(header)

    f_content = create_field_report(schema.fields)
    content.report.extend(f_content.report)
    _add_error_report(header, f_content.error_report, content)

    if schema.items:
        r_items = _create_schema_report(indent, schema.items, False, is_root)
        content.report.extend(r_items.report)
        _add_error_report(header, r_items.error_report, content)

    for prop in schema.properties:
        r_items = _create_schema_report(indent, prop, False, is_root)
        content.report.extend(r_items.report)
        _add_error_report(header, r_items.error_report, content)

    return content


def _prepare_schema_report(indent: int, comp_analysis: ComponentsAnalysis):
    content = Reporting()

    with open(Path(ROOT_DIR, 'app', 'resources', 'schema_description.txt'), 'r', encoding='utf-8') as file:
        content.all(file.read())

    content.all(f"{_indent(indent)} Schemas Presentes\n")
    if comp_analysis.get_schemas():
        presence = set(comp_analysis.get_field('schemas').get_expected_value()).intersection(
            comp_analysis.get_field('schemas').get_current_value())
        content.all(f"{len(presence)} schemas encontrados:\n")
        for name in presence:
            content.all(f"- {name}")
    else:
        content.all('Nenhum schema encontrado\n')

    content.all(f"\n{_indent(indent)} Schemas Ausentes\n")
    if comp_analysis.get_schemas():
        presence = set(comp_analysis.get_field('schemas').get_expected_value()).difference(
            comp_analysis.get_field('schemas').get_current_value())
        content.all(f"{len(presence)} schemas encontrados:\n")
        for name in presence:
            content.all(f"- {name}")
    else:
        content.all('Nenhum schema encontrado\n')

    content.all(f"\n{_indent(indent)} Schemas Extras Presentes\n")
    if comp_analysis.get_schemas():
        presence = set(comp_analysis.get_field('schemas').get_current_value()).difference(
            comp_analysis.get_field('schemas').get_expected_value())
        content.all(f"{len(presence)} schemas encontrados:\n")
        for name in presence:
            content.all(f"- {name}")
    else:
        content.all('Nenhum schema encontrado\n')

    schema_report = Reporting()
    for c_item in comp_analysis.get_schemas().values():
        report = _create_schema_report(indent, cast(SchemaAnalysis, c_item))
        schema_report.report.extend(report.report)
        _add_error_report('', report.error_report, schema_report)

    content.report.extend(schema_report.report)
    content.error_report.extend(schema_report.error_report)
    return content


def create_media_types_analysis(indent: int, media_types_analysis: list[MediaTypeAnalysis]):
    indent += 1
    content = Reporting()
    for media_type in media_types_analysis:
        header = f"{_indent(indent)} Media Type {media_type.name}\n"
        content.report.append(header)

        f_content = create_field_report(media_type.fields)
        content.report.extend(f_content.report)
        _add_error_report(header, f_content.error_report, content)

        s_content = _create_schema_report(indent + 1, media_type.schema)
        content.report.extend(s_content.report)
        _add_error_report(header, s_content.error_report, content)

    return content


def create_parameters_report(indent: int, parameters_analysis: list[ParameterAnalysis]):
    indent += 1
    content = Reporting()
    for param in parameters_analysis:
        header = f"{_indent(indent)} Parameter {param.name}\n"
        content.report.append(header)

        f_content = create_field_report(param.fields)
        content.report.extend(f_content.report)
        _add_error_report(header, f_content.error_report, content)

        p_content = create_media_types_analysis(indent, param.content)
        content.report.extend(p_content.report)
        _add_error_report(header, p_content.error_report, content)

        s_content = _create_schema_report(indent + 1, param.schema)
        content.report.extend(s_content.report)
        _add_error_report(header, s_content.error_report, content)

    return content


def create_headers_analysis(indent: int, headers: list[HeaderAnalysis]):
    indent += 1
    content = Reporting()
    for header in headers:
        header_title = f"{_indent(indent)} Header {header.name}\n"
        content.report.append(header_title)

        f_content = create_field_report(header.fields)
        content.report.extend(f_content.report)
        _add_error_report(header_title, f_content.error_report, content)

        mt_content = create_media_types_analysis(indent, header.content)
        content.report.extend(mt_content.report)
        _add_error_report(header_title, mt_content.error_report, content)

        s_content = _create_schema_report(indent + 1, header.schema)
        content.report.extend(s_content.report)
        _add_error_report(header_title, s_content.error_report, content)
    return content


def create_response_list_report(indent: int, responses: list[ResponseAnalysis]):
    indent += 1
    content = Reporting()
    for response in responses:
        header = f"{_indent(indent)} Response {response.name}\n"
        content.report.append(header)

        f_content = create_field_report(response.fields)
        content.report.extend(f_content.report)
        _add_error_report(header, f_content.error_report, content)

        p_content = create_media_types_analysis(indent, response.content)
        content.report.extend(p_content.report)
        _add_error_report(header, p_content.error_report, content)

        h_content = create_headers_analysis(indent, response.headers)
        content.report.extend(h_content.report)
        _add_error_report(header, h_content.error_report, content)

    return content


def create_responses_obj_report(indent: int, responses: Optional[ResponsesAnalysis]):
    content = Reporting()
    if responses:
        resp_param = []
        if responses.default is not None:
            resp_param.append(responses.default)
        if len(responses.responses) > 0:
            resp_param.extend(responses.responses)
        if len(resp_param) > 0:
            p_content = create_response_list_report(indent, resp_param)
            content.report.extend(p_content.report)
            _add_error_report('', p_content.error_report, content)
    return content


def create_request_body_report(indent: int, request_body: Optional[RequestBodyAnalysis]):
    indent += 1
    content = Reporting()
    if request_body is not None:
        header = f"{_indent(indent)} Request Body {request_body.name}\n"
        content.report.append(header)

        f_content = create_field_report(request_body.fields)
        content.report.extend(f_content.report)
        _add_error_report(header, f_content.error_report, content)

        mt_content = create_media_types_analysis(indent, request_body.content)
        content.report.extend(mt_content.report)
        _add_error_report(header, mt_content.error_report, content)

    return content


def create_operations_report(indent, operations: dict[str, OperationAnalysis]):
    content = Reporting()
    for operation in operations.values():
        header = f"{_indent(indent)} Operation {operation.name}\n"
        content.report.append(header)

        f_content = create_field_report(operation.fields)
        content.report.extend(f_content.report)
        _add_error_report(header, f_content.error_report, content)

        p_content = create_parameters_report(indent, operation.parameters)
        content.report.extend(p_content.report)
        _add_error_report(header, p_content.error_report, content)

        r_content = create_responses_obj_report(indent, operation.responses)
        content.report.extend(r_content.report)
        _add_error_report(header, r_content.error_report, content)

        rb_content = create_request_body_report(indent, operation.request_body)
        content.report.extend(rb_content.report)
        _add_error_report(header, rb_content.error_report, content)

    return content


def create_paths_report(paths_analysis: PathsAnalysis) -> Reporting:
    indent = 1
    content = Reporting()
    content.all(f"{_indent(indent)} Paths\n")

    indent += 1
    for path_item in paths_analysis.path_items:
        header = f"""{_indent(indent)} Path *{path_item.name}*\n"""
        content.report.append(header)

        f_content = create_field_report(path_item.fields)
        content.report.extend(f_content.report)
        _add_error_report(header, f_content.error_report, content)

        p_content = create_parameters_report(indent + 1, path_item.parameters)
        content.report.extend(p_content.report)
        _add_error_report(header, p_content.error_report, content)

        o_content = create_operations_report(indent + 1, path_item.operations)
        content.report.extend(o_content.report)
        _add_error_report(header, o_content.error_report, content)
    if len(paths_analysis.path_items) == 0:
        content.all('Nenhum objeto "PathItem" encontrado')

    if len(content.error_report) == 1:
        content.error_report.append('Nenhuma inconsistência encontrada')

    return content


def create_component_report(component_analysis: ComponentsAnalysis) -> Reporting:
    indentation = 1
    content = Reporting()
    content.all(f"{_indent(indentation)} Components\n")

    indentation += 1
    for comp_name, comp in component_analysis.components.items():
        if 'schemas' == comp_name:
            content.all(f"{_indent(indentation)} Schemas\n")
            s_report = _prepare_schema_report(indentation + 1, component_analysis)
            content.report.extend(s_report.report)
            content.error_report.extend(s_report.error_report)

    return content
