import functools
from typing import Optional


class AttributeMatchingData(object):
    def __init__(self, attribute_name: str):
        self.attribute_name: str = attribute_name
        self._expected_value = None
        self._current_value = None
        self.is_matching: bool = False
        self.reason: str = ''

    def __str__(self):
        return f"{self.attribute_name}: '{self.is_matching}'; expected: {self._expected_value}; " \
               f"current: {self._current_value}"

    def set_values(self, expected_value, current_value):
        self._expected_value = expected_value
        self._current_value = current_value

    def get_expected_value(self):
        return self._expected_value

    def get_current_value(self):
        return self._current_value


class SchemaAnalysis(object):
    def __init__(self, name: str, attributes: list[AttributeMatchingData]):
        self.name: str = name
        self.attributes: list[AttributeMatchingData] = attributes
        self.properties: list[SchemaAnalysis] = []
        self.items: Optional[SchemaAnalysis] = None
        self._is_ok: Optional[bool] = None

    def evaluate(self) -> bool:
        if self._is_ok is None:
            attr_ok: bool = functools.reduce(lambda a, b: a and b, map(lambda a: a.is_matching, self.attributes), True)
            prop_ok: bool = functools.reduce(lambda a, b: a and b, map(lambda a: a.evaluate(), self.properties), True)
            self._is_ok = attr_ok and prop_ok and (self.items.evaluate() if self.items is not None else True)
        if self._is_ok is None:
            raise Exception('Avaliação de Schema não deve ser None')
        return self._is_ok

    def __str__(self):
        return f"{self.name}: '{self.evaluate()}'"


class SchemaAnalysisResult(object):
    def __init__(self):
        self.present: list[str] = []
        self.absent: list[str] = []
        self.extra: list[str] = []
        self.results: dict[str, SchemaAnalysis] = {}
