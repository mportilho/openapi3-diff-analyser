from spec_matcher import matching_operations
from spec_metadata.component_metadata import ComponentMetadata


def match_specs(component_metadata: ComponentMetadata, base_spec: dict, target_spec: dict):
    attr_list = ['name', 'in', 'required', 'allowEmptyValue']
    attr_matching_data = matching_operations.compare_attributes(attr_list, base_spec, target_spec)

    print()
