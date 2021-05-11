from definitions import METADATA_RESULT
from structures.comparison_result import ComparisonResult
from structures.schema_analysis import SchemaResultMetadata
from structures.schema_comparison import SchemaComparison

ERROR_KEY = '_ERROR_'
REPORT_KEY = '_SCHEMA_'
RESUME_KEY = '_RESUME_'


def create_report(schema_comparison: SchemaComparison) -> str:
    report = ''
    report += f"""# Schemas\n
Análise dos objetos Schema da especificação OpenAPI 3 com base na documentação original.

Neste item, os Schemas definidos na documentação original serão comparados com a especificação da API alvo. Somente 
os Schemas originais presentes na especificação alvo serão analisados em detalhes e os demais ausentes ou extras 
serão apenas mencionados no relatório.\n\n"""

    found_text = 'item encontrado' if len(schema_comparison.present) <= 1 else 'itens encontrados'
    report += f"#### Schemas Presentes\n\n{len(schema_comparison.present)} {found_text}:\n\n"
    for found_schema in schema_comparison.present:
        report += f"- {found_schema}\n"

    found_text = 'item encontrado' if len(schema_comparison.absent) <= 1 else 'itens encontrados'
    report += f"\n#### Schemas Ausentes\n\n{len(schema_comparison.absent)} {found_text}:\n\n"
    for found_schema in schema_comparison.absent:
        report += f"- {found_schema}\n"

    found_text = 'item encontrado' if len(schema_comparison.extra) <= 1 else 'itens encontrados'
    report += f"\n#### Schemas Extras Encontrados\n\n{len(schema_comparison.extra)} {found_text}:\n\n"
    for found_schema in schema_comparison.extra:
        report += f"- {found_schema}\n"

    report_details = _prepare_report(schema_comparison)

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


def _prepare_report(schema_comparison: SchemaComparison) -> dict:
    report_dict = {}
    for schema_name in schema_comparison.present:
        report_dict[schema_name] = _create_schema_report(schema_comparison.result[schema_name])
    return report_dict


def _create_schema_report(schema: dict, is_root=True) -> dict:
    r = {REPORT_KEY: '', ERROR_KEY: ''}
    result_metadata: SchemaResultMetadata = schema[METADATA_RESULT]
    title = f"""{'### Schema' if is_root else '#### Sub-Schema'} *{result_metadata.name}*\n\n"""

    r[REPORT_KEY] = title
    r[ERROR_KEY] = ''

    for attr_name in result_metadata.attributes:
        attr_report = ''
        attr_comparison: ComparisonResult = result_metadata.attributes[attr_name]
        attr_report += f"""##### Atributo '{attr_comparison.attr_name}'\n"""
        attr_report += f"""- Estado: {'**correto**' if attr_comparison.equivalent else '**incorreto**'}\n"""
        attr_report += f"""- Razão: {attr_comparison.reason}\n"""
        attr_report += f"""- Dados Esperados: `{attr_comparison.get_source()}`\n"""
        attr_report += f"""- Dados Encontrados: `{attr_comparison.get_target()}`\n\n"""
        r[REPORT_KEY] += attr_report
        if not attr_comparison.equivalent:
            if not r[ERROR_KEY]:
                r[ERROR_KEY] = title
            r[ERROR_KEY] += attr_report

    prop_comparison: ComparisonResult = result_metadata.properties
    if prop_comparison:
        prop_report = ''
        prop_report += '##### Propriedades do Schema\n'
        prop_report += f"""- Estado: {'**correto**' if prop_comparison.equivalent else '**incorreto**'}\n"""
        prop_report += f"""- Razão: {prop_comparison.reason}\n"""
        prop_report += f"""- Propriedades Esperadas: `{prop_comparison.get_source()}`\n"""
        prop_report += f"""- Propriedades Encontradas: `{prop_comparison.get_target()}`\n\n"""
        r[REPORT_KEY] += prop_report
        if not prop_comparison.equivalent:
            if not r[ERROR_KEY]:
                r[ERROR_KEY] = title
            r[ERROR_KEY] = prop_report

    if result_metadata.items:
        r_items = _create_schema_report(result_metadata.items, False)
        r[REPORT_KEY] += r_items[REPORT_KEY]
        r[ERROR_KEY] += r_items[ERROR_KEY]

    for prop_name in result_metadata.all_properties:
        if prop_comparison is not None and prop_comparison.get_target():
            r_props = _create_schema_report(result_metadata.all_properties[prop_name], False)
            r[REPORT_KEY] += r_props[REPORT_KEY]
            r[ERROR_KEY] += r_props[ERROR_KEY]

    return r
