from functools import reduce
from typing import Optional


class FieldMatchingData(object):
    def __init__(self, field_name: str):
        self.field_name: str = field_name
        self._expected_value = None
        self._current_value = None
        self.is_matching: bool = False
        self.reason: str = ''

    def __str__(self):
        return f"{self.field_name}: '{self.is_matching}'; expected: {self._expected_value}; " \
               f"current: {self._current_value}"

    def set_values(self, expected_value, current_value):
        self._expected_value = expected_value
        self._current_value = current_value

    def get_expected_value(self):
        return self._expected_value

    def get_current_value(self):
        return self._current_value


class GenericAnalysis(object):
    def __init__(self, name: str):
        self.name: str = name
        self.fields: list[FieldMatchingData] = []
        self.is_ok: Optional[bool] = None

    def evaluate(self):
        return reduce(lambda a, b: a and b, map(lambda a: a.is_matching, self.fields), True)

    def __str__(self):
        return f"{self.name}: '{self.evaluate()}'"


def eval_analysis_obj(obj: Optional[GenericAnalysis]):
    return obj.evaluate() if obj is not None else True


class SchemaAnalysis(GenericAnalysis):
    def __init__(self, name: str):
        super().__init__(name)
        self.properties: list[SchemaAnalysis] = []
        self.items: Optional[SchemaAnalysis] = None

    def evaluate(self) -> bool:
        if self.is_ok is None:
            prop_ok: bool = reduce(lambda a, b: a and b, map(lambda a: a.evaluate(), self.properties), True)
            self.is_ok = super().evaluate() and prop_ok and eval_analysis_obj(self.items)
        if self.is_ok is None:
            raise Exception('Avaliação de Schema não deve ser None')
        return self.is_ok


class SchemaAnalysisResult(object):
    def __init__(self):
        self.present: list[str] = []
        self.absent: list[str] = []
        self.extra: list[str] = []
        self.results: dict[str, SchemaAnalysis] = {}


class ParameterAnalysis(GenericAnalysis):
    def __init__(self, name: str):
        super().__init__(name)
        self.schema: Optional[SchemaAnalysis] = None

    def evaluate(self):
        if self.is_ok is None:
            self.is_ok = super().evaluate() and eval_analysis_obj(self.schema)
        if self.is_ok is None:
            raise Exception('Avaliação de Schema não deve ser None')
        return self.is_ok


class MediaTypeAnalysis(GenericAnalysis):
    def __init__(self, name: str):
        super().__init__(name)
        self.schema: Optional[SchemaAnalysis] = None

    def evaluate(self):
        if self.is_ok is None:
            self.is_ok = super().evaluate() and eval_analysis_obj(self.schema)
        if self.is_ok is None:
            raise Exception('Avaliação de Schema não deve ser None')
        return self.is_ok
