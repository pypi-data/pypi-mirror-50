from pyBlang import model
import unittest
import os


class Test(unittest.TestCase):

    def test_model_basic(self):
        """ test basic model instantiation (minimal arguments) """
        mod = model.Model(name="test", project_path="/Users/Sahand/desktop/blang/workspace/blangProject",
                          post_process="NoPostProcessor")
        self.assertEqual(mod.name, "test")
        self.assertEqual(mod.blang_args, "--model test --postProcessor NoPostProcessor ")

    def test_model_all(self):
        """ test instantiation of a model with all constructor arguments """
        mod = model.Model(name="HierarchicalRugby", project_path="/Users/Sahand/desktop/blang/workspace/blangProject",
                          post_process="NoPostProcessor",
                          data="/Users/Sahand/Desktop/blang/workspace/blangProject/data/blang-rugby.csv")
        self.assertEqual(mod.name, "HierarchicalRugby")
        self.assertEqual(mod.data_name, "blang-rugby")

        mod = model.Model(name="HierarchicalRugby", project_path="/Users/Sahand/desktop/blang/workspace/blangProject",
                          post_process="NoPostProcessor",
                          data="/Users/Sahand/Desktop/blang/workspace/blangProject/data/blang-rugby.csv",
                          data_name="data")
        self.assertEqual(mod.name, "HierarchicalRugby")
        self.assertEqual(mod.data_name, "data")
        self.assertEqual(mod.data, "/Users/Sahand/Desktop/blang/workspace/blangProject/data/blang-rugby.csv")
        self.assertEqual(mod.blang_args,
                         "--model HierarchicalRugby --postProcessor NoPostProcessor " +
                         "--HierarchicalRugby.data " +
                         "/Users/Sahand/Desktop/blang/workspace/blangProject/data/blang-rugby.csv")

    def test_run(self):
        """ tests that model.run() correctly sets the path to the results folder"""
        mod1 = model.Model("test", "/Users/Sahand/Desktop/blang/workspace/blangProject")
        res1 = mod1.run()
        path = "/Users/Sahand/Desktop/blang/workspace/blangProject/results/" + \
               os.readlink("/Users/Sahand/Desktop/blang/workspace/blangProject/results/latest")
        self.assertEqual(path, mod1.res_path)
        self.assertEqual(path, res1.path)
        self.assertEqual(res1.path, mod1.res_path)

        # TODO: fix issue with importing functions in the model and/or find other plated model to use
        # 'blangProject.RugbyFn.xtend cannot be resolved to a type' persists when running other models in the project,
        # and is fixed on removal of the model and fn file

        # mod2 = model.Model(name="HierarchicalRugby", project_path="/Users/Sahand/desktop/blang/workspace/blangProject",
        #                   post_process="NoPostProcessor",
        #                   data="/Users/Sahand/Desktop/blang/workspace/blangProject/data/blang-rugby.csv",
        #                   data_name="data")
        # res2 = mod2.run()
        # self.assertEqual(mod2.res_path,
        #                  os.readlink("/Users/Sahand/Desktop/blang/workspace/blangProject/results/latest"))
        # self.assertEqual(res2.path, os.readlink("/Users/Sahand/Desktop/blang/workspace/blangProject/results/latest"))
        # self.assertEqual(res2.path, mod2.res_path)
