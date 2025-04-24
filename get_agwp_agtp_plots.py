import base64
import io
import logging
import matplotlib
import matplotlib.pyplot as plt
matplotlib.use('Agg')
import numpy as np

from import_data import import_values

def get_agwp_lines(co2_emissions, ch4_emissions, n2o_emissions):
    """
    Purpose: Creates the AGWP plots based on the emissions data provided
    Arguments: Emissions vectors for co2, ch4, and n2o (created in app.py)
    """
    time = 101

    # initialize vectors to all 0s
    co2_plot = np.zeros(time)
    ch4_plot = np.zeros(time)
    n2o_plot = np.zeros(time)
    net_plot = np.zeros(time)

    agwp_co2 = import_values("ghc_metrics/agwp_co2.txt") * 1000
    agwp_ch4 = import_values("ghc_metrics/agwp_ch4.txt") * 1000
    agwp_n2o = import_values("ghc_metrics/agwp_n2o.txt") * 1000

    for t in range(1, time):  # Start from t=1 (second year)
        co2_plot[t:] += co2_emissions[t - 1] * agwp_co2[:time - t]
        ch4_plot[t:] += ch4_emissions[t - 1] * agwp_ch4[:time - t]
        n2o_plot[t:] += n2o_emissions[t - 1] * agwp_n2o[:time - t]

    net_plot = co2_plot + ch4_plot + n2o_plot

    return co2_plot, ch4_plot, n2o_plot, net_plot


def get_agtp_lines(co2_emissions, ch4_emissions, n2o_emissions):
    """
    Purpose: Creates the AGTP plots based on the emissions data provided
    Arguments: Emissions vectors for co2, ch4, and n2o (created in app.py)
    """
    time = 101

    # initialize vectors to all 0s
    co2_plot = np.zeros(time)
    ch4_plot = np.zeros(time)
    n2o_plot = np.zeros(time)
    net_plot = np.zeros(time)

    agtp_co2 = import_values("ghc_metrics/agtp_co2.txt") * 1000
    agtp_ch4 = import_values("ghc_metrics/agtp_ch4.txt") * 1000
    agtp_n2o = import_values("ghc_metrics/agtp_n2o.txt") * 1000

    for t in range(1, time):  # Start from t=1 (second year)
        co2_plot[t:] += co2_emissions[t - 1] * agtp_co2[:time - t]
        ch4_plot[t:] += ch4_emissions[t - 1] * agtp_ch4[:time - t]
        n2o_plot[t:] += n2o_emissions[t - 1] * agtp_n2o[:time - t]

    net_plot = co2_plot + ch4_plot + n2o_plot

    return co2_plot, ch4_plot, n2o_plot, net_plot
