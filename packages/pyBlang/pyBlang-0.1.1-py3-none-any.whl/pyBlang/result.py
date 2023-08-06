import os
from pyBlang import variable, utils


class Result:

    def __init__(self, path, post_proc_option):
        self.path = path
        self.pp_option = post_proc_option
        self.__get_folders()
        self.print_folders()
        self.variables = self.__set_variables()

    def __get_folders(self):
        # res_options = {'NoPostProcessor': ['samples', 'monitoring'],
        #                'DefaultPostProcessor': ['samples', 'posteriorPlots', 'summaries', 'ess', 'tracePlots',
        #                                         'tracePlotsFull', 'monitoring', 'monitoringPlots']}

        if self.pp_option is 'DefaultPostProcessor':
            self.__get_samples()
            self.__get_posterior_plots()
            self.__get_summaries()
            self.__get_ess()
            self.__get_trace_plots()
            self.__get_trace_plots_full()
            self.__get_monitoring()
            self.__get_monitoring_plots()
        else:
            self.__get_samples()
            self.__get_monitoring()

    def __get_samples(self, dataframe=False):
        self.samples = [f for f in os.listdir(self.path+"/samples/") if not f.startswith('.')]
        for i in self.samples:
            if i.endswith('tsv'):
                self.samples.remove(i)
        self.samples = utils.build_idx_dict(self.samples, self.path + "/samples/")

    def __get_posterior_plots(self):
        self.post_plots = os.listdir(self.path + "/posteriorPlots")
        self.post_plots = utils.build_idx_dict(self.post_plots, self.path + "/posteriorPlots/")

    def __get_summaries(self):
        self.summaries = os.listdir(self.path + "/summaries")
        self.summaries = utils.build_idx_dict(self.summaries, self.path + "/summaries/")

    def __get_ess(self):
        self.ess_list = os.listdir(self.path + "/ess")
        self.ess_list = utils.build_idx_dict(self.ess_list, self.path + "/ess/")

    def __get_trace_plots(self):
        self.traces = os.listdir(self.path + "/tracePlots")
        self.traces = utils.build_idx_dict(self.traces, self.path + "/tracePlots/")

    def __get_trace_plots_full(self):
        self.traces_full = os.listdir(self.path + "/tracePlotsFull")
        self.traces_full = utils.build_idx_dict(self.traces_full, self.path + "/tracePlotsFull/")

    def __get_monitoring(self):
        self.monitoring = [f for f in os.listdir(self.path+"/monitoring/") if not f.startswith('.')]
        for i in self.monitoring:
            if i.endswith('tsv'):
                self.monitoring.remove(i)
        self.monitoring = utils.build_idx_dict(self.monitoring, self.path + "/monitoring/")

    def __get_monitoring_plots(self):
        self.monitoring_plots = os.listdir(self.path + "/monitoringPlots")
        self.monitoring_plots = utils.build_idx_dict(self.monitoring_plots, self.path + "/monitoringPlots/")

    def print_folders(self):
        print(str(vars(self).keys()).replace("dict_keys(", "Result folders are: ").replace(")", ""))

    def __set_variables(self):
        paths = self.samples.values()
        rvars = []
        for i in paths:
            rvars.append(variable.Variable(path=i))

        result = {}
        for i in rvars:
            result.update({i.name : i})
        return result
