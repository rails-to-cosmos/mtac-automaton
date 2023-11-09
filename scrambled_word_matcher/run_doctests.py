import doctest
import unittest
import os
from types import ModuleType
from typing import Iterable, Tuple, List

MODULE_NAME = 'scrambled_word_matcher'

def load_tests(loader: unittest.TestLoader, tests: unittest.TestSuite, ignore: str) -> unittest.TestSuite:
    for root, dirs, files in os.walk(MODULE_NAME):
        for f in files:
            if f.endswith('.py'):
                modname = MODULE_NAME + '.' + f[:-3]
                if modname.endswith('.__init__'):
                    modname = modname[:-9]
                modname = modname.replace(os.path.sep, '.')
                try:
                    module = __import__(modname, fromlist=[''])
                except ImportError as e:
                    ...  # Skip non-modules
                else:
                    tests.addTests(doctest.DocTestSuite(module))
    return tests

if __name__ == "__main__":
    unittest.main()
