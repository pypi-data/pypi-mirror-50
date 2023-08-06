from pyBlang import result
import unittest


class Test(unittest.TestCase):

    def setUp(self):
        res = result.Result(path="/Users/sahand/Desktop/blang/workspace/" +
                                 "blangProject/results/all/2019-05-22-11-21-11-Yq2Hfp2L.exec",
                            post_proc_option="DefaultPostProcessor")
        return res.variables.get('y')

    def test_init(self):
        y = self.setUp()
        self.assertTrue(y.name == 'y')
        self.assertEqual(y.trace.shape, (1001, 1))
        self.assertEqual(y.path, "/Users/sahand/Desktop/blang/workspace/" +
                                 "blangProject/results/all/2019-05-22-11-21-11-Yq2Hfp2L.exec/samples/y.csv")

    def test_get_ess(self):
        y = self.setUp()
        try:
            y.get_ess()
            pass
        except FileNotFoundError:
            self.fail("Should not be throwing an exception")



