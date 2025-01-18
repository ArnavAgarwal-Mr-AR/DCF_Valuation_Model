import streamlit as st
import pandas as pd
from data_processing import preprocess_historical_data
from forecasting import financial_projection_with_model
from dcf_calculation import calculate_dcf
from monte import plot_monte_simulations
from report_generator import generate_report
from matplotlib import pyplot as plt
import numpy as np

st.title("DCF Valuation Model with Monte Carlo Simulation")

# Step 1: General Inputs
st.header("Step 1: Enter General Inputs")
ticker = st.text_input("Enter Stock Ticker:")
wacc = round(st.number_input("Enter WACC (in %):", min_value=0.0, step=0.1) / 100, 2)
terminal_growth_rate = round(st.number_input("Enter Terminal Growth Rate (in %):", min_value=0.0, step=0.1) / 100, 2)
current_share_price = st.number_input("Enter Current Share Price:", min_value=0.0, step=0.1)
shares_outstanding = st.number_input("Enter Total Number of Shares Outstanding:", min_value=1, step=1)
rroi = round(st.number_input("Enter Required ROI (in %):", min_value=0.0, step=0.1) /100, 2)
# Convert general data to DataFrame
general_data = {
    "Ticker": ticker,
    "WACC": wacc,
    "Terminal Growth Rate": terminal_growth_rate,
    "Current Share Price": current_share_price,
    "Shares Outstanding": shares_outstanding,
    "Required ROI": rroi
}

# Step 2: Historical Data Inputs
st.header("Step 2: Enter Historical Data for 3 years")
years = 3

historical_data = []
for i in range(years):
    st.subheader(f"Year {i + 1}")
    year = st.text_input(f"Enter Year for Data Point {i + 1}:", key=f"year_{i}")
    revenue = st.number_input(f"Enter Revenue for {year}:", min_value=0.0, step=1.0, key=f"revenue_{i}")
    ebit_margin = st.number_input(f"Enter EBIT Margin (in %) for {year}:", min_value=0.0, key=f"ebit_{i}")
    d_and_a = st.number_input(f"Enter Depreciation & Amortization for {year}:", step=1.0, key=f"da_{i}")
    capex = st.number_input(f"Enter CapEx for {year}:", min_value=0.0, step=1.0, key=f"capex_{i}")
    wc_change = st.number_input(f"Enter Change in Working Capital for {year}:", step=1.0, key=f"wc_{i}")
    tax_rate = st.number_input(f"Enter Tax Rate (in %) for {year}:", min_value=0.0, step=1.0, key=f"tax_{i}") 
    historical_data.append([year, revenue, ebit_margin, d_and_a, capex, wc_change, tax_rate])

# Convert historical data to DataFrame
historical_df = pd.DataFrame(
    historical_data,
    columns=["Year", "Revenue", "EBIT Margin", "D&A", "CapEx", "WC Change", "Tax Rate"]
)

if st.button("Process Data"):
    try:
        historical_df = preprocess_historical_data(historical_df)
        st.success("Historical Data Processed Successfully!")

        # Save the processed historical data to Streamlit session state
        st.session_state["historical_df"] = historical_df
    except Exception as e:
        st.error(f"An error occurred during data processing: {e}")

# Step 3: Projecting Financial Parameters
if "historical_df" in st.session_state:
    st.header("Step 3: Project Financial Parameters for 10 Years")
    # Retrieve historical data from session state
    historical_df = st.session_state["historical_df"]
    # Perform projections
    if st.button("Project Financials"):
        #try:
            projected_data = financial_projection_with_model(historical_df, years=10)
            
            # Save projections to session state
            st.session_state["projected_data"] = projected_data
            
            # Display projections
            st.write("Projected Financial Parameters for the Next 10 Years:")
            st.dataframe(projected_data.reset_index(drop=True))

        #except Exception as e:
            #st.error(f"An error occurred during projection: {e}")


# Step 4: DCF Calculations
if "projected_data" in st.session_state:
    st.header("Step 4: DCF Calculations")
    
    if st.button("Calculate DCF"):
        try:
            projected_data = st.session_state["projected_data"]
            # Perform DCF calculation
            dcf_results = calculate_dcf(projected_data, wacc, terminal_growth_rate)
            # Save dcf result to session state
            st.session_state["dcf_results"] = dcf_results
            # Display results
            st.write("Discounted Cash Flow Analysis")
            st.write(dcf_results["projected_data"])
            st.metric("Enterprise Value (₹)", dcf_results["enterprise_value"])
            st.metric("Terminal Value (₹)", dcf_results["terminal_value"])
                
        except ValueError as e:
            st.warning(f"DCF Calculation Warning: {e}")
        except Exception as e:
            st.error(f"An unexpected error occurred during DCF calculations: {e}")

# Step 5: Monte Carlo simulations
if "dcf_results" in st.session_state:
    st.header("Step 5: Monte Carlo simulations")
    
    if st.button("Monte Carlo Simulation"):
        try:
            dcf_results = st.session_state["dcf_results"]
            projected_data = st.session_state["projected_data"]
            present_values = plot_monte_simulations(projected_data["FCF"][2],rroi, terminal_growth_rate)
            company_value = np.mean(present_values)
            company_value = round(company_value, 2)
            st.session_state["company_value"] = company_value
            st.metric("Terminal Value (₹)", dcf_results["terminal_value"])
            st.metric("Present Value (₹)", company_value)
            fig, ax = plt.subplots(figsize=(12, 8))
            plt.style.use('bmh')
            ax.hist(present_values, bins=50, alpha=0.5, color='blue', edgecolor='black')
            # Add a title and axis labels
            ax.set_title("Distribution of the company value")
            ax.set_xlabel("Value in ₹")
            ax.set_ylabel("Frequency")
            st.pyplot(fig)
            plt.savefig('fig.png')
        except Exception as e:
            st.warning(f"Monte Carlo simulation Warning: {e}")
            st.error(f"An unexpected error occurred during simulations: {e}")

# Step 6: Generate Report
if st.button("Generate Report"):
    dcf_results = st.session_state["dcf_results"]
    historical_df = st.session_state["historical_df"]
    projected_data = st.session_state["projected_data"]
    projected_data["DF"] = projected_data["Discount Factor"]
    projected_data["PFCF"] = projected_data["Present Value of FCF"] 
    projected_data.drop(columns=["Discount Factor", "Present Value of FCF"], inplace=True)
    company_value = st.session_state["company_value"]
    del dcf_results["projected_data"]    # Deleting the projected row column from dictionary
    dcf_results["Terminal Value of Stock"] = dcf_results["terminal_value"]
    dcf_results["Present Value of Terminal Value"] = dcf_results["terminal_value_pv"]
    dcf_results["Enterprise Value of Stock"] = dcf_results["enterprise_value"]
    dcf_results["Company Value"] = company_value
    del dcf_results["terminal_value"]
    del dcf_results["terminal_value_pv"]
    del dcf_results["enterprise_value"]
    # Generate Report
    generated_report = generate_report(general_data, historical_df, projected_data, dcf_results)    
    st.download_button(
        label="Download Report",
        data=generated_report,
        file_name="Financial_report.pdf",
        mime="application/pdf"
    )
    st.success("Report generated successfully! Use the button above to download.")
    