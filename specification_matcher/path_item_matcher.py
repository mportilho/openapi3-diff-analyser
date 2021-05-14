from basic_operations.comparison_operations import add_field_comparison
from definitions import ANALYSIS_HTTP_REQ_METHODS
from spec_metadata.analysis_metadata import PathItemAnalysis
from spec_metadata.component_metadata import ComponentMetadata
from specification_matcher.operation_matcher import match_operation
from specification_matcher.parameter_matcher import match_parameter


def match_path_item(components: dict[str, ComponentMetadata], spec_name: str, base_spec: dict,
                    target_spec: dict) -> PathItemAnalysis:
    if '$ref' in base_spec or '$ref' in target_spec:
        if '$ref' in base_spec and '$ref' in target_spec:
            analysis = PathItemAnalysis(spec_name)
            add_field_comparison(analysis, '$ref', base_spec, target_spec)
            return analysis
        elif '$ref' in base_spec:
            comp_obj = components['base'].get_component_by_ref(base_spec['$ref'])
            name = spec_name + f".$ref[{comp_obj.name}]"
            return match_path_item(components, name, comp_obj.get_spec(), target_spec)
        elif '$ref' in target_spec:
            comp_obj = components['target'].get_component_by_ref(target_spec['$ref'])
            name = spec_name + f".$ref[{comp_obj.name}]"
            return match_path_item(components, name, base_spec, comp_obj.get_spec())

    analysis = PathItemAnalysis(spec_name)

    for http_method in ANALYSIS_HTTP_REQ_METHODS:
        if http_method in base_spec:
            if http_method in target_spec:
                analysis.operations[http_method] = match_operation(components, f"op[{http_method}]", base_spec,
                                                                   target_spec)
            else:
                add_field_comparison(analysis, http_method, base_spec, target_spec, lambda a: f"Campo '{http_method}'")

    add_field_comparison(analysis, 'parameters', base_spec, target_spec, lambda a: map(lambda l: l['name'], a))
    if 'parameters' in base_spec and 'parameters' in target_spec:
        for p_name in map(lambda l: l['name'], base_spec):
            target_param = next(filter(lambda tp: tp['name'] == p_name, target_spec['parameters']), None)
            if target_param is not None:
                match_parameter(components, f"par[{p_name}]", base_spec[p_name], target_spec[p_name])
    return analysis
