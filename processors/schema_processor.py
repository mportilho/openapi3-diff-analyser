from openapi3_structs import schema

def process(openapi):
    schemas_source = openapi['components']['schemas']
    for schema_key in schemas_source:
        _process_schema(schema_key, schemas_source)


def _process_schema(schema_key, schemas_source):

    print(schemas_source[schema_key])
