# dass-assignment-2

cd black-box
pytest test_quickcart.py -v


cd ../integration
pytest test_integration.py -v


cd ../whitebox
# Basic test run:
pytest tests/test_white_box.py -v

# Run with a code coverage report for the moneypoly package:
pytest tests/test_white_box.py -v --cov=moneypoly --cov-report=term-report=term-missing