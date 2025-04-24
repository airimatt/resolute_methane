import base64
import io
import logging
import matplotlib
import matplotlib.pyplot as plt
matplotlib.use('Agg')
import numpy as np

from import_data import import_values

def plot_scenario_intervention(scenario, intervention_start, agtp_net_plot, co2e_plot, metric):
    """
    Purpose: Plots the Scenario with Intervention plot
    Arguments:
    """
    time = 106

    # Determine line to plot based off of selected SSP scenario
    scenario_plot = np.zeros(time)
    if scenario == "SSP1-1.9":
        scenario_plot = import_values("ssp_data/ssp119_dt.txt")
    elif scenario == "SSP1-2.6":
        scenario_plot = import_values("ssp_data/ssp126_dt.txt")
    elif scenario == "SSP2-4.5":
        scenario_plot = import_values("ssp_data/ssp245_dt.txt")
    elif scenario == "SSP3-7.0":
        scenario_plot = import_values("ssp_data/ssp370_dt.txt")
    elif scenario == "SSP4-3.4_over":
        scenario_plot = import_values("ssp_data/ssp434_over_dt.txt")
    else:
        scenario_plot = import_values("ssp_data/ssp585_dt.txt")

    # Get historical data (scatter plot)
    years_historical = np.arange(1995, 2024)
    historical_obs = import_values("ssp_data/historical_dt.txt")

    # Create offset vectors
    net_offset = np.zeros(time)
    yr_offset = intervention_start - 1995 # hard coded 1995 for now, can change to be first index of array of years
    co2e_net_offset = np.zeros(time)

    # Find start and end indices to use for plotting
    start_index = yr_offset
    end_index = min(time, yr_offset + 100)
    source_end_index = min(time, time - yr_offset)

    # Update values in the net offset vector
    agtp_net_plot[:source_end_index] *= 5e9
    net_offset[start_index:end_index] = agtp_net_plot[:source_end_index]

    # Define intervention1 plot to be the sum of the scenario and net offset plots
    intervention1 = scenario_plot + net_offset

    # Update values in the co2e net offset vector
    co2e_plot[:source_end_index] *= 5e9
    co2e_net_offset[start_index:end_index] = co2e_plot[:source_end_index]

    # Define co2e plot to be the sum of the scenario and co2e net offset plots
    co2e = scenario_plot + co2e_net_offset

    lines = []
    x_range = np.arange(1995, 2101) # x-axis range from 1995 to 2100

    # Add plots and their labels
    lines.append((x_range, scenario_plot, f"Baseline SSP"))
    lines.append((x_range, intervention1, f"Intervention 1"))
    if metric != "none": lines.append((x_range, co2e, f"CO2e"))

    plt.figure(figsize=(10, 8))

    plt.scatter(years_historical, historical_obs, color='black', marker='.', label='Historical Obs.')

    for x_values, y_values, label in lines:
        plt.plot(x_values, y_values, label=label)

    plt.title("Scenario with Intervention")
    plt.xlabel("time (years)")
    plt.ylabel("*C from pre-industrial")

    plt.xticks(np.arange(2000, 2101, 10))  # Set x-axis ticks starting from 2000
    plt.legend()
    plt.grid(True)

    img = io.BytesIO()
    plt.savefig(img, format='png')
    plt.close()
    img.seek(0)
    plot_url = base64.b64encode(img.getvalue()).decode('utf-8')

    return plot_url