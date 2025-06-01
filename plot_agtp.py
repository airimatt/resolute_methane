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

# import base64
# import io
# import logging
# import matplotlib
# import matplotlib.pyplot as plt
# matplotlib.use('Agg')
# import numpy as np

# from import_data import import_values
# from co2e import calculate_co2e_emissions

# def plot_agtp_lines(co2_plot, ch4_plot, n2o_plot, agwp_net_plot, agtp_net_plot, metric, scenario):
#     """
#     Purpose: Plots the AGTP graph,
#     Arguments: co2 plot, ch4 plot, n2o plot, net plot for agwp, net plot for agtp, and the co2e metric selected
#     """
#     time = 101

#     co2e_emissions = calculate_co2e_emissions(agwp_net_plot, agtp_net_plot, metric)

#     co2e_plot = np.zeros(time)
#     agtp_co2 = import_values("ghc_metrics/agtp_co2.txt") * 1000

#      # If co2e metric is not "none selected" then update values in the co2e plot vector
#     if metric != "none":
#         for t in range(1, time):
#             co2e_plot[t:] += co2e_emissions[t - 1] * agtp_co2[:time - t]

#     shift_x_axis = False

#     scenario_plot = np.zeros(time)
#     if scenario != "none":
#         if scenario == "SSP1-1.9":
#             scenario_plot = import_values("ssp_data/ssp119_dt.txt")[5:]
#         elif scenario == "SSP1-2.6":
#             scenario_plot = import_values("ssp_data/ssp126_dt.txt")[5:]
#         elif scenario == "SSP2-4.5":
#             scenario_plot = import_values("ssp_data/ssp245_dt.txt")[5:]
#         elif scenario == "SSP3-7.0":
#             scenario_plot = import_values("ssp_data/ssp370_dt.txt")[5:]
#         elif scenario == "SSP4-3.4_over":
#             scenario_plot = import_values("ssp_data/ssp434_over_dt.txt")[5:]
#         else:
#             scenario_plot = import_values("ssp_data/ssp585_dt.txt")[5:]

#         shift_x_axis = True

#     lines = []
#     x_range = np.arange(time)

#     # if shift_x_axis:
#     #     x_range = np.arange(2000, 2101)
#     #     pad = 2000 - 0  # Shift from year 0 to year 2000
#     #     co2_plot = np.pad(co2_plot, (pad, 0), 'constant')[:101]
#     #     ch4_plot = np.pad(ch4_plot, (pad, 0), 'constant')[:101]
#     #     n2o_plot = np.pad(n2o_plot, (pad, 0), 'constant')[:101]
#     #     agtp_net_plot = np.pad(agtp_net_plot, (pad, 0), 'constant')[:101]
#     #     co2e_plot = np.pad(co2e_plot, (pad, 0), 'constant')[:101]
#     # else:
#     #     x_range = np.arange(time)
#     # x_range = np.arange(2000, 2000 + time) if shift_x_axis else np.arange(time)

#     # print("Max CO2:", np.max(co2_plot))
#     # print("Max CH4:", np.max(ch4_plot))
#     # print("Max N2O:", np.max(n2o_plot))
#     # print("Max Net:", np.max(agtp_net_plot))
#     # print("Max SSP:", np.max(scenario_plot))

#     # Add plots and their labels
#     lines.append((x_range, co2_plot, f"CO2"))
#     lines.append((x_range, ch4_plot, f"CH4"))
#     lines.append((x_range, n2o_plot, f"N2O"))
#     lines.append((x_range, agtp_net_plot, f"Net"))
#     if metric != "none": lines.append((x_range, co2e_plot, f"CO2e"))
#     # if scenario != "none": lines.append((x_range, scenario_plot, f"Baseline SSP"))

#     # Create main plot
#     fig, ax1 = plt.subplots(figsize=(6, 4))
#     ax1.set_xlabel("time (years)")
#     ax1.set_ylabel("Temp. Anomaly (K) - Intervention", color="black")

#     # Plot intervention lines
#     ax1.plot(x_range, co2_plot, label="CO2", color="lightblue")
#     ax1.plot(x_range, ch4_plot, label="CH4", color="green")
#     ax1.plot(x_range, n2o_plot, label="N2O", color="orange")
#     ax1.plot(x_range, agtp_net_plot, label="Net", color="red")
#     if metric != "none":
#         ax1.plot(x_range, co2e_plot, label="CO2e", color="red")

#     ax1.tick_params(axis='y')
#     ax1.grid(True)

#     # Optional: Second axis for SSP baseline
#     if scenario != "none":
#         ax2 = ax1.twinx()
#         ax2.set_ylabel("Temp. Anomaly (K) - Baseline SSP", color="purple")
#         ax2.plot(x_range, scenario_plot, label="Baseline SSP", color="purple", linestyle="--")
#         ax2.tick_params(axis='y', labelcolor="purple")

#     # Legend handling
#     lines_labels = ax1.get_legend_handles_labels()
#     if scenario != "none":
#         lines_labels_2 = ax2.get_legend_handles_labels()
#         lines_labels = (lines_labels[0] + lines_labels_2[0], lines_labels[1] + lines_labels_2[1])
#     fig.legend(*lines_labels, loc="upper left", bbox_to_anchor=(0.1, 0.92), fontsize="small")

#     fig.tight_layout()

#     # Save and return as base64
#     img = io.BytesIO()
#     plt.savefig(img, format='png')
#     plt.close()
#     img.seek(0)
#     plot_url = base64.b64encode(img.getvalue()).decode('utf-8')

#     return plot_url, co2e_plot