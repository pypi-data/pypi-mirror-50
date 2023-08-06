from pyBlang import plots, diagnostics
import pandas as pd


class Variable:

    def __init__(self, path):
        self.path = path
        self.name = self.__set_name()
        self.df = pd.read_csv(self.path, index_col=0)
        self.trace = self.df.values
        self.summary = self.df.describe()

    def __set_name(self):
        """ Helper function to set the name of the random variable object """
        return self.path.split("/")[len(self.path.split("/")) - 1].replace(".csv", "")

    def plot_posterior(self):
        """ Returns the posterior pdf/pmf plot for this random variable """
        # TODO: add hist argument?
        return plots.plot_posterior(self.trace, self.name)

    def plot_trace(self):
        """ Returns the trace plot for the MCMC samples of this random variable """
        return plots.plot_trace(self.trace, self.name)

    def plot_acf(self):
        """ Returns the ACF plot of the random variable """
        return plots.plot_acf(self.get_acf(), self.name)

    def get_acf(self):
        """ Calculates and returns the acf of the random variable """
        return diagnostics.autocorr(self.trace)

    def get_ess(self):
        """
        Returns the ESS calculated by blang for this random variable.

        Throws exception if file was not found (Post-processing option was not selected)
        :return: ESS
        """
        try:
            ess = pd.read_csv(self.path.split('samples/')[0]+'ess/'+self.name+'.csv',index_col=0).values
            print("ESS for this random variable is: " + ess)
            return ess
        except FileNotFoundError:
            print("ESS was not calculated for this run, select 'DefaultPostProcessor option for ESS calculations")



