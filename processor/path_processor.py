from definitions import METADATA_OBJ
from structures.schema_analysis import PathMetadata


def _create_metadata(schema: dict, name: str):
    if METADATA_OBJ not in schema:
        print()


def process(openapi: dict):
    paths = openapi['paths']
    for path_name in paths:
        _process_path(path_name, paths[path_name])


def _process_path(path_name: str, path: dict):
    metadata = PathMetadata(path_name)
    if '$ref' in path:
        print()

    http_verbs = ['get', 'put', 'post', 'delete', 'options', 'head', 'patch', 'trace']

    for method_name in path:
        print()
