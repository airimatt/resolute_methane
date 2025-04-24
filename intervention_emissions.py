import base64
import io
import logging
import matplotlib
import matplotlib.pyplot as plt
matplotlib.use('Agg')
import numpy as np

from import_data import import_values

def plot_intervention_emissions(co2_emissions, ch4_emissions, n2o_emissions):
    """
    Purpose: Plots the Intervention Emissions graph
    Arguments: Emissions vectors for co2, ch4, and n2o (created in app.py)
    """
    time = 100

    lines = []
    x_range = np.arange(time)

    # Add plots and their labels
    lines.append((x_range, co2_emissions, f"CO2"))
    lines.append((x_range, ch4_emissions, f"CH4"))
    lines.append((x_range, n2o_emissions, f"N2O"))

    plt.figure(figsize=(4, 2))

    for x_values, y_values, label in lines:
        plt.plot(x_values, y_values, label=label)

    plt.scatter(x_range[0], co2_emissions[0])
    plt.scatter(x_range[0], ch4_emissions[0])
    plt.scatter(x_range[0], n2o_emissions[0])

    plt.title("Intervention Emissions")
    plt.xlabel("time (years)")
    plt.ylabel("tons")

    plt.legend()
    plt.grid(True)

    img = io.BytesIO()
    plt.savefig(img, format='png')
    plt.close()
    img.seek(0)
    plot_url = base64.b64encode(img.getvalue()).decode('utf-8')

    return plot_url