#! usr/bin/env python3.7
"""
Tests for the graphql_client library
"""

from datetime import datetime
from typing import List

from pydantic import BaseModel

from gqlclient import GraphQLClient


# Graphql Client to test
test_client = GraphQLClient(gql_uri="http://localhost:5000/graphql")


# Test input parameter definition
class ParametersTest(BaseModel):
    str_param: str
    int_param: int
    float_param: float
    str_array_param: List[str]
    str_num_param: List[int]
    date_param: datetime
    optional_param: int = None


# Test response model(s)
class ResponseChildTest(BaseModel):
    child_param_1: str
    child_param_2: str


class ResponseParentTest(BaseModel):
    parent_param_1: str
    parent_param_2: str
    child_object: ResponseChildTest


test_query_base = "query_base"
test_mutation_base = "mutation_base"
test_parameters = ParametersTest(
    str_param="A",
    int_param=1,
    float_param=1.1,
    str_array_param=["A", "B"],
    str_num_param=[1, 2],
    date_param="2010-03-25T14:08:00.000000",
)


def test_query_string_with_parameters():
    """
    Test of query string structure when parameter model is included
    :return: None
    """
    test_query = test_client.get_query(
        query_base=test_query_base,
        query_parameters=test_parameters,
        query_response_cls=ResponseParentTest,
    )
    expected_result = {
        "query": '{query_base(str_param: "A", '
        "int_param: 1, "
        "float_param: 1.1, "
        'str_array_param: ["A", "B"], '
        "str_num_param: [1, 2], "
        'date_param: "2010-03-25T14:08:00")'
        "{parent_param_1, parent_param_2, "
        "child_object { child_param_1 child_param_2 }"
        "} }"
    }
    assert test_query == expected_result


def test_query_string_without_parameters():
    """
    Test of query string structure when parameter model is NOT included
    :return: None
    """
    test_query = test_client.get_query(
        query_base=test_query_base, query_response_cls=ResponseParentTest
    )
    expected_result = {
        "query": "{query_base"
        "{parent_param_1, parent_param_2, "
        "child_object { child_param_1 child_param_2 }"
        "} }"
    }

    assert test_query == expected_result


def test_mutation_string_with_response():
    """
    Test of mutation string structure when response model is included
    :return: None
    """
    test_mutation = test_client.get_mutation(
        mutation_base=test_mutation_base,
        mutation_response_cls=ResponseParentTest,
        mutation_parameters=test_parameters,
    )
    expected_result = {
        "query": "mutation mutation_base "
        "{mutation_base("
        'str_param: "A", '
        "int_param: 1, "
        "float_param: 1.1, "
        'str_array_param: ["A", "B"], '
        "str_num_param: [1, 2], "
        'date_param: "2010-03-25T14:08:00")'
        "{ok, "
        "parent_param_1, parent_param_2, "
        "child_object { child_param_1 child_param_2 }"
        "} }",
        "operationName": "mutation_base",
    }
    assert test_mutation == expected_result


def test_mutation_string_without_response():
    """
    Test of mutation string structure when response model is NOT included
    :return: None
    """
    test_mutation = test_client.get_mutation(
        mutation_base=test_mutation_base, mutation_parameters=test_parameters
    )
    print(test_mutation)
    expected_result = {
        "query": "mutation mutation_base "
        "{mutation_base("
        'str_param: "A", '
        "int_param: 1, "
        "float_param: 1.1, "
        'str_array_param: ["A", "B"], '
        "str_num_param: [1, 2], "
        'date_param: "2010-03-25T14:08:00")'
        "{ok"
        "} }",
        "operationName": "mutation_base",
    }
    print(expected_result)
    assert test_mutation == expected_result
