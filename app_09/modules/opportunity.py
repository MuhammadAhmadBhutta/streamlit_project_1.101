# modules/opportunity.py

import pandas as pd

def detect_opportunities(df: pd.DataFrame):
    """
    Example: Detect low-profit sub-categories for improvement.
    """
    profit_by_subcategory = df.groupby('Sub-Category')['Profit'].sum().sort_values()
    loss_making = profit_by_subcategory[profit_by_subcategory < 0]

    opportunities = ""
    if not loss_making.empty:
        opportunities += "⚠️ Loss-making sub-categories:\n"
        opportunities += loss_making.to_string()
    else:
        opportunities += "✅ All sub-categories are profitable!"

    high_sales_region = df.groupby('Region')['Sales'].sum().idxmax()
    opportunities += f"\n\n💡 Highest sales region: {high_sales_region}"

    return opportunities
