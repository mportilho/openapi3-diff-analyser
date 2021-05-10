from definitions import METADATA_RESULT
from structures.comparison_result import ComparisonResult
from structures.schema_analysis import SchemaResultMetadata
from structures.schema_comparison import SchemaComparison


def create_report(schema_comparison: SchemaComparison) -> str:
    report = ''
    report += f"""## Schemas\n
Análise dos objetos Schema da especificação OpenAPI 3 com base na documentação original.

Neste item, os Schemas definidos na documentação original serão comparados com a especificação da API alvo. Somente 
os Schemas originais presentes na especificação alvo serão analisados em detalhes e os demais ausentes ou extras 
serão apenas mencionados no relatório.\n\n"""

    found_text = 'item encontrado' if len(schema_comparison.present) <= 1 else 'itens encontrados'
    report += f"##### Schemas Presentes\n\n{len(schema_comparison.present)} {found_text}:\n\n"
    for found_schema in schema_comparison.present:
        report += f"- {found_schema}\n"

    found_text = 'item encontrado' if len(schema_comparison.absent) <= 1 else 'itens encontrados'
    report += f"\n##### Schemas Ausentes\n\n{len(schema_comparison.absent)} {found_text}:\n\n"
    for found_schema in schema_comparison.absent:
        report += f"- {found_schema}\n"

    found_text = 'item encontrado' if len(schema_comparison.extra) <= 1 else 'itens encontrados'
    report += f"\n##### Schemas Extras Encontrados\n\n{len(schema_comparison.extra)} {found_text}:\n\n"
    for found_schema in schema_comparison.extra:
        report += f"- {found_schema}\n"

    errors: dict = {}
    schema_report = ''
    for schema_name in schema_comparison.present:
        schema_report += _create_schema_report(schema_comparison.result[schema_name], errors)

    report += '## Resumo das Diferenças Encontradas\n\n'
    error_report = ''
    for name in errors:
        error_report += f"### Elemento {name}\n\n"
        if len(errors[name]['attributes']) > 0:
            error_report += '> **Atributos:**\n'
            for err_msg in errors[name]['attributes']:
                error_report += f"- {err_msg}\n"
            error_report += '\n'
        if errors[name]['properties']:
            error_report += '> **Resumo das Propriedades:**\n\n'
            error_report += f"{errors[name]['properties']}"

    if error_report:
        report += error_report
    else:
        report += 'Nenhuma inconformidade encontrada'

    report += '\n\n-----------------------------\n\n' + schema_report
    return report


def _create_schema_report(schema: dict, errors: dict, is_root=True) -> str:
    result_metadata: SchemaResultMetadata = schema[METADATA_RESULT]
    attr_errors = list()
    prop_error = ''

    report = f"""{'### Schema' if is_root else '#### Sub-Schema'} *{result_metadata.name}*\n\n"""

    for attr_name in result_metadata.attributes:
        attr_comparison: ComparisonResult = result_metadata.attributes[attr_name]
        report += f"""***Atributo '{attr_comparison.attr_name}'***\n"""
        report += f"""- Estado: {'**correto**' if attr_comparison.equivalent else '**incorreto**'}\n"""
        report += f"""- Razão: {attr_comparison.reason}\n"""
        report += f"""- Dados Esperados: `{attr_comparison.get_source()}`\n"""
        report += f"""- Dados Encontrados: `{attr_comparison.get_target()}`\n\n"""
        if not attr_comparison.equivalent:
            attr_errors.append(F"**{attr_comparison.attr_name}**: {attr_comparison.reason}")

    prop_comparison: ComparisonResult = result_metadata.properties
    if prop_comparison:
        report += '***Propriedades do Schema***\n'
        report += f"""- Estado: {'**correto**' if prop_comparison.equivalent else '**incorreto**'}\n"""
        report += f"""- Razão: {prop_comparison.reason}\n"""
        report += f"""- Propriedades Esperadas: `{prop_comparison.get_source()}`\n"""
        report += f"""- Propriedades Encontradas: `{prop_comparison.get_target()}`\n\n"""
        if not prop_comparison.equivalent:
            prop_error = prop_comparison.reason

    if len(attr_errors) > 0 or prop_error:
        errors[result_metadata.name] = {}
        errors[result_metadata.name]['attributes'] = attr_errors
        errors[result_metadata.name]['properties'] = prop_error

    if result_metadata.items:
        report += _create_schema_report(result_metadata.items, errors, False)

    for prop_name in result_metadata.all_properties:
        if prop_comparison is not None and prop_comparison.get_target():
            report += _create_schema_report(result_metadata.all_properties[prop_name], errors, False)

    return report
