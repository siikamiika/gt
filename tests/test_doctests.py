import doctest
import pkgutil

try:
    import gt
except ImportError: # hack for pylint
    from .. import gt # pylint: disable=import-self

def load_tests(loader, tests, ignore): # pylint: disable=unused-argument
    for _, module, _ in pkgutil.iter_modules(gt.__path__, gt.__name__ + '.'):
        tests.addTests(doctest.DocTestSuite(module))
    return tests
