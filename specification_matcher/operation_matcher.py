from basic_operations.comparison_operations import add_field_comparison
from spec_metadata.analysis_metadata import OperationAnalysis
from spec_metadata.component_metadata import ComponentMetadata
from specification_matcher.parameter_matcher import match_parameters
from specification_matcher.request_body_matcher import match_request_body
from specification_matcher.responses_matcher import match_responses


def match_operation(components: dict[str, ComponentMetadata], spec_name: str, base_spec: dict,
                    target_spec: dict) -> OperationAnalysis:
    analysis = OperationAnalysis(spec_name)
    add_field_comparison(analysis, 'deprecated', base_spec, target_spec)
    analysis.parameters = match_parameters(components, base_spec, target_spec, analysis)

    add_field_comparison(analysis, 'requestBody', base_spec, target_spec, lambda a: 'Campo "requestBody"')
    if 'requestBody' in base_spec and 'requestBody' in target_spec:
        analysis.request_body = match_request_body(components, spec_name, base_spec['requestBody'],
                                                   target_spec['requestBody'])

    add_field_comparison(analysis, 'responses', base_spec, target_spec, lambda a: list(a.keys()))
    if 'responses' in base_spec and 'responses' in target_spec:
        analysis.responses = match_responses(components, spec_name, base_spec['responses'], target_spec['responses'])
    return analysis
