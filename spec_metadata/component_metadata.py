import copy
import re
from typing import Optional

from definitions import ANALYSIS_COMPONENTS

regex_ref = r'^#\/components\/([\w]+)\/([\w]+)'


class ComponentMetadataObject(object):
    def __init__(self, name: str, spec: dict):
        self.name: str = name
        self._spec: dict = spec

    def get_spec(self):
        return copy.deepcopy(self._spec)


class ComponentMetadata(object):
    def __init__(self):
        self._components: dict = {}

    def add_component_spec(self, component_type_name: str, component_specs: dict):
        self._components[component_type_name] = component_specs

    def get_component_by_ref(self, ref: str) -> Optional[ComponentMetadataObject]:
        groups = re.search(regex_ref, ref).groups()
        if groups[0] in self._components and groups[1] in self._components[groups[0]]:
            return self._components[groups[0]][groups[1]]
        return None


def analyse_components(openapi_spec: dict) -> ComponentMetadata:
    component_metadata = ComponentMetadata()
    if 'components' not in openapi_spec:
        return component_metadata
    for component_type_name in ANALYSIS_COMPONENTS:
        if component_type_name in openapi_spec['components']:
            obj_meta = _analyse_component_object(openapi_spec['components'][component_type_name])
            component_metadata.add_component_spec(component_type_name, obj_meta)
    return component_metadata


def _analyse_component_object(components_spec: dict) -> dict:
    object_metadata = {}
    for obj_name in components_spec:
        object_metadata[obj_name] = ComponentMetadataObject(obj_name, copy.deepcopy(components_spec[obj_name]))
    return object_metadata
