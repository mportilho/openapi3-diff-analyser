from app.basic_operations.comparison_operations import add_field_comparison
from definitions import ANALYSIS_COMPONENTS
from app.spec_metadata.analysis_metadata import ComponentsAnalysis
from app.spec_metadata.component_metadata import analyse_components
from app.specification_matcher.header_matcher import match_header
from app.specification_matcher.parameter_matcher import match_parameter
from app.specification_matcher.request_body_matcher import match_request_body
from app.specification_matcher.responses_matcher import match_responses
from app.specification_matcher.schema_matcher import match_schema


def match_components(base_api_spec: dict, target_api_spec: dict) -> ComponentsAnalysis:
    analysis = ComponentsAnalysis('components')
    analysis.components_metadata = {'base': analyse_components(base_api_spec),
                                    'target': analyse_components(target_api_spec)}
    add_field_comparison(analysis, 'components', base_api_spec, target_api_spec, lambda a: list(a.keys()))

    if 'components' in base_api_spec and 'components' in target_api_spec:
        base_components = base_api_spec['components']
        target_components = target_api_spec['components']
        for comp_name in ANALYSIS_COMPONENTS:
            add_field_comparison(analysis, comp_name, base_components, target_components,
                                 lambda a: list(a.keys()))
            if comp_name in base_components and comp_name in target_components:
                for comp_item_name in [c_name for c_name in base_components[comp_name] if
                                       c_name in target_components[comp_name]]:
                    component_analysis = None
                    if 'schemas' == comp_name:
                        component_analysis = match_schema(analysis.components_metadata, comp_item_name,
                                                          base_components[comp_name][comp_item_name],
                                                          target_components[comp_name][comp_item_name])
                    elif 'responses' == comp_name:
                        component_analysis = match_responses(analysis.components_metadata, comp_item_name,
                                                             base_components[comp_name][comp_item_name],
                                                             target_components[comp_name][comp_item_name])
                    elif 'parameters' == comp_name:
                        component_analysis = match_parameter(analysis.components_metadata, comp_item_name,
                                                             base_components[comp_name][comp_item_name],
                                                             target_components[comp_name][comp_item_name])
                    elif 'requestBodies' == comp_name:
                        component_analysis = match_request_body(analysis.components_metadata, comp_item_name,
                                                                base_components[comp_name][comp_item_name],
                                                                target_components[comp_name][comp_item_name])
                    elif 'headers' == comp_name:
                        component_analysis = match_header(analysis.components_metadata, comp_item_name,
                                                          base_components[comp_name][comp_item_name],
                                                          target_components[comp_name][comp_item_name])
                    if component_analysis is not None:
                        analysis.set_component(comp_name, comp_item_name, component_analysis)
    return analysis
