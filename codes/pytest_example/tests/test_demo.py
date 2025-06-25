import pytest
import allure
import requests
from jsonpath_ng.ext import parse

from utils import load_test_case, validate_response

@allure.title("demo")
@pytest.mark.api
@pytest.mark.parametrize("send, validate, extract", load_test_case())
def test_demo(send, validate, extract):
    """
    Test case for API requests.
    
    :param send: The request data for the API call.
    :param validate: The validation rules for the response.
    :param extract: The extraction rules for the response.
    """
    
    # step 1: send the request
    url = send.get("url")
    method = send.get("method")
    headers = send.get("headers", {})
    body = send.get("body", {})
    
    response = requests.request(method=method, url=url, headers=headers, json=body)

    # step 2: validate the response
    val_result = validate_response(response, validate)
    assert val_result is None
    
    # step 3: extract data if needed
    if extract:
        for key, expr in extract.items():
            jsonpath_expr = parse(expr)
            matches = jsonpath_expr.find(response.json())
            if matches:
                extracted_value = matches[0].value
                allure.attach(name=key, body=str(extracted_value), attachment_type=allure.attachment_type.TEXT)
            else:
                allure.attach(name=key, body="No match found", attachment_type=allure.attachment_type.TEXT)