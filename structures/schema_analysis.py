from typing import Optional

from structures.comparison_result import ComparisonResult


class SchemaMetadata(object):
    def __init__(self, name: str):
        self.name: str = name
        self.visited: bool = False
        self.all_properties: dict = {}
        self.ref: dict = {}
        self.items: dict = {}

    def __str__(self):
        return f"name: {self.name}, visited: {self.visited}"


class SchemaResultMetadata(object):
    def __init__(self, name: str):
        self.name: str = name
        self.analysed: bool = False
        self.valid: bool = False
        self.is_present = True
        self.attributes: dict = {}
        self.properties: Optional[ComparisonResult] = None
        self.all_properties: dict = {}
        self.items: dict = {}

    def is_empty(self):
        return len(self.attributes) == 0 and len(self.all_properties) == 0 and self.properties is None

    def finish_analysis(self):
        self.valid = True
        if len(self.attributes) > 0:
            for attr in self.attributes:
                if not self.attributes[attr].equivalent:
                    self.valid = False
                    break
        if self.valid and self.properties is not None:
            self.valid = self.properties.equivalent

    def __str__(self):
        return f"name: {self.name}, analysed: {self.analysed}, valid: {self.valid}"
