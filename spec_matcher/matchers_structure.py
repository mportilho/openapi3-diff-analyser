class AttributeMatchingData(object):
    def __init__(self, attribute_name: str):
        self.attribute_name: str = attribute_name
        self._expected_value = None
        self._current_value = None
        self.is_matching: bool = False
        self.reason: str = ''

    def set_values(self, expected_value, current_value):
        self._expected_value = expected_value
        self._current_value = current_value

    def get_expected_value(self):
        return self._expected_value

    def get_current_value(self):
        return self._current_value


class SchemaMatchingData(object):
    def __init__(self):
        print()
