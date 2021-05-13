import copy
from typing import Optional, Callable, Any

from spec_metadata.analysis_metadata import FieldMatchingData


def compare_fields(attr_list: list[str], base_spec: dict, target_spec: dict) -> list[FieldMatchingData]:
    comparison_list = list()
    for attr_name in base_spec:
        if attr_name in attr_list:
            result = compare_simple_field(attr_name, base_spec, target_spec)
            if result is not None:
                comparison_list.append(result)
    return comparison_list


def _extract_value(attr_name: str, source_object) -> Optional[Any]:
    return source_object[attr_name] if attr_name in source_object else None


def _is_equal(obj_a, obj_b):
    if isinstance(obj_a, list):
        if len(obj_a) != len(obj_b):
            return False
        if set(obj_a) == set(obj_b):
            return True
        else:
            return False
    else:
        return obj_a == obj_b


def compare_simple_field(field_name, base_spec: dict, target_spec: dict,
                         value_extractor: Callable[[Any, Any], Any] = _extract_value
                         ) -> Optional[FieldMatchingData]:
    result = FieldMatchingData(field_name)
    if field_name in base_spec and field_name in target_spec:
        expected = copy.deepcopy(value_extractor(field_name, base_spec))
        current = copy.deepcopy(value_extractor(field_name, target_spec))
        result.set_values(expected, current)
        if _is_equal(expected, current):
            result.reason = 'Atributo validado'
            result.is_matching = True
        else:
            result.reason = f'Atributo possui valor diferente do esperado'
            result.is_matching = False
    elif field_name in base_spec:
        expected = copy.deepcopy(value_extractor(field_name, base_spec))
        result.reason = 'Atributo esperado não encontrado'
        result.is_matching = False
        result.set_values(expected, None)
    elif field_name in target_spec:
        current = copy.deepcopy(value_extractor(field_name, target_spec))
        result.reason = 'Atributo não está definido na especificação'
        result.is_matching = False
        result.set_values(None, current)
    else:
        return None
    return result
