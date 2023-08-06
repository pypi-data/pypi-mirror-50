import unittest
from pyBlang import result


class Test(unittest.TestCase):

    def setUp(self):
        res = result.Result(path="/Users/sahand/Desktop/blang/workspace/" +
                                 "blangProject/results/all/2019-05-22-11-21-11-Yq2Hfp2L.exec",
                            post_proc_option="DefaultPostProcessor")
        return res

    def test_result(self):
        res = self.setUp()

        print(res.samples)
        print(res.monitoring)

        print(res.variables)

        self.assertEqual(len(res.variables), len(res.samples))

