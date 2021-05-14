from functools import reduce
from typing import Optional

from spec_metadata.component_metadata import ComponentMetadata


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

    def get_field(self, name: str) -> Optional[FieldMatchingData]:
        return next(filter(lambda a: a.field_name == name, self.fields), None)

    def evaluate(self):
        return reduce(lambda a, b: a and b, map(lambda a: a.is_matching, self.fields), True)

    def __str__(self):
        return f"{self.name}: '{self.evaluate()}'"


def eval_analysis_obj(obj: Optional[GenericAnalysis]) -> bool:
    return obj.evaluate() if obj is not None else True


class ComponentsAnalysis(GenericAnalysis):
    def __init__(self, name: str):
        super().__init__(name)
        self._components: dict[str, dict[str, GenericAnalysis]] = {}
        self.components_metadata: dict[str, ComponentMetadata]

    def set_component(self, component_name: str, component_item_name: str, component_item_analysis: GenericAnalysis):
        if component_name not in self._components:
            self._components[component_name] = {}
        self._components[component_name][component_item_name] = component_item_analysis

    def get_component(self, component_name: str) -> dict[str, GenericAnalysis]:
        return self._components[component_name] if component_name in self._components else {}

    def get_schemas(self) -> dict[str, GenericAnalysis]:
        return self.get_component('schemas')

    def get_responses(self) -> dict[str, GenericAnalysis]:
        return self.get_component('responses')

    def get_parameters(self) -> dict[str, GenericAnalysis]:
        return self.get_component('parameters')

    def get_request_bodies(self) -> dict[str, GenericAnalysis]:
        return self.get_component('requestBodies')

    def get_headers(self) -> dict[str, GenericAnalysis]:
        return self.get_component('headers')


class SchemaAnalysis(GenericAnalysis):
    def __init__(self, name: str):
        super().__init__(name)
        self.properties: list[SchemaAnalysis] = []
        self.items: Optional[SchemaAnalysis] = None

    def evaluate(self) -> bool:
        prop_ok: bool = reduce(lambda a, b: a and b, map(lambda a: a.evaluate(), self.properties), True)
        self.is_ok = super().evaluate() and prop_ok and eval_analysis_obj(self.items)
        if self.is_ok is None:
            raise Exception('Avaliação de Schema não deve ser None')
        return self.is_ok


# class SchemaAnalysisResult(object):
#     def __init__(self):
#         self.present: list[str] = []
#         self.absent: list[str] = []
#         self.extra: list[str] = []
#         self.results: dict[str, SchemaAnalysis] = {}


class ParameterAnalysis(GenericAnalysis):
    def __init__(self, name: str):
        super().__init__(name)
        self.schema: Optional[SchemaAnalysis] = None
        self.content: list[MediaTypeAnalysis] = []

    def evaluate(self):
        is_content = reduce(lambda a, b: a and b, map(lambda d: d.evaluate(), self.content), True)
        self.is_ok = super().evaluate() and is_content and eval_analysis_obj(self.schema)
        if self.is_ok is None:
            raise Exception('Avaliação de Schema não deve ser None')
        return self.is_ok


class MediaTypeAnalysis(GenericAnalysis):
    def __init__(self, name: str):
        super().__init__(name)
        self.schema: Optional[SchemaAnalysis] = None
        self.encoding: list[EncodingAnalysis] = []

    def evaluate(self):
        is_encoding = reduce(lambda a, b: a and b, map(lambda d: d.evaluate(), self.encoding), True)
        self.is_ok = super().evaluate() and is_encoding and eval_analysis_obj(self.schema)
        if self.is_ok is None:
            raise Exception('Avaliação de Schema não deve ser None')
        return self.is_ok


class EncodingAnalysis(GenericAnalysis):
    def __init__(self, name: str):
        super().__init__(name)
        self.headers: list[HeaderAnalysis] = []

    def evaluate(self):
        is_headers = reduce(lambda a, b: a and b, map(lambda d: d.evaluate(), self.headers), True)
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
        self.content: list[MediaTypeAnalysis] = []

    def evaluate(self):
        is_content = reduce(lambda a, b: a and b, map(lambda d: d.evaluate(), self.content), True)
        self.is_ok = super().evaluate() and is_content
        if self.is_ok is None:
            raise Exception('Avaliação de Schema não deve ser None')
        return self.is_ok


class ResponsesAnalysis(GenericAnalysis):
    def __init__(self, name: str):
        super().__init__(name)
        self.default: Optional[ResponseAnalysis] = None
        self.response: list[ResponseAnalysis] = []

    def evaluate(self):
        is_response = reduce(lambda a, b: a and b, map(lambda d: d.evaluate(), self.response), True)
        self.is_ok = super().evaluate() and is_response and eval_analysis_obj(self.default)
        if self.is_ok is None:
            raise Exception('Avaliação de Schema não deve ser None')
        return self.is_ok


class ResponseAnalysis(GenericAnalysis):
    def __init__(self, name: str):
        super().__init__(name)
        self.headers: list[HeaderAnalysis] = []
        self.content: list[MediaTypeAnalysis] = []

    def evaluate(self):
        is_content = reduce(lambda a, b: a and b, map(lambda d: d.evaluate(), self.content), True)
        is_headers = reduce(lambda a, b: a and b, map(lambda d: d.evaluate(), self.headers), True)
        self.is_ok = super().evaluate() and is_content and is_headers
        if self.is_ok is None:
            raise Exception('Avaliação de Schema não deve ser None')
        return self.is_ok


class OperationAnalysis(GenericAnalysis):
    def __init__(self, name: str):
        super().__init__(name)
        self.parameters: list[ParameterAnalysis] = []
        self.responses: Optional[ResponsesAnalysis] = None
        self.request_body: Optional[RequestBodyAnalysis] = None

    def evaluate(self):
        is_parameters = reduce(lambda a, b: a and b, map(lambda d: d.evaluate(), self.parameters), True)
        self.is_ok = super().evaluate() and is_parameters and eval_analysis_obj(self.responses) and eval_analysis_obj(
            self.request_body)
        if self.is_ok is None:
            raise Exception('Avaliação de Schema não deve ser None')
        return self.is_ok


class PathItemAnalysis(GenericAnalysis):
    def __init__(self, name: str):
        super().__init__(name)
        self.operations: dict[str, OperationAnalysis] = {}
        self.parameters: list[ParameterAnalysis] = []

    def evaluate(self):
        is_parameters = reduce(lambda a, b: a and b, map(lambda d: d.evaluate(), self.parameters), True)
        is_op = reduce(lambda a, b: a and b, map(lambda a: a.evaluate(), self.operations.values()), True)
        self.is_ok = super().evaluate() and is_parameters and is_op
        if self.is_ok is None:
            raise Exception('Avaliação de Schema não deve ser None')
        return self.is_ok


class PathsAnalysis(GenericAnalysis):
    def __init__(self, name: str):
        super().__init__(name)
        self.path_items: list[PathItemAnalysis] = []

    def evaluate(self):
        is_path_items = reduce(lambda a, b: a and b, map(lambda d: d.evaluate(), self.path_items), True)
        self.is_ok = super().evaluate() and is_path_items
        if self.is_ok is None:
            raise Exception('Avaliação de Schema não deve ser None')
        return self.is_ok
