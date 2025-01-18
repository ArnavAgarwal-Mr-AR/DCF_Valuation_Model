import pandas as pd
from sklearn.linear_model import LinearRegression
import numpy as np

def financial_projection_with_model(historical_data, years):
    """
    Generate financial projections using a simple regression model based on historical data.

    Parameters:
    - historical_data (dict): Dictionary containing historical financial data.
    - years (int): Number of years to project (default is 10).

    Returns:
    - pd.DataFrame: DataFrame containing the financial projections.
    """
    # Prepare historical data for regression
    historical_years = np.array(historical_data["Year"]).reshape(-1, 1)
    revenue = np.array(historical_data["Revenue"])
    
    # Fit linear regression model for revenue
    revenue_model = LinearRegression()
    revenue_model.fit(historical_years, revenue)

    # Predict future years
    last_year = historical_data["Year"][2]
    future_years = np.arange(last_year + 1, last_year + years + 1).reshape(-1, 1)
    projected_revenue = revenue_model.predict(future_years)

    # Extract other ratios
    ebit_margin = np.mean(historical_data["EBIT Margin"]) / 100
    depreciation_percent = np.mean(np.array(historical_data["D&A"]) / np.array(historical_data["Revenue"]))
    capex_percent = np.mean(np.array(historical_data["CapEx"]) / np.array(historical_data["Revenue"]))
    wc_percent = np.mean(np.array(historical_data["WC Change"]) / np.array(historical_data["Revenue"]))
    tax_rate = np.mean(historical_data["Tax Rate"]) / 100

    # Initialize the projections DataFrame
    projections = {
        "Year": [],
        "Revenue": [],
        "EBIT": [],
        "NOPAT": [],
        "D&A": [],
        "CapEx": [],
        "WC Change": [],
        "FCF": []
    }

    # Generate projections for each future year
    for i, revenue in enumerate(projected_revenue):
        year = future_years[i][0]
        ebit = revenue * ebit_margin
        nopat = ebit * (1 - tax_rate)
        depreciation = revenue * depreciation_percent
        capex = revenue * capex_percent
        wc_change = revenue * wc_percent
        free_cash_flow = nopat + depreciation - capex - wc_change

        # Append values to projections
        projections["Year"].append(year)
        projections["Revenue"].append(revenue)
        projections["EBIT"].append(ebit)
        projections["NOPAT"].append(nopat)
        projections["D&A"].append(depreciation)
        projections["CapEx"].append(capex)
        projections["WC Change"].append(wc_change)
        projections["FCF"].append(free_cash_flow)

    projections["Year"] = [int(year) for year in projections["Year"]]
    projections["Revenue"] = [round(revenue, 2) for revenue in projections["Revenue"]]
    projections["EBIT"] = [round(ebit, 2) for ebit in projections["EBIT"]]
    projections["NOPAT"] = [round(nopat, 2) for nopat in projections["NOPAT"]]
    projections["D&A"] = [round(depreciation, 2) for depreciation in projections["D&A"]]
    projections["CapEx"] = [round(capex, 2) for capex in projections["CapEx"]]
    projections["WC Change"] = [round(wc_change, 2) for wc_change in projections["WC Change"]]
    projections["FCF"] = [round(free_cash_flow, 2) for free_cash_flow in projections["FCF"]]
    return pd.DataFrame(projections)



