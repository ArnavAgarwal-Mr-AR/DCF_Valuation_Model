def calculate_dcf(projected_data, WACC, growth_rate):
    """
    Calculate DCF based on forecasted data.
    Args:
        projected_: A pandas DataFrame with forecasted financial parameters.
        WACC: Weighted Average Cost of Capital (decimal, e.g., 0.12 for 12%).
        growth_rate: Terminal growth rate (decimal, e.g., 0.03 for 3%).
    Returns:
        A dictionary with DCF calculations, including present value of FCF and terminal value.
    """
    # Ensure WACC > growth_rate
    if WACC <= growth_rate:
        raise ValueError("WACC must be greater than the growth rate to calculate terminal value.")

    # Ensure no NaN or invalid FCF values
    if projected_data["FCF"].isna().any() or (projected_data["FCF"] <= 0).all():
        raise ValueError("Invalid or negative FCF values detected. Check your input data.")

    # Calculate Terminal Value
    last_year_fcf = projected_data["FCF"].iloc[-1]
    terminal_value = max((last_year_fcf * (1 + growth_rate)) / (WACC - growth_rate), 0)

    # Calculate Present Value of FCF
    projected_data["Discount Factor"] = [(1 / (1 + WACC)) ** i for i in range(1, len(projected_data) + 1)]
    projected_data["Discount Factor"] = round(projected_data["Discount Factor"], 2)
    projected_data["Present Value of FCF"] = projected_data["FCF"] * projected_data["Discount Factor"]
    projected_data["Present Value of FCF"] = round(projected_data["Present Value of FCF"], 2)
    terminal_value = terminal_value.round(2)
    # Debugging: Print terminal value
    print(f"Terminal Value: {terminal_value}")

    # Calculate Present Value of Terminal Value
    terminal_value_pv = terminal_value / ((1 + WACC) ** len(projected_data))
    terminal_value_pv = terminal_value_pv.round(2)
    # Debugging: Print present value of terminal value
    print(f"Present Value of Terminal Value: {terminal_value_pv}")

    # Sum all Present Values
    total_pv_fcf = projected_data["Present Value of FCF"].sum()
    enterprise_value = total_pv_fcf + terminal_value_pv
    enterprise_value = enterprise_value.round(2)

    return {
        "projected_data": projected_data,
        "terminal_value": terminal_value,
        "terminal_value_pv": terminal_value_pv,
        "enterprise_value": enterprise_value,
    }
