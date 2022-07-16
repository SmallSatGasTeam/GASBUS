
import unittest

from testing import testManager

suite = unittest.TestSuite()
tests = [testManager.testManager]
for test in tests:
    suite.addTest(unittest.makeSuite(test))

runner = unittest.TextTestRunner(verbosity=2)
runner.run(suite)