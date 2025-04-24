import base64
import io
import logging
import matplotlib
import matplotlib.pyplot as plt
matplotlib.use('Agg')
import numpy as np

from import_data import import_values
from co2e import calculate_co2e_emissions

def plot_agtp_lines(co2_plot, ch4_plot, n2o_plot, agwp_net_plot, agtp_net_plot, metric):
    """
    Purpose: Plots the AGTP graph
    Arguments: co2 plot, ch4 plot, n2o plot, net plot for agwp, net plot for agtp, and the co2e metric selected
    """
    time = 101

    co2e_emissions = calculate_co2e_emissions(agwp_net_plot, agtp_net_plot, metric)

    co2e_plot = np.zeros(time)
    agtp_co2 = import_values("ghc_metrics/agtp_co2.txt") * 1000

     # If co2e metric is not "none selected" then update values in the co2e plot vector
    if metric != "none":
        for t in range(1, time):
            co2e_plot[t:] += co2e_emissions[t - 1] * agtp_co2[:time - t]

    lines = []
    x_range = np.arange(time)

    # Add plots and their labels
    lines.append((x_range, co2_plot, f"CO2"))
    lines.append((x_range, ch4_plot, f"CH4"))
    lines.append((x_range, n2o_plot, f"N2O"))
    lines.append((x_range, agtp_net_plot, f"Net"))
    if metric != "none": lines.append((x_range, co2e_plot, f"CO2e"))

    plt.figure(figsize=(6, 4))
    for x_values, y_values, label in lines:
        plt.plot(x_values, y_values, label=label)

    plt.title("Intervention Temp Response")
    plt.xlabel("time (years)")
    plt.ylabel("Temp. Anomoly (K)")

    plt.legend()
    plt.grid(True)

    img = io.BytesIO()
    plt.savefig(img, format='png')
    plt.close()
    img.seek(0)
    plot_url = base64.b64encode(img.getvalue()).decode('utf-8')

    return plot_url, co2e_plot