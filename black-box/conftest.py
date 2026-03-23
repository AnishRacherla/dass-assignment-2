import pytest
import requests
import json
import logging

logs = []

original_request = requests.request
original_get = requests.get
original_post = requests.post
original_put = requests.put
original_delete = requests.delete
original_patch = requests.patch

current_test_name = None

def pytest_runtest_setup(item):
    global current_test_name
    current_test_name = item.name

def monkey_get(*args, **kwargs):
    req_args = args
    req_kwargs = kwargs
    res = original_get(*args, **kwargs)
    logs.append({"test": current_test_name, "method": "GET", "url": args[0], "headers": kwargs.get('headers'), "body": kwargs.get('json') or kwargs.get('data'), "status": res.status_code})
    return res

def monkey_post(*args, **kwargs):
    res = original_post(*args, **kwargs)
    logs.append({"test": current_test_name, "method": "POST", "url": args[0], "headers": kwargs.get('headers'), "body": kwargs.get('json') or kwargs.get('data'), "status": res.status_code})
    return res

def monkey_put(*args, **kwargs):
    res = original_put(*args, **kwargs)
    logs.append({"test": current_test_name, "method": "PUT", "url": args[0], "headers": kwargs.get('headers'), "body": kwargs.get('json') or kwargs.get('data'), "status": res.status_code})
    return res

def monkey_delete(*args, **kwargs):
    res = original_delete(*args, **kwargs)
    logs.append({"test": current_test_name, "method": "DELETE", "url": args[0], "headers": kwargs.get('headers'), "body": kwargs.get('json') or kwargs.get('data'), "status": res.status_code})
    return res

def monkey_patch(*args, **kwargs):
    res = original_patch(*args, **kwargs)
    logs.append({"test": current_test_name, "method": "PATCH", "url": args[0], "headers": kwargs.get('headers'), "body": kwargs.get('json') or kwargs.get('data'), "status": res.status_code})
    return res

requests.get = monkey_get
requests.post = monkey_post
requests.put = monkey_put
requests.delete = monkey_delete
requests.patch = monkey_patch

def pytest_sessionfinish(session, exitstatus):
    with open('test_interceptions.json', 'w') as f:
        json.dump(logs, f)
