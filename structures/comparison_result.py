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
            self._source = {'value': source}

    def set_target(self, target):
        if isinstance(target, dict):
            self._target = target
        else:
            self._target = {'value': target}

    def get_source(self):
        return self._source

    def get_target(self):
        return self._target

    def __str__(self):
        return f'Result of "{self.attr_name}": {self.equivalent} - Reason: {self.reason}'
