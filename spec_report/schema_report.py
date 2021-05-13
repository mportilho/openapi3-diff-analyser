from spec_metadata.analysis_metadata import SchemaAnalysisResult, SchemaAnalysis

ERROR_KEY = '_ERROR_'
REPORT_KEY = '_SCHEMA_'
RESUME_KEY = '_RESUME_'


def create_report(analysis_result: SchemaAnalysisResult) -> str:
    report = ''
    report += f"""# Schemas\n
Análise dos objetos Schema da especificação OpenAPI 3 com base na documentação original.

Neste item, os Schemas definidos na documentação original serão comparados com a especificação da API alvo. Somente 
os Schemas originais presentes na especificação alvo serão analisados em detalhes e os demais ausentes ou extras 
serão apenas mencionados no relatório.\n\n"""

    report += f"#### Schemas Presentes\n\n"
    if len(analysis_result.present) > 0:
        report += f"{len(analysis_result.present)} schemas encontrados:\n\n"
        for name in analysis_result.present:
            report += f"- {name}\n"
    else:
        report += 'Nenhum schema encontrado\n\n'

    report += f"#### Schemas Ausentes\n\n"
    if len(analysis_result.absent) > 0:
        report += f"{len(analysis_result.absent)} schemas encontrados:\n\n"
        for name in analysis_result.absent:
            report += f"- {name}\n"
    else:
        report += 'Nenhum schema encontrado\n\n'

    report += f"#### Schemas Extras Presentes\n\n"
    if len(analysis_result.extra) > 0:
        report += f"{len(analysis_result.extra)} schemas encontrados:\n\n"
        for name in analysis_result.extra:
            report += f"- {name}\n"
    else:
        report += 'Nenhum schema encontrado\n\n'

    report_details = {}
    for schema_name in analysis_result.present:
        report_details[schema_name] = _create_schema_report(analysis_result.results[schema_name])

    report += '## Resumo das Diferenças Encontradas\n\n'
    schema_report = ''
    error_report = ''
    for name in report_details:
        schema_report += report_details[name][REPORT_KEY]
        if report_details[name][ERROR_KEY]:
            error_report += report_details[name][ERROR_KEY]
    if error_report:
        report += error_report
    else:
        report += 'Nenhuma inconformidade encontrada nos esquemas presentes'

    report += '\n\n-----------------------------\n\n'
    report += '## Detalhamento dos Schemas Exigidos\n\n' + schema_report

    return report


def _create_schema_report(schema_analyse: SchemaAnalysis, is_root=True) -> dict:
    r = {REPORT_KEY: '', ERROR_KEY: ''}
    title = f"""{'### Schema' if is_root else '#### Sub-Schema'} *{schema_analyse.name}*\n\n"""

    r[REPORT_KEY] = title
    r[ERROR_KEY] = ''

    for attribute in schema_analyse.attributes:
        attr_report = ''
        attr_report += f"""##### Atributo '{attribute.attribute_name}'\n"""
        attr_report += f"""- Estado: {'**correto**' if attribute.is_matching else '**incorreto**'}\n"""
        attr_report += f"""- Razão: {attribute.reason}\n"""
        attr_report += f"""- Dados Esperados: `{attribute.get_expected_value()}`\n"""
        attr_report += f"""- Dados Encontrados: `{attribute.get_current_value()}`\n\n"""
        r[REPORT_KEY] += attr_report
        if not attribute.is_matching:
            if not r[ERROR_KEY]:
                r[ERROR_KEY] = title
            r[ERROR_KEY] += attr_report

    if schema_analyse.items:
        r_items = _create_schema_report(schema_analyse.items, False)
        r[REPORT_KEY] += r_items[REPORT_KEY]
        r[ERROR_KEY] += r_items[ERROR_KEY]

    for prop in schema_analyse.properties:
        r_props = _create_schema_report(prop, False)
        r[REPORT_KEY] += r_props[REPORT_KEY]
        r[ERROR_KEY] += r_props[ERROR_KEY]

    return r
