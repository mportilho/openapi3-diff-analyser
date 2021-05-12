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
        self._analyse_presence()

    def _analyse_presence(self):
        for schema_name in self.source:
            if schema_name in self.target:
                self.present.append(schema_name)
            else:
                self.absent.append(schema_name)

        for schema_name in self.target:
            if schema_name not in self.source:
                self.extra.append(schema_name)


class PathComparison(object):
    def __init__(self, source_spec: dict, target_spec: dict):
        self.source: dict = source_spec
        self.target: dict = target_spec

    def analyse(self):
        self.source
        print()
