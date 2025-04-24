import base64
import io
import logging
import matplotlib
import matplotlib.pyplot as plt
matplotlib.use('Agg')
import numpy as np

from import_data import import_values

def calculate_co2e_emissions(agwp_net_plot, agtp_net_plot, co2e_metric):
    """
    Purpose: Calculates the CO2 equivalent plot based on the metric value selected
    Arguments: AGWP and AGTP net plots, and the metric value selected by user
    """

    # If "none plotted" was selected, return
    if co2e_metric == "none": return None

    time = 101

    metric_value = 0
    co2e_emissions = np.zeros(time)

    # Get the agwp and agtp values for co2
    agwp_co2 = import_values("ghc_metrics/agwp_co2.txt") * 1000
    agtp_co2 = import_values("ghc_metrics/agtp_co2.txt") * 1000

    # Calculate the metric value based on the selected metric
    if co2e_metric == "GWP100":
        GWP100_unit = agwp_co2[99]
        metric_value = agwp_net_plot[100] / GWP100_unit
    elif co2e_metric == "GWP20":
        GWP20_unit = agwp_co2[19]
        metric_value = agwp_net_plot[20] / GWP20_unit
    elif co2e_metric == "GTP100":
        GTP100_unit = agtp_co2[99]
        metric_value = agtp_net_plot[100] / GTP100_unit
    else:
        GTP20_unit = agtp_co2[19]
        metric_value = agtp_net_plot[20] / GTP20_unit

    # Set the initial value for the co2e emissions to the metric value calculated above
    co2e_emissions[0] = metric_value

    return co2e_emissions