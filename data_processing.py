import pandas as pd

def preprocess_historical_data(historical_data):
    """
    Preprocess historical data to ensure correctness and consistency.
    Args:
        historical_data: A pandas DataFrame with columns like 'Year', 'Revenue', 'EBIT Margin', etc.
    Returns:
        A cleaned and scaled DataFrame.
    """
    # Ensure numeric columns
    historical_data["Year"] = pd.to_numeric(historical_data["Year"], errors="coerce")
    numerical_columns = [col for col in historical_data.columns if col != "Year"]

    for col in numerical_columns:
        historical_data[col] = pd.to_numeric(historical_data[col], errors="coerce")

    return historical_data

