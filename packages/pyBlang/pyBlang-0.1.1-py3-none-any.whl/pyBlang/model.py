import os
from pyBlang import result


class Model:

    def __init__(self, name, project_path, data=None, blang_args=None,
                 out_path=True, data_name=None, post_process="NoPostProcessor"):
        """
        Constructor for a Blang model object.

        :param name: name of the model to be run (name of .bl file)
        :param project_path: filepath to the Blang project directory that houses the .bl file
        :param data: optional argument to pass in observed data (in .csv format) into blang
        :param blang_args: additional runtime arguments, full list of which is here:
            https://www.stat.ubc.ca/~bouchard/blang/
        :param out_path: optional argument, set to false to output to current folder instead of Blang default
        :param data_name: optional argument, use if the name of the parameter in the blang model is different to the
            .csv file's name
        :param post_process: Set post-processing options, defaults to NoPostProcessor, other option is
            DefaultPostProcessor
        """
        # postProcessor options
        post_p_types = ['NoPostProcessor', 'DefaultPostProcessor']

        # Ensure Post Processing option is set correctly
        if post_process not in post_p_types:
            raise ValueError("Invalid PostProcessing Option. Expected one of %s" % post_p_types)

        self.name = name
        self.project_path = project_path
        self.pp_option = post_process

        args = ""
        self.res_path = None
        self.results = None

        # Given a data file, if a custom name has not been set for the model  GlobalDataSource parameter, then the name
        # is set to .csv file's name and appended to blang_args as data_arg

        if data is not None:
            if data_name is not None:
                self.data_name = data_name
            else:
                self.data_name = data.split("/")[len(data.split("/")) - 1].replace(".csv", "")
            self.data = data
            args = args + "--" + self.name + "." + self.data_name + " " + self.data

        # Given a custom output path, adds that to the arguments.
        if out_path is False:
            args = args + " --experimentConfigs.managedExecutionFolder false"

        if blang_args is not None:
            self.blang_args = "--model " + self.name + " " + "--postProcessor " + post_process + " " + blang_args \
                              + " " + args
        else:
            self.blang_args = "--model " + self.name + " " + "--postProcessor " + post_process + " " + args

    def run(self, run_args=None):
        """
        Run the Model with its assigned arguments (set by model constructor) or with different one-time arguments.

        :param run_args: optional, runs the model with these arguments as opposed to the ones defined in model
            instantiation
        :return: A result object that contains the output of the run
        """
        # TODO: Add some print statements with relevant info?
        curdir = os.getcwd()
        os.chdir(self.project_path)

        if run_args is None:
            os.system('blang ' + self.blang_args)
        else:
            os.system('blang ' + run_args)

        self.res_path = self.project_path + "/results/" + os.readlink(self.project_path + "/results/latest")

        os.chdir(curdir)

        self.results = result.Result(self.res_path, self.pp_option)

        return self.results

    # TODO: Add a function that converts python code to a .bl file?
    # TODO: Refactor some of the code in constructor to helper fns for better readability?
