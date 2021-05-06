from main import schema_comparator


def compare_specs(source_yaml_spec, target_yaml_spec):
    schema_comparator.compare_schema(source_yaml_spec, target_yaml_spec)
