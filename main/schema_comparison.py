import copy


class SchemaComparison(object):
    def __init__(self, source_spec: dict, target_spec: dict):
        self.source: dict = source_spec
        self.target: dict = target_spec
        self.present: list[str] = []
        self.absent: list[str] = []
        self.extra: list[str] = []
        self.result: dict = copy.deepcopy(source_spec)

    def analyse(self):
        _analyse_presence(self)


def _analyse_presence(result_schema: SchemaComparison):
    for schema_name in result_schema.source:
        if schema_name in result_schema.target:
            result_schema.present.append(schema_name)
        else:
            result_schema.absent.append(schema_name)

    for schema_name in result_schema.target:
        if schema_name not in result_schema.source:
            result_schema.extra.append(schema_name)
