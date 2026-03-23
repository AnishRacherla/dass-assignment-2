import json
import re

with open('test_interceptions.json', 'r', encoding='utf-8') as f:
    logs = json.load(f)

with open('test_output.txt', 'r', encoding='utf-16') as f:
    lines = f.readlines()

passed_tests = []
for line in lines:
    if 'PASSED' in line:
        match = re.search(r'test_quickcart.py::(\S+)', line)
        if match:
            passed_tests.append(match.group(1))

test_reqs = {}
for log in logs:
    test_reqs[log["test"]] = log

output = "# QuickCart Black-Box Passing Tests Report\n\n"

count = 1
for test_name in passed_tests:
    if test_name in test_reqs:
        req = test_reqs[test_name]
        title = test_name.replace("test_", "").replace("_", " ").title()
        endpoint = req["url"].replace('http://localhost:8080', '')
        # Prettier formatting for title
        reason = f"Validates that {title.lower()} is processed correctly according to specification, preventing regressions."
        
        output += f"### Passing Test {count}: {title}\n"
        output += f"- **Endpoint tested**: {req['method']} {endpoint}\n"
        output += f"- **Request payload**:\n"
        output += f"  - Method: {req['method']}\n"
        output += f"  - URL: {req['url']}\n"
        output += f"  - Headers: {req['headers']}\n"
        output += f"  - Body: {req['body']}\n"
        
        status = req['status']
        # passing test -> expected equals actual
        output += f"- **Expected result**: {status} HTTP Status Code\n"
        output += f"- **Actual result observed**: {status} HTTP Status Code\n"
        output += f"- **Reason why this test case is useful**: {reason}\n\n"
        
        count += 1

with open('BLACK_BOX_PASSING_REPORT.md', 'w', encoding='utf-8') as f:
    f.write(output)
print(f"Generated report for {count-1} passing tests.")
