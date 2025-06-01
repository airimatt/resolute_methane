import base64
from flask import Flask, render_template, request
import numpy as np
import logging

# Import custom plotting and processing modules
from plot_agwp import plot_agwp_lines
from plot_agtp import plot_agtp_lines
from scenario_intervention import plot_scenario_intervention
from get_agwp_agtp_plots import get_agwp_lines, get_agtp_lines
from intervention_emissions import plot_intervention_emissions

logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')  # Change to INFO

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    time = 100
    duration, duration2 = 0, 0
    decay_type = ""
    total_lifetime, total_lifetime2 = 1, 1
    halflife, co2_capture_yr1, halflife2, co2_capture_yr1_2 = 1.0, 1.0, 1.0, 1.0

    # Initialize emissions for both interventions in a table
    intervention_data = {
        "intervention1": {"co2": np.zeros(time), "ch4": np.zeros(time), "n2o": np.zeros(time)},
        "intervention2": {"co2": np.zeros(time), "ch4": np.zeros(time), "n2o": np.zeros(time)}
    }

    # Default values
    co2_val = ch4_val = n2o_val = 0.0
    co2_val2 = ch4_val2 = n2o_val2 = 0.0
    intervention = "manual"
    intervention2 = "manual2"
    scenario = "SSP1-1.9"
    metric = "none"
    intervention_start = 2024
    active_intervention = "intervention1"
    tch4_yr = tch4_yr2 = 1.0

    if request.method == 'POST':
        active_intervention = request.form.get("submit_source", "intervention1")
        scenario = request.form.get('scenarioSelect', scenario)
        metric = request.form.get('Metric', metric)
        intervention_start = int(request.form.get('year_intervention_start', intervention_start))

        # if active_intervention == "intervention1":
        #     intervention = request.form.get('Intervention')
        #     co2 = intervention_data["intervention1"]["co2"]
        #     ch4 = intervention_data["intervention1"]["ch4"]
        #     n2o = intervention_data["intervention1"]["n2o"]

        #     if intervention == "manual":
        #         co2_val = float(request.form.get('co2_value') or 0.0)
        #         ch4_val = float(request.form.get('ch4_value') or 0.0)
        #         n2o_val = float(request.form.get('n2o_value') or 0.0)
        #         co2[0], ch4[0], n2o[0] = co2_val, ch4_val, n2o_val
        #     elif intervention == "co2_mitigation":
        #         co2_val = float(request.form.get('co2_ch4_mit_value') or 0.0)
        #         co2[0], ch4[0] = co2_val, -1.0
        #     elif intervention == "ch4_flux":
        #         duration = int(request.form.get('duration_value') or 0)
        #         tch4_yr = float(request.form.get('tch4_yr') or 1.0)
        #         ch4[:duration] = tch4_yr
        #     elif intervention == "co2_capture":
        #         co2_capture_yr1 = float(request.form.get('co2_capture_yr1') or 1.0)
        #         decay_type = request.form.get('CO2_Decay_Type')
        #         co2[0] = -co2_capture_yr1
        #         if decay_type == "linear_decay":
        #             total_lifetime = int(request.form.get('total_lifetime') or 50)
        #             co2[1:total_lifetime+1] = co2_capture_yr1 / total_lifetime
        #         else:
        #             halflife = float(request.form.get('halflife') or 1.0)
        #             lam = np.log(2) / halflife
        #             for t in range(1, time):
        #                 co2[t] = co2_capture_yr1 * np.exp(-lam * t) * lam

        # elif active_intervention == "intervention2":
        #     intervention2 = request.form.get('Intervention2')
        #     co2 = intervention_data["intervention2"]["co2"]
        #     ch4 = intervention_data["intervention2"]["ch4"]
        #     n2o = intervention_data["intervention2"]["n2o"]

        #     if intervention2 == "manual2":
        #         co2_val2 = float(request.form.get('co2_value2') or 0.0)
        #         ch4_val2 = float(request.form.get('ch4_value2') or 0.0)
        #         n2o_val2 = float(request.form.get('n2o_value2') or 0.0)
        #         co2[0], ch4[0], n2o[0] = co2_val2, ch4_val2, n2o_val2
        #     elif intervention2 == "co2_mitigation2":
        #         co2_val2 = float(request.form.get('co2_ch4_mit_value2') or 0.0)
        #         co2[0], ch4[0] = co2_val2, -1.0
        #     elif intervention2 == "ch4_flux2":
        #         duration2 = int(request.form.get('duration_value2') or 0)
        #         tch4_yr2 = float(request.form.get('tch4_yr2') or 1.0)
        #         ch4[:duration] = tch4_yr2
        #     elif intervention2 == "co2_capture2":
        #         co2_capture_yr1 = float(request.form.get('co2_capture_year_1_2') or 1.0)
        #         decay_type = request.form.get('CO2_Decay_Type2')
        #         co2[0] = -co2_capture_yr1
        #         if decay_type == "linear_decay2":
        #             total_lifetime = int(request.form.get('total_lifetime2') or 50)
        #             co2[1:total_lifetime+1] = co2_capture_yr1 / total_lifetime
        #         else:
        #             halflife = float(request.form.get('halflife2') or 1.0)
        #             lam = np.log(2) / halflife
        #             for t in range(1, time):
        #                 co2[t] = co2_capture_yr1 * np.exp(-lam * t) * lam
        #
        # Use only the active intervention to generate plots
        # co2_emissions = intervention_data[active_intervention]["co2"]
        # ch4_emissions = intervention_data[active_intervention]["ch4"]
        # n2o_emissions = intervention_data[active_intervention]["n2o"]

        # Get the intervention type and values from the form for Intervention 1
        intervention = request.form.get('Intervention', 'manual')
        co2_val = float(request.form.get('co2_value') or 0.0)
        ch4_val = float(request.form.get('ch4_value') or 0.0)
        n2o_val = float(request.form.get('n2o_value') or 0.0)
        co2_ch4_mit_value = float(request.form.get('co2_ch4_mit_value') or 0.0)
        duration = int(request.form.get('duration_value') or 0)
        tch4_yr = float(request.form.get('tch4_yr') or 1.0)
        co2_capture_yr1 = float(request.form.get('co2_capture_yr1') or 1.0)
        decay_type = request.form.get('CO2_Decay_Type', '')
        total_lifetime = int(request.form.get('total_lifetime') or 1)
        halflife = float(request.form.get('halflife') or 1.0)

        # Get the intervention type and values from the form for Intervention 2
        intervention2 = request.form.get('Intervention2', 'manual2')
        co2_val2 = float(request.form.get('co2_value2') or 0.0)
        ch4_val2 = float(request.form.get('ch4_value2') or 0.0)
        n2o_val2 = float(request.form.get('n2o_value2') or 0.0)
        co2_ch4_mit_value2 = float(request.form.get('co2_ch4_mit_value2') or 0.0)
        duration2 = int(request.form.get('duration_value2') or 0)
        tch4_yr2 = float(request.form.get('tch4_yr2') or 1.0)
        co2_capture_yr1_2 = float(request.form.get('co2_capture_year_1_2') or 1.0)
        decay_type2 = request.form.get('CO2_Decay_Type2', '')
        total_lifetime2 = int(request.form.get('total_lifetime2') or 1)
        halflife2 = float(request.form.get('halflife2') or 1.0)

        # Get the selected intervention data based on active_intervention and get the emissions plots
        selected_intervention = intervention_data[active_intervention]
        co2_emissions = selected_intervention["co2"]
        ch4_emissions = selected_intervention["ch4"]
        n2o_emissions = selected_intervention["n2o"]

        # Process emissions based on selected intervention type
        if active_intervention == "intervention1":
            if intervention == "manual":
                co2_emissions[0], ch4_emissions[0], n2o_emissions[0] = co2_val, ch4_val, n2o_val
            elif intervention == "co2_mitigation":
                co2_emissions[0], ch4_emissions[0] = co2_ch4_mit_value, -1.0
            elif intervention == "ch4_flux":
                ch4_emissions[:duration] = tch4_yr
            elif intervention == "co2_capture":
                co2_emissions[0] = -co2_capture_yr1
                if decay_type == "linear_decay":
                    co2_emissions[1:total_lifetime+1] = co2_capture_yr1 / total_lifetime
                elif decay_type == "exponential_decay":
                    lam = np.log(2) / halflife
                    for t in range(1, time):
                        co2_emissions[t] = co2_capture_yr1 * np.exp(-lam * t) * lam
        elif active_intervention == "intervention2":
            if intervention2 == "manual2":
                co2_emissions[0], ch4_emissions[0], n2o_emissions[0] = co2_val2, ch4_val2, n2o_val2
            elif intervention2 == "co2_mitigation2":
                co2_emissions[0], ch4_emissions[0] = co2_ch4_mit_value2, -1.0
            elif intervention2 == "ch4_flux2":
                ch4_emissions[:duration2] = tch4_yr2
            elif intervention2 == "co2_capture2":
                co2_emissions[0] = -co2_capture_yr1_2
                if decay_type2 == "linear_decay2":
                    co2_emissions[1:total_lifetime2+1] = co2_capture_yr1_2 / total_lifetime2
                elif decay_type2 == "exponential_decay2":
                    lam = np.log(2) / halflife2
                    for t in range(1, time):
                        co2_emissions[t] = co2_capture_yr1_2 * np.exp(-lam * t) * lam

        # Generate the plots
        agwp_co2_plot, agwp_ch4_plot, agwp_n2o_plot, agwp_net_plot = get_agwp_lines(co2_emissions, ch4_emissions, n2o_emissions)
        agtp_co2_plot, agtp_ch4_plot, agtp_n2o_plot, agtp_net_plot = get_agtp_lines(co2_emissions, ch4_emissions, n2o_emissions)

        # Get the plot urls for the AGWP and AGTP graphs
        agwp_plot_url = plot_agwp_lines(agwp_co2_plot, agwp_ch4_plot, agwp_n2o_plot, agwp_net_plot, agtp_net_plot, metric)
        agtp_plot_url, co2e_plot = plot_agtp_lines(agtp_co2_plot, agtp_ch4_plot, agtp_n2o_plot, agwp_net_plot, agtp_net_plot, metric)

        # Get the plot url for the scenario intervention graph
        scenario_plot_url = plot_scenario_intervention(scenario, intervention_start, agtp_net_plot, co2e_plot, metric)
        intervention_emissions_plot_url = plot_intervention_emissions(co2_emissions, ch4_emissions, n2o_emissions)

        active_tab = active_intervention

        return render_template('index.html',
            intervention=intervention, intervention2=intervention2,
            plot_url=agwp_plot_url, plot_url2=agtp_plot_url,
            plot_url3=scenario_plot_url, plot_url4=intervention_emissions_plot_url,
            co2_value=co2_val, ch4_value=ch4_val, n2o_value=n2o_val,
            co2_value2=co2_val2, ch4_value2=ch4_val2, n2o_value2=n2o_val2,
            co2_ch4_mit_value=co2_ch4_mit_value, co2_ch4_mit_value2=co2_ch4_mit_value2,
            duration=duration, duration2=duration2, tch4_yr=tch4_yr, tch4_yr2=tch4_yr2,
            co2_capture_yr1=co2_capture_yr1, co2_capture_yr1_2=co2_capture_yr1_2,
            decay_type=decay_type, decay_type2=decay_type2,
            total_lifetime=total_lifetime, halflife=halflife,
            total_lifetime2=total_lifetime2, halflife2=halflife2,
            scenario=scenario, intervention_start=intervention_start,
            agtp_net_plot=agtp_net_plot, co2e_plot=co2e_plot,
            metric=metric, active_intervention=active_intervention, active_tab=active_intervention)

    else:
        # GET request — use default values
        scenario = "SSP1-1.9"
        metric = "none"
        intervention_start = 2024
        active_intervention = "intervention1"

        co2_val = ch4_val = n2o_val = 1.0
        co2_val2 = ch4_val2 = n2o_val2 = 1.0

        co2_emissions = np.zeros(time)
        ch4_emissions = np.zeros(time)
        n2o_emissions = np.zeros(time)

        agwp_co2_plot, agwp_ch4_plot, agwp_n2o_plot, agwp_net_plot = get_agwp_lines(co2_emissions, ch4_emissions, n2o_emissions)
        agtp_co2_plot, agtp_ch4_plot, agtp_n2o_plot, agtp_net_plot = get_agtp_lines(co2_emissions, ch4_emissions, n2o_emissions)

        agwp_plot_url = plot_agwp_lines(agwp_co2_plot, agwp_ch4_plot, agwp_n2o_plot, agwp_net_plot, agtp_net_plot, metric)
        agtp_plot_url, co2e_plot = plot_agtp_lines(agtp_co2_plot, agtp_ch4_plot, agtp_n2o_plot, agwp_net_plot, agtp_net_plot, metric)

        scenario_plot_url = plot_scenario_intervention(scenario, intervention_start, agtp_net_plot, co2e_plot, metric)
        intervention_emissions_plot_url = plot_intervention_emissions(co2_emissions, ch4_emissions, n2o_emissions)

        return render_template('index.html',
            intervention=intervention, intervention2=intervention2,
            plot_url=agwp_plot_url, plot_url2=agtp_plot_url,
            plot_url3=scenario_plot_url, plot_url4=intervention_emissions_plot_url,
            co2_value=co2_val, ch4_value=ch4_val, n2o_value=n2o_val,
            co2_value2=co2_val2, ch4_value2=ch4_val2, n2o_value2=n2o_val2,
            tch4_yr=tch4_yr, duration=duration, decay_type=decay_type,
            total_lifetime=total_lifetime, halflife=halflife,
            co2_capture_yr1=co2_capture_yr1,
            scenario=scenario, intervention_start=intervention_start,
            agtp_net_plot=agtp_net_plot, co2e_plot=co2e_plot,
            metric=metric, active_intervention=active_intervention, active_tab=active_intervention)


# Run the Flask app
if __name__ == '__main__':
    app.run(debug=True)