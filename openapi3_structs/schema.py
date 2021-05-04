class Schema(dict):
    def __init__(self, *args, **kwargs):
        self['schema_name'] = None
        # self.multipleOf
        # self.uniqueItems
