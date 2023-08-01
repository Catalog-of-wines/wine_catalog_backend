# code from file wine/app/product/test_queye.py
import unittest
from app.product.test_product import TestProductEndpoints

# List all the test classes here in the desired order of execution
test_classes = [TestProductEndpoints]

# Test suite to hold the tests
test_suite = unittest.TestSuite()

# Add test cases from test classes to the suite
for test_class in test_classes:
    test_suite.addTest(unittest.makeSuite(test_class))


def run_tests_sequentially():
    runner = unittest.TextTestRunner()
    result = runner.run(test_suite)
    return result


if __name__ == "__main__":
    run_tests_sequentially()

# the end of code from file wine/app/product/test_queye.py