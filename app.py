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
    co2_emissions = np.zeros(time)
    ch4_emissions = np.zeros(time)
    n2o_emissions = np.zeros(time)
    duration = 0
    decay_type = ""
    total_lifetime = 1
    halflife, co2_capture = 1.0, 1.0

    if request.method == 'POST':

        # Get intervention method
        intervention = request.form.get('Intervention')
        co2_val, ch4_val, n2o_val, tch4_per_yr = 0.0, 0.0, 0.0, 1.0

        # Get metric value (for co2e)
        metric = request.form.get('Metric')

        if intervention == "manual" or intervention == "co2_mitigation":
            # intervention is manual or co2_mitigation
            if intervention == "manual":
                co2 = request.form.get('co2_value', '')
                ch4 = request.form.get('ch4_value', '')
                n2o = request.form.get('n2o_value', '')
                co2_val = float(co2) if co2 else 0.0
                ch4_val = float(ch4) if ch4 else 0.0
                n2o_val = float(n2o) if n2o else 0.0
            else:
                co2_mitigation_value = request.form.get('co2_ch4_mit_value', '')
                co2_val = float(co2_mitigation_value) if co2_mitigation_value else 0.0
                ch4_val = -1.0
            co2_emissions[0] = co2_val
            ch4_emissions[0] = ch4_val
            n2o_emissions[0] = n2o_val
        elif intervention == "ch4_flux":
            # intervention is ch4_flux
            dur = request.form.get('duration_value', '')
            duration = int(dur) if dur else 0
            yr = request.form.get('tch4_yr', '')
            tch4_per_yr = float(yr) if yr else 0.0
            ch4_emissions[:duration] = tch4_per_yr if tch4_per_yr else 1.0
        else:
            # intervention is co2_capture
            co2_capture = float(request.form.get('co2_capture_year_1'))
            if not co2_capture:
                co2_capture = 1.0

            # Get decay type and calculate emissions based on decay type
            decay_type = request.form.get('CO2_Decay_Type')
            if decay_type == "linear_decay":
                total_lifetime = int(request.form.get('total_lifetime', 50))
                emission_rate = co2_capture / total_lifetime
                co2_emissions[0] = -co2_capture
                co2_emissions[1:total_lifetime + 1] = round(emission_rate, 2)
            else:
                # Get halflife (default to 1.0)
                halflife = float(request.form.get('halflife'))
                if not halflife:
                    halflife = 1.0
                co2_emissions[0] = -co2_capture
                if halflife > 0:  # Avoid division by zero
                    lambda_val = np.log(2) / halflife
                    for t in range(1, time):
                        co2_emissions[t] = co2_capture * np.exp(-lambda_val * t) * lambda_val

        # Get ssp scenario (set default value to "SSP1-1.9")
        scenario = request.form.get('scenarioSelect')
        if not scenario:
            scenario = "SSP1-1.9"

        # Generate AGWP and AGTP lines for the emissions
        agwp_co2_plot, agwp_ch4_plot, agwp_n2o_plot, agwp_net_plot = get_agwp_lines(co2_emissions, ch4_emissions, n2o_emissions)
        agtp_co2_plot, agtp_ch4_plot, agtp_n2o_plot, agtp_net_plot = get_agtp_lines(co2_emissions, ch4_emissions, n2o_emissions)

        # Generate plot_url from emissions vectors
        agwp_plot_url = plot_agwp_lines(agwp_co2_plot, agwp_ch4_plot, agwp_n2o_plot, agwp_net_plot, agtp_net_plot, metric)
        agtp_plot_url, co2e_plot = plot_agtp_lines(agtp_co2_plot, agtp_ch4_plot, agtp_n2o_plot, agwp_net_plot, agtp_net_plot, metric)

        # Get intervention start year (default to 2024)
        intervention_start = int(request.form.get('year_intervention_start'))
        if not intervention_start:
            intervention_start = 2024

        # Generate plot_url for scenario with intervention plot and interventions emissions plot
        scenario_plot_url = plot_scenario_intervention(scenario, intervention_start, agtp_net_plot, co2e_plot, metric)
        intervention_emissions_plot_url = plot_intervention_emissions(co2_emissions, ch4_emissions, n2o_emissions)

        # Render the results with all plot URLs (necessary for the values to be available in the html file)
        # This function passes Python variables to the HTML template (in index.html)
        return render_template('index.html', intervention=intervention,
                               plot_url=agwp_plot_url, plot_url2=agtp_plot_url,
                               plot_url3=scenario_plot_url,
                               plot_url4=intervention_emissions_plot_url,
                               co2_value=co2_val, ch4_value=ch4_val, n2o_value=n2o_val,
                               tch4_per_yr=tch4_per_yr, duration=duration, decay_type=decay_type,
                               total_lifetime=total_lifetime, halflife=halflife,
                               co2_capture=co2_capture,
                               scenario=scenario, intervention_start=intervention_start,
                               agtp_net_plot=agtp_net_plot, co2e_plot=co2e_plot,
                               metric=metric)
    else:
        # Default values for the initial page load

        # Handle GET requests (initial page load)
        co2_val, ch4_val, n2o_val = 1.0, 1.0, 1.0
        co2_capture, tch4_per_yr = 1.0, 1.0
        scenario = "SSP1-1.9"
        intervention_start = 2024
        metric = "none"

        # Generate AGWP and AGTP lines for the emissions
        agwp_co2_plot, agwp_ch4_plot, agwp_n2o_plot, agwp_net_plot = get_agwp_lines(co2_emissions, ch4_emissions, n2o_emissions)
        agtp_co2_plot, agtp_ch4_plot, agtp_n2o_plot, agtp_net_plot = get_agtp_lines(co2_emissions, ch4_emissions, n2o_emissions)

        # Generate plot_url from emissions vectors
        agwp_plot_url = plot_agwp_lines(agwp_co2_plot, agwp_ch4_plot, agwp_n2o_plot, agwp_net_plot, agtp_net_plot, metric)
        agtp_plot_url, co2e_plot = plot_agtp_lines(agtp_co2_plot, agtp_ch4_plot, agtp_n2o_plot, agwp_net_plot, agtp_net_plot, metric)

        # Generate plot_url for scenario with intervention plot and interventions emissions plot
        scenario_plot_url = plot_scenario_intervention(scenario, intervention_start, agtp_net_plot, co2e_plot, metric)
        intervention_emissions_plot_url = plot_intervention_emissions(co2_emissions, ch4_emissions, n2o_emissions)

        # Render the results with all plot URLs (necessary for the values to be available in the html file)
        return render_template('index.html', plot_url=agwp_plot_url, plot_url2=agtp_plot_url,
                               plot_url3=scenario_plot_url,
                               plot_url4=intervention_emissions_plot_url,
                               co2_value=co2_val, ch4_value=ch4_val, n2o_value=n2o_val,
                               co2_capture=co2_capture, tch4_per_yr=tch4_per_yr,
                               scenario=scenario, intervention_start=intervention_start,
                               agtp_net_plot=agtp_net_plot, co2e_plot=co2e_plot,
                               metric=metric)

# Run the Flask app
if __name__ == '__main__':
    app.run(debug=True)