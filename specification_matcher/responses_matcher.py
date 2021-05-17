from basic_operations import comparison_operations as comp
from spec_metadata.analysis_metadata import ResponsesAnalysis, FieldMatchingData
from spec_metadata.component_metadata import ComponentMetadata
from specification_matcher.response_matcher import match_response


def match_responses(components: dict[str, ComponentMetadata], spec_name: str, base_spec: dict,
                    target_spec: dict) -> ResponsesAnalysis:
    analysis = ResponsesAnalysis(spec_name)
    comp.add_field_comparison(analysis, 'default', base_spec, target_spec, lambda a: 'Campo "default"')
    if 'default' in base_spec and 'default' in target_spec:
        analysis.default = match_response(components, 'default', base_spec['default'], target_spec['target'])

    field_comp = FieldMatchingData('httpResponses')
    base_codes = [code for code in base_spec if str(code).isnumeric()]
    target_codes = [code for code in target_spec if str(code).isnumeric()]
    field_comp.set_values(base_codes, target_codes)
    if comp.is_equal(base_codes, target_codes):
        field_comp.is_matching = True
        field_comp.reason = 'Responses possuem mesmos http status code'
    else:
        field_comp.is_matching = False
        field_comp.reason = 'Responses possuem diferentes http status code'
    for http_code in [code for code in base_codes if code in target_spec]:
        analysis.responses.append(
            match_response(components, f"rps[{http_code}]", base_spec[http_code], target_spec[http_code]))
    analysis.fields.append(field_comp)
    return analysis
