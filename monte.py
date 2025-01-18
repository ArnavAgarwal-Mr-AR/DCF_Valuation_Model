import numpy as np
import matplotlib.pyplot as plt


def plot_monte_simulations(initial_FCFE, required_rate_of_return, growth_FCFE):
    num_scenarios = 10000 # Set the number of scenarios to generate
    forecast_period = 10 # Set the forecast period (in years)
    # Generate a random sample of future FCFEs for each scenario
    std_growth_FCFE = 0.05 #set the volatility of your assumptions
    future_fcfe = initial_FCFE*(1+np.random.normal(growth_FCFE, std_growth_FCFE, size=(num_scenarios, forecast_period)))

    # Calculate the present value of the future cash flows for each scenario
    present_values = []
    for scenario in future_fcfe:
        present_value = 0
        for i, fcfe in enumerate(scenario):
        # Use the formula for discounted cash flow to calculate the present value
        # of the cash flow for each year: present value += future cash flow / (1 + required rate of return)^year
            present_value += fcfe / (1 + required_rate_of_return)**(i+1)
        present_values.append(present_value)
    return present_values
