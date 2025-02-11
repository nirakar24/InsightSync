import random
from datetime import datetime, timedelta

# --------------------------
# Churn Prediction Model (Placeholder)
# --------------------------
def predict_churn(customer_id):
    """
    Returns a random churn probability between 0 and 1 for a given customer.
    """
    return round(random.uniform(0.1, 0.9), 2)

# --------------------------
# Sales Forecasting Model (Placeholder)
# --------------------------
def forecast_sales():
    """
    Returns a random predicted sales figure for the next period.
    """
    predicted_sales = round(random.uniform(5000, 20000), 2)
    return {
        "date": (datetime.now() + timedelta(days=7)).strftime("%Y-%m-%d"),
        "predicted_sales": predicted_sales
    }

# --------------------------
# Product Recommendation Model (Placeholder)
# --------------------------
def recommend_products(customer_id):
    """
    Returns a list of randomly recommended product names.
    """
    products = ["Smartphone", "Laptop", "Headphones", "Shoes", "Backpack", "T-Shirt", "Wristwatch"]
    recommended = random.sample(products, 3)  # Pick 3 random products
    return recommended

# --------------------------
# Dynamic Pricing Insights (Placeholder)
# --------------------------
def get_pricing_trends(product_id):
    """
    Simulates pricing trends for a given product.
    """
    base_price = round(random.uniform(100, 500), 2)
    trend = [round(base_price * random.uniform(0.9, 1.1), 2) for _ in range(5)]
    return {
        "product_id": product_id,
        "price_trends": trend,
        "suggested_price": round(sum(trend) / len(trend), 2)
    }
