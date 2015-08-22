import doctest
import pkgutil

import gt

def load_tests(loader, tests, ignore): # pylint: disable=unused-argument
    for _, module, _ in pkgutil.iter_modules(gt.__path__, gt.__name__ + '.'):
        tests.addTests(doctest.DocTestSuite(module))
    return tests
