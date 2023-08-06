import matplotlib.pyplot as plt
import seaborn as sns


def plot_acf(acf, var_name):
    fig = plt.plot(acf, 'r')
    plt.xlabel("Lags")
    plt.ylabel("ACF")
    plt.title("ACF of random variable " + var_name)
    return fig


def plot_posterior(trace, var_name):
    fig = sns.distplot(trace, hist=False, kde=True, kde_kws={'shade': True, 'linewidth': 2})
    plt.xlabel(var_name)
    plt.ylabel("Density")
    plt.title("Posterior Density Plot of "+var_name)
    return fig


def plot_trace(trace, var_name):
    # TODO: discard burn-ins?
    fig = plt.plot(trace, 'b')
    plt.xlabel("Samples")
    plt.ylabel(var_name)
    plt.title("Trace Plot of "+var_name)
    return fig

