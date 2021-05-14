import os

ROOT_DIR = os.path.dirname(os.path.abspath(__file__))  # This is your Project Root

ANALYSIS_COMPONENTS = ['schemas', 'responses', 'parameters', 'requestBodies', 'headers']
ANALYSIS_SCHEMA_FIELDS = ['required', 'type', 'enum', 'format', 'minimum', 'maximum', 'exclusiveMinimum',
                          'exclusiveMaximum', 'minLength', 'maxLength', 'pattern', 'minProperties',
                          'maxProperties', 'minItems', 'maxItems', 'default']
ANALYSIS_PARAMETERS_FIELDS = ['name', 'in', 'required', 'deprecated', 'allowEmptyValue', 'allowReserved']
ANALYSIS_HTTP_REQ_METHODS = ['get', 'put', 'post', 'delete', 'options', 'head', 'patch', 'trace']
