import copy
from typing import Optional, Callable, Any

from spec_metadata.analysis_metadata import AttributeMatchingData


def compare_attributes(attr_list: list[str], base_spec: dict, target_spec: dict) -> list[AttributeMatchingData]:
    comparison_list = list()
    for attr_name in base_spec:
        if attr_name in attr_list:
            result = compare_simple_attribute(attr_name, base_spec, target_spec)
            if result is not None:
                comparison_list.append(result)
    return comparison_list


def _extract_value(attr_name: str, source_object) -> Optional[Any]:
    return source_object[attr_name] if attr_name in source_object else None


def compare_simple_attribute(attr_name, base_spec: dict, target_spec: dict,
                             value_extractor: Callable[[Any, Any], Any] = _extract_value
                             ) -> Optional[AttributeMatchingData]:
    result = AttributeMatchingData(attr_name)
    if attr_name in base_spec and attr_name in target_spec:
        expected = copy.deepcopy(value_extractor(attr_name, base_spec))
        current = copy.deepcopy(value_extractor(attr_name, target_spec))
        result.set_values(expected, current)
        if expected == current:
            result.reason = 'Atributo validado'
            result.is_matching = True
        else:
            result.reason = f'Atributo possui valor diferente do esperado'
            result.is_matching = False
    elif attr_name in base_spec:
        expected = copy.deepcopy(value_extractor(attr_name, base_spec))
        result.reason = 'Atributo esperado não encontrado'
        result.is_matching = False
        result.set_values(expected, None)
    elif attr_name in target_spec:
        current = copy.deepcopy(value_extractor(attr_name, target_spec))
        result.reason = 'Atributo não está definido na especificação'
        result.is_matching = False
        result.set_values(None, current)
    else:
        return None
    return result
