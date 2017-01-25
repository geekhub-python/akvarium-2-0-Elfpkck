import os
import sys
import unittest

sys.path.append(
    os.path.abspath(os.path.join(os.path.dirname(__file__), os.path.pardir)))

from inhabitants import Inhabitant


class TestInhabitant(unittest.TestCase):
    def setUp(self):
        self.inh = Inhabitant(10)

    def testWeight(self):
        self.assertEqual(10, self.inh.weight)


class TestAquarium(unittest.TestCase):
    def testSingleton(self):
        from aquarium import aquarium
        id1 = id(aquarium)
        del aquarium
        from aquarium import aquarium
        self.assertEqual(id1, id(aquarium))


def run_tests(classname):
    class_to_test = classname()
    suite = unittest.TestLoader().loadTestsFromModule(class_to_test)
    unittest.TextTestRunner().run(suite)

if __name__ == '__main__':
    run_tests(TestInhabitant)
    run_tests(TestAquarium)