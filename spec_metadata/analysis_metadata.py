from typing import Optional

from spec_matcher.matchers_structure import AttributeMatchingData


class SchemaAnalysis(object):
    def __init__(self, name: str, attributes: list[AttributeMatchingData]):
        self.name: str = name
        self.attributes: list[AttributeMatchingData] = attributes
        self.properties: list[SchemaAnalysis] = list()
        self.items: Optional[SchemaAnalysis] = None
