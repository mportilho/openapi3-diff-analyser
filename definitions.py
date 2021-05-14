import os

ROOT_DIR = os.path.dirname(os.path.abspath(__file__))  # This is your Project Root

ANALYSIS_SCHEMA_FIELDS = ['required', 'type', 'enum', 'format', 'minimum', 'maximum', 'exclusiveMinimum',
                          'exclusiveMaximum', 'minLength', 'maxLength', 'pattern', 'minProperties',
                          'maxProperties', 'minItems', 'maxItems', 'default']
ANALYSIS_PARAMETERS_FIELDS = ['name', 'in', 'required', 'deprecated', 'allowEmptyValue', 'allowReserved']
ANALYSIS_MEDIA_TYPE_FIELDS = []
