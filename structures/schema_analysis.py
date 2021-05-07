from structures.comparison_result import ComparisonResult


class SchemaMetadata(object):
    def __init__(self, name: str):
        self.name: str = name
        self.visited: bool = False
        self.all_properties: dict = {}

    def __str__(self):
        return f"name: {self.name}, visited: {self.visited}"


class SchemaResultMetadata(object):
    def __init__(self, name: str):
        self.name: str = name
        self.analysed: bool = False
        self.attributes: dict = {}
        self.properties: ComparisonResult

    def __str__(self):
        return f"name: {self.name}, analysed: {self.analysed}"
