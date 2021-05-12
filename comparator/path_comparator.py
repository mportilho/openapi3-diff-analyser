from processor import path_processor
from structures.comparison_result import ComparisonResult
from structures.schema_analysis import PathResultMetadata
from structures.schema_comparison import PathComparison


# def _create_result_metadata(schema: dict) -> SchemaResultMetadata:
#     if METADATA_RESULT not in schema:
#         schema[METADATA_RESULT] = SchemaResultMetadata(schema[METADATA_OBJ].name)
#     return schema[METADATA_RESULT]


def compare_paths(source_path_spec, target_path_spec):
    source_path_spec: dict = path_processor.process(source_path_spec)
    target_path_spec: dict = path_processor.process(target_path_spec)
    path_comparison = PathComparison(source_path_spec, target_path_spec)
    path_comparison.analyse()

    for name in source_path_spec:
        if name in target_path_spec:
            _compare_path(path_comparison, name, source_path_spec[name], target_path_spec[name])
        else:
            print()

    # for name in schema_comparison.source:
    #     if name in schema_comparison.target:
    #         _compare_schemas(schema_comparison, schema_comparison.result[name], schema_comparison.target[name])
    #     else:
    #         schema: dict = schema_comparison.result[name]
    #         result_metadata = _create_result_metadata(schema)
    #         result_metadata.analysed = True
    #         result_metadata.valid = False
    #         result_metadata.is_present = False


def _compare_path(path_comparison: PathComparison, source_path, target_path):
    print()


def _compare_responses(path_comparison: PathComparison, name: str, source_path: dict, target_path: dict):
    result_response: dict = {}
    result_metadata = PathResultMetadata(name)
    if 'responses' in source_path and 'responses' in target_path:
        for response_code in source_path['responses']:
            result_r_code = ComparisonResult(response_code)
            if response_code in target_path['responses']:
                result_r_code.equivalent = True
                result_r_code.reason = f"Response {response_code} presente"
                source_response: dict = source_path['responses'][response_code]
                target_response: dict = target_path['responses'][response_code]
                if 'content' in source_response and 'content' in target_response:
                    for content_type_name in source_response:
                        if content_type_name in target_response:
                            print()
                        else:
                            print('target não contem content_type_name')
                elif 'content' in source_response:
                    print('target nao contem attr content')
            else:
                result_r_code.reason = f"A spec alvo não possui response {response_code}"
                result_r_code.equivalent = False
            result_metadata.responses[response_code] = result_r_code
    elif 'responses' in source_path:
        print('sem attr responses no target')

    for response_code in source_path['responses']:
        if response_code in target_path['responses']:
            content = source_path['responses'][response_code]['content']
            print()
        else:
            print()
        response = {}
        # result_metadata.responses[response_code]
        print()


def _compare_path_item(source_path_item: dict, target_path_item: dict):
    if '$ref' in source_path_item:
        print()
    operations = ['get', 'put', 'post', 'delete', 'options', 'head', 'patch', 'trace']
    for operation_name in operations:
        _compare_operation(operations[operation_name])


def _compare_operation(source_operation: dict, target_operation: dict):
    print()


def _compare_parameters(element_name: str, source_parameter: dict, target_parameter: dict):
    print()


def _compare_request_body(a: dict, b: dict):
    print()


def _compare_response(a: dict, b: dict):
    print()
