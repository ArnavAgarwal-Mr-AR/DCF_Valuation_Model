from reportlab.lib.pagesizes import landscape, letter
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer, Image
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet
import pandas as pd
import os
import io

def dataframe_to_table(data, title, elements, styles, column_widths=None, font_size=10):
    """
    Add a table from data to the PDF with enhanced styles and customizable column widths and font size.

    Parameters:
        data (pd.DataFrame or dict): Data to include in the table.
        title (str): Title of the table.
        elements (list): List of PDF elements.
        styles (StyleSheet1): Style sheet for formatting.
        column_widths (list): List of column widths for the table.
        font_size (int): Font size for the table content.

    Returns:
        None
    """
    from reportlab.lib.pagesizes import letter
    page_width, _ = landscape(letter)  # Get the landscape page width

    # Check if the data is a dict and convert to DataFrame
    if isinstance(data, dict):
        data = pd.DataFrame(list(data.items()), columns=["Metric", "Value"])

    elements.append(Paragraph(title, styles['Heading2']))
    table_data = [list(data.columns)] + data.values.tolist()

    # Use provided column widths or calculate proportional widths
    if column_widths is None:
        num_columns = len(data.columns)
        column_widths = [page_width / num_columns] * num_columns

    # Create the table
    table = Table(table_data, hAlign='LEFT', colWidths=column_widths)
    table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.darkblue),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, 0), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, 0), font_size + 2),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 10),

        # Alternating row background colors
        ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
        ('TEXTCOLOR', (0, 1), (-1, -1), colors.black),
        ('GRID', (0, 0), (-1, -1), 1, colors.black),
        ('ALIGN', (0, 1), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 1), (-1, -1), 'Helvetica'),
        ('FONTSIZE', (0, 1), (-1, -1), font_size),
    ]))

    # Apply alternating row colors
    for i in range(1, len(table_data)):
        bg_color = colors.beige if i % 2 == 0 else colors.lightgrey
        table.setStyle(TableStyle([
            ('BACKGROUND', (0, i), (-1, i), bg_color)
        ]))
    elements.append(table)
    elements.append(Spacer(1, 12))

def generate_report(general_data, historical_data, forecast_data, dcf_data):
    """
    Generate a comprehensive PDF report using ReportLab in landscape mode with adjustable margins.

    Parameters:
        historical_data (pd.DataFrame): Historical financial data.
        forecast_data (pd.DataFrame): Forecasted financial data.
        dcf_data (pd.DataFrame or dict): DCF calculations.

    Returns:
        bytes: Generated PDF content.
    """
    buffer = io.BytesIO()
    doc = SimpleDocTemplate(
        buffer,
        pagesize=landscape(letter),
        leftMargin=35,  
        rightMargin=30,
        topMargin=30,
        bottomMargin=20,
        title="Financial Analysis Report"
    )
    elements = []
    styles = getSampleStyleSheet()

    # Title
    title = Paragraph("Financial Analysis Report For Your Asked Stock", styles['Title'])
    elements.append(title)
    elements.append(Spacer(1, 12))

    # Summary
    #summary = Paragraph(
    #    "This report includes financial projections, discounted cash flow analysis, and Monte Carlo simulations based on the provided data.",
    #    styles['BodyText']
    #)
    #elements.append(summary)
    #elements.append(Spacer(1, 12))

    #Adding general data to tables
    gen_column_widths = [120, 70]
    dataframe_to_table(general_data, "Ticker Data", elements, styles, column_widths=gen_column_widths, font_size=9)
    # Add Historical Data Table
    hist_column_widths = [60, 80, 80, 80, 60, 90, 80]
    dataframe_to_table(historical_data, "Historical Data", elements, styles, column_widths=hist_column_widths, font_size=9)

    # Add Forecasted Data Table with custom column widths
    forecast_column_widths = [60, 80, 80, 80, 60, 70, 80, 70, 50, 80]  # Example custom widths
    dataframe_to_table(forecast_data, "Forecasted Data", elements, styles, column_widths=forecast_column_widths, font_size=9)

    # Add DCF Calculations Table
    dcf_column_widths = [160, 120]  # Custom widths for DCF table
    dataframe_to_table(dcf_data, "DCF Calculations", elements, styles, column_widths=dcf_column_widths, font_size=9)

    # Monte Carlo Simulations Placeholder
    elements.append(Paragraph("Monte Carlo Simulations", styles['Heading2']))
    monte_carlo_image = "fig.png"  # Replace with the path to your chart image
    if os.path.exists(monte_carlo_image):
        img = Image(monte_carlo_image, width=400, height=300)
        elements.append(img)
    else:
        elements.append(Paragraph("Monte Carlo simulation image is not available.", styles['BodyText']))

    #elements.append(Spacer(1, 12))

    # Build the PDF
    doc.build(elements)

    # Retrieve binary content
    pdf_content = buffer.getvalue()
    buffer.close()

    return pdf_content