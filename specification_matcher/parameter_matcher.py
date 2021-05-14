from basic_operations.comparison_operations import compare_fields, add_field_comparison
from definitions import ANALYSIS_PARAMETERS_FIELDS
from spec_metadata.analysis_metadata import ParameterAnalysis, GenericAnalysis
from spec_metadata.component_metadata import ComponentMetadata
from specification_matcher import schema_matcher, media_type_matcher


def match_parameters(components: dict[str, ComponentMetadata], base_spec: dict,
                     target_spec: dict, analysis: GenericAnalysis = None) -> list[ParameterAnalysis]:
    base_params = {}
    target_params = {}
    params_analysis_map: list[ParameterAnalysis] = []
    if 'parameters' in base_spec or 'parameters' in target_spec:
        if 'parameters' in base_spec:
            for params in base_spec['parameters']:
                if '$ref' in params:
                    pmo = components['base'].get_component_by_ref(params['$ref'])
                    p_spec = pmo.get_spec()
                    base_params[p_spec['name']] = p_spec
                else:
                    base_params[params['name']] = params
        if 'parameters' in target_spec:
            for params in target_spec['parameters']:
                if '$ref' in params:
                    pmo = components['base'].get_component_by_ref(params['$ref'])
                    p_spec = pmo.get_spec()
                    target_params[p_spec['name']] = p_spec
                else:
                    target_params[params['name']] = params

        for p_name in base_params:
            if p_name in target_params:
                params_analysis_map.append(match_parameter(components, f"par[{p_name}]", base_params[p_name],
                                                           target_params[p_name]))
    if analysis is not None and (base_params or target_params):
        add_field_comparison(analysis, 'parameters', {'parameters': base_params}, {'parameters': target_params},
                             lambda a: list(a.keys()))
    return params_analysis_map


def match_parameter(components: dict[str, ComponentMetadata], spec_name: str, base_spec: dict,
                    target_spec: dict) -> ParameterAnalysis:
    analysis = ParameterAnalysis(spec_name)
    analysis.fields = compare_fields(ANALYSIS_PARAMETERS_FIELDS, base_spec, target_spec)

    add_field_comparison(analysis, 'schema', base_spec, target_spec, lambda a: 'Objeto Schema')
    if 'schema' in base_spec and 'schema' in target_spec:
        analysis.schema = schema_matcher.match_schema(components, f"scm[{spec_name}]", base_spec['schema'],
                                                      target_spec['schema'])

    add_field_comparison(analysis, 'content', base_spec, target_spec, lambda a: list(a.keys()))
    if 'content' in base_spec and 'content' in target_spec:
        for c_name, c_value in base_spec.items():
            if c_name in target_spec['content']:
                analysis.content.append(
                    media_type_matcher.match_media_type(components, f"cnt[{c_name}]", base_spec['content'][c_name],
                                                        target_spec['content'][c_name]))
    return analysis
