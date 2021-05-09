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

    report += f"##### Schemas Presentes - {len(schema_comparison.present)} Itens\n\n"
    for found_schema in schema_comparison.present:
        report += f"- {found_schema}\n"

    report += f"\n##### Schemas Ausentes - {len(schema_comparison.absent)} Itens\n\n"
    for found_schema in schema_comparison.absent:
        report += f"- {found_schema}\n"

    report += f"\n##### Schemas Extras Encontrados - {len(schema_comparison.extra)} Itens\n\n"
    for found_schema in schema_comparison.extra:
        report += f"- {found_schema}\n"

    for schema_name in schema_comparison.present:
        report += _create_schema_report(schema_comparison.result[schema_name])

    return report


def _create_schema_report(schema: dict, is_root=True) -> str:
    if METADATA_RESULT not in schema:
        print()

    result_metadata: SchemaResultMetadata = schema[METADATA_RESULT]
    report = f"""{'### Schema' if is_root else '#### Sub-Schema'} *{result_metadata.name}*\n\n"""

    for attr_name in result_metadata.attributes:
        attr_comparison: ComparisonResult = result_metadata.attributes[attr_name]
        report += f"""***Atributo '{attr_comparison.attr_name}'***\n"""
        report += f"""- Estado: {'**correto**' if attr_comparison.equivalent else '**incorreto**'}\n"""
        report += f"""- Razão: {attr_comparison.reason}\n"""
        report += f"""- Dados Esperados: {attr_comparison.get_source()}\n"""
        report += f"""- Dados Encontrados: {attr_comparison.get_target()}\n\n"""

    prop_comparison: ComparisonResult = result_metadata.properties
    if prop_comparison:
        report += '***Propriedades do Schema***\n'
        report += f"""- Propriedades {'**equivalentes**' if prop_comparison.equivalent else 'incorretas'}\n"""
        report += f"""- Propriedades Esperadas: {prop_comparison.get_source()}\n"""
        report += f"""- Propriedades Encontradas: {prop_comparison.get_target()}\n\n"""

    for prop_name in result_metadata.all_properties:
        report += _create_schema_report(result_metadata.all_properties[prop_name], False)

    return report
