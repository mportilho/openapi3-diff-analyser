from functools import reduce
from typing import Optional

from app.definitions import ANALYSIS_COMPONENTS
from app.spec_metadata.component_metadata import ComponentMetadata


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

    def evaluate_fields(self):
        return reduce(lambda a, b: a and b, map(lambda a: a.is_matching, self.fields), True)

    def evaluate(self):
        return self.evaluate_fields()

    def __str__(self):
        return f"{self.name}: '{self.evaluate()}'"


def eval_analysis_obj(obj: Optional[GenericAnalysis]) -> bool:
    return obj.evaluate() if obj is not None else True


class ComponentsAnalysis(GenericAnalysis):
    def __init__(self, name: str):
        super().__init__(name)
        self.components: dict[str, dict[str, GenericAnalysis]] = {}
        self.components_metadata: dict[str, ComponentMetadata] = {}

    def set_component(self, component_name: str, component_item_name: str, component_item_analysis: GenericAnalysis):
        if component_name not in self.components:
            self.components[component_name] = {}
        self.components[component_name][component_item_name] = component_item_analysis

    def get_component(self, component_name: str) -> dict[str, GenericAnalysis]:
        return self.components[component_name] if component_name in self.components else {}

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

    def evaluate(self):
        is_comp = True
        for n in ANALYSIS_COMPONENTS:
            if n in self.components:
                temp = reduce(lambda a, b: a and b, [self.components[n][c].evaluate() for c in self.components[n]])
                is_comp = is_comp and temp
                if not is_comp:
                    break
        return is_comp and reduce(lambda a, b: a and b, map(lambda a: a.is_matching, self.fields), True)


class SchemaAnalysis(GenericAnalysis):
    def __init__(self, name: str):
        super().__init__(name)
        self.properties: list[SchemaAnalysis] = []
        self.items: Optional[SchemaAnalysis] = None

    def evaluate(self) -> bool:
        prop_ok: bool = reduce(lambda a, b: a and b, map(lambda a: a.evaluate(), self.properties), True)
        self.is_ok = prop_ok and super().evaluate() and eval_analysis_obj(self.items)
        if self.is_ok is None:
            raise Exception('Avaliação de Schema não deve ser None')
        return self.is_ok


class ParameterAnalysis(GenericAnalysis):
    def __init__(self, name: str):
        super().__init__(name)
        self.schema: Optional[SchemaAnalysis] = None
        self.content: list[MediaTypeAnalysis] = []

    def evaluate(self):
        is_content = reduce(lambda a, b: a and b, map(lambda d: d.evaluate(), self.content), True)
        self.is_ok = is_content and super().evaluate() and eval_analysis_obj(self.schema)
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
        self.is_ok = is_encoding and super().evaluate() and eval_analysis_obj(self.schema)
        if self.is_ok is None:
            raise Exception('Avaliação de Schema não deve ser None')
        return self.is_ok


class EncodingAnalysis(GenericAnalysis):
    def __init__(self, name: str):
        super().__init__(name)
        self.headers: list[HeaderAnalysis] = []

    def evaluate(self):
        is_headers = reduce(lambda a, b: a and b, map(lambda d: d.evaluate(), self.headers), True)
        self.is_ok = is_headers and super().evaluate()
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
        self.is_ok = is_content and super().evaluate()
        if self.is_ok is None:
            raise Exception('Avaliação de Schema não deve ser None')
        return self.is_ok


class ResponsesAnalysis(GenericAnalysis):
    def __init__(self, name: str):
        super().__init__(name)
        self.default: Optional[ResponseAnalysis] = None
        self.responses: list[ResponseAnalysis] = []

    def evaluate(self):
        is_response = reduce(lambda a, b: a and b, map(lambda d: d.evaluate(), self.responses), True)
        self.is_ok = is_response and super().evaluate() and eval_analysis_obj(self.default)
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
        self.is_ok = is_content and is_headers and super().evaluate()
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
        self.is_ok = is_parameters and super().evaluate() and eval_analysis_obj(self.responses) and eval_analysis_obj(
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
        self.is_ok = is_parameters and is_op and super().evaluate()
        if self.is_ok is None:
            raise Exception('Avaliação de Schema não deve ser None')
        return self.is_ok


class PathsAnalysis(GenericAnalysis):
    def __init__(self, name: str):
        super().__init__(name)
        self.path_items: list[PathItemAnalysis] = []

    def evaluate(self):
        is_path_items = reduce(lambda a, b: a and b, map(lambda d: d.evaluate(), self.path_items), True)
        self.is_ok = is_path_items and super().evaluate()
        if self.is_ok is None:
            raise Exception('Avaliação de Schema não deve ser None')
        return self.is_ok
