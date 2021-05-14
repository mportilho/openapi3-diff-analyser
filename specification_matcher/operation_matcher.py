from basic_operations.comparison_operations import add_field_comparison
from spec_metadata.analysis_metadata import OperationAnalysis
from spec_metadata.component_metadata import ComponentMetadata
from specification_matcher.parameter_matcher import match_parameter
from specification_matcher.request_body_matcher import match_request_body
from specification_matcher.responses_matcher import match_responses


def match_operation(components: dict[str, ComponentMetadata], spec_name: str, base_spec: dict,
                    target_spec: dict) -> OperationAnalysis:
    analysis = OperationAnalysis(spec_name)
    add_field_comparison(analysis, 'deprecated', base_spec, target_spec)

    add_field_comparison(analysis, 'parameters', base_spec, target_spec, lambda a: map(lambda l: l['name'], a))
    if 'parameters' in base_spec and 'parameters' in target_spec:
        for p_name in map(lambda l: l['name'], base_spec):
            target_param = next(filter(lambda tp: tp['name'] == p_name, target_spec['parameters']), None)
            if target_param is not None:
                analysis.parameters.append(
                    match_parameter(components, f"par[{p_name}]", base_spec[p_name], target_spec[p_name]))

    add_field_comparison(analysis, 'requestBody', base_spec, target_spec, lambda a: 'Campo "requestBody"')
    if 'requestBody' in base_spec and 'requestBody' in target_spec:
        analysis.request_body = match_request_body(components, f"rb[{spec_name}]", base_spec['requestBody'],
                                                   target_spec['requestBody'])

    add_field_comparison(analysis, 'responses', base_spec, target_spec, lambda a: 'Campo "responses"')
    if 'responses' in base_spec and 'responses' in target_spec:
        analysis.responses = match_responses(components, f"rps[{spec_name}]", base_spec['responses'],
                                             target_spec['responses'])
    return analysis
