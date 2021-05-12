from comparator import schema_comparator, path_comparator
from report import schema_report, paths_report


def compare_specs(source_yaml_spec, target_yaml_spec):
    schema_comparison = schema_comparator.compare_schema(source_yaml_spec, target_yaml_spec)
    schema_report.create_report(schema_comparison)

    paths_report.create_report(source_yaml_spec['paths'])
