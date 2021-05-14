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


def eval_analysis_obj(obj: Optional[GenericAnalysis]) -> bool:
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
        self.content: list[MediaTypeAnalysis] = []

    def evaluate(self):
        if self.is_ok is None:
            is_content = reduce(lambda a, b: a and b, map(lambda d: d.evaluate(), self.content), True)
            self.is_ok = super().evaluate() and is_content and eval_analysis_obj(self.schema)
        if self.is_ok is None:
            raise Exception('Avaliação de Schema não deve ser None')
        return self.is_ok


class MediaTypeAnalysis(GenericAnalysis):
    def __init__(self, name: str):
        super().__init__(name)
        self.schema: Optional[SchemaAnalysis] = None
        self.encoding: dict[str, EncodingAnalysis] = {}

    def evaluate(self):
        if self.is_ok is None:
            is_encoding = reduce(lambda a, b: a and b, map(lambda d: d.evaluate(), self.encoding.values()), True)
            self.is_ok = super().evaluate() and is_encoding and eval_analysis_obj(self.schema)
        if self.is_ok is None:
            raise Exception('Avaliação de Schema não deve ser None')
        return self.is_ok


class EncodingAnalysis(GenericAnalysis):
    def __init__(self, name: str):
        super().__init__(name)
        self.headers: dict[str, HeaderAnalysis] = {}

    def evaluate(self):
        if self.is_ok is None:
            is_headers = reduce(lambda a, b: a and b, map(lambda d: d.evaluate(), self.headers.values()), True)
            self.is_ok = super().evaluate() and is_headers
        if self.is_ok is None:
            raise Exception('Avaliação de Schema não deve ser None')
        return self.is_ok


class HeaderAnalysis(ParameterAnalysis):
    def __init__(self, name: str):
        super().__init__(name)


class RequestBodyAnalysis(GenericAnalysis):
    def __init__(self, name: str):
        super().__init__(name)
        self.content: dict[str, MediaTypeAnalysis] = {}

    def evaluate(self):
        if self.is_ok is None:
            is_content = reduce(lambda a, b: a and b, map(lambda d: d.evaluate(), self.content.values()), True)
            self.is_ok = super().evaluate() and is_content
        if self.is_ok is None:
            raise Exception('Avaliação de Schema não deve ser None')
        return self.is_ok


class ResponsesAnalysis(GenericAnalysis):
    def __init__(self, name: str):
        super().__init__(name)
        self.default: Optional[ResponseAnalysis] = None
        self.response: dict[str, ResponseAnalysis] = {}


class ResponseAnalysis(GenericAnalysis):
    def __init__(self, name: str):
        super().__init__(name)
        self.headers: dict[str, HeaderAnalysis] = {}
        self.content: dict[str, MediaTypeAnalysis] = {}

    def evaluate(self):
        if self.is_ok is None:
            is_content = reduce(lambda a, b: a and b, map(lambda d: d.evaluate(), self.content.values()), True)
            is_headers = reduce(lambda a, b: a and b, map(lambda d: d.evaluate(), self.headers.values()), True)
            self.is_ok = super().evaluate() and is_content and is_headers
        if self.is_ok is None:
            raise Exception('Avaliação de Schema não deve ser None')
        return self.is_ok


class OperationAnalysis(GenericAnalysis):
    def __init__(self, name: str):
        super().__init__(name)
        self.parameters: list[ParameterAnalysis] = []
        self.request_body: Optional[RequestBodyAnalysis] = None
        self.responses: list[ResponsesAnalysis] = []

    def evaluate(self):
        if self.is_ok is None:
            is_parameters = reduce(lambda a, b: a and b, map(lambda d: d.evaluate(), self.parameters), True)
            is_responses = reduce(lambda a, b: a and b, map(lambda d: d.evaluate(), self.responses), True)
            self.is_ok = super().evaluate() and is_parameters and is_responses and eval_analysis_obj(self.request_body)
        if self.is_ok is None:
            raise Exception('Avaliação de Schema não deve ser None')
        return self.is_ok


class PathItemAnalysis(GenericAnalysis):
    def __init__(self, name: str):
        super().__init__(name)
        self.get: Optional[OperationAnalysis] = None
        self.put: Optional[OperationAnalysis] = None
        self.post: Optional[OperationAnalysis] = None
        self.delete: Optional[OperationAnalysis] = None
        self.options: Optional[OperationAnalysis] = None
        self.head: Optional[OperationAnalysis] = None
        self.patch: Optional[OperationAnalysis] = None
        self.trace: Optional[OperationAnalysis] = None
        self.parameters: list[ParameterAnalysis] = []

    def evaluate(self):
        if self.is_ok is None:
            is_parameters = reduce(lambda a, b: a and b, map(lambda d: d.evaluate(), self.parameters), True)
            operations = filter(lambda a: a is not None,
                                [self.get, self.put, self.post, self.delete, self.options, self.head, self.patch,
                                 self.trace])
            is_op = reduce(lambda a, b: a and b, map(lambda a: a.evaluate(), operations), True)
            self.is_ok = super().evaluate() and is_parameters and is_op
        if self.is_ok is None:
            raise Exception('Avaliação de Schema não deve ser None')
        return self.is_ok


class PathAnalysis(GenericAnalysis):
    def __init__(self, name: str):
        super().__init__(name)
        self.path_items: dict[str, PathItemAnalysis] = {}

    def evaluate(self):
        if self.is_ok is None:
            is_path_items = reduce(lambda a, b: a and b, map(lambda d: d.evaluate(), self.path_items.values()), True)
            self.is_ok = super().evaluate() and is_path_items
        if self.is_ok is None:
            raise Exception('Avaliação de Schema não deve ser None')
        return self.is_ok
