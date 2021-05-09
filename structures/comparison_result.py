VALUE_ATTR = '_value_'


class ComparisonResult(object):

    def __init__(self, attribute_name: str):
        self.attr_name: str = attribute_name
        self.equivalent: bool = False
        self.reason: str = ''
        self._source: dict = {}
        self._target: dict = {}

    def set_source(self, source):
        if isinstance(source, dict):
            self._source = source
        else:
            self._source = {VALUE_ATTR: source}

    def set_target(self, target):
        if isinstance(target, dict):
            self._target = target
        else:
            self._target = {VALUE_ATTR: target}

    def get_source(self):
        return self._source[VALUE_ATTR] if VALUE_ATTR in self._source else self._source

    def get_target(self):
        return self._target[VALUE_ATTR] if VALUE_ATTR in self._target else self._target

    def __str__(self):
        return f'Result of "{self.attr_name}": {self.equivalent} - Reason: {self.reason}'
