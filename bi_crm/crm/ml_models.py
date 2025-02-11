import random
from datetime import datetime, timedelta
import numpy as np
import pandas as pd
from django.utils.timezone import now
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.preprocessing import StandardScaler
from .models import Customer

# --------------------------
# Generate Initial Churn Scores
# --------------------------
def generate_initial_churn_scores():
    """
    Assigns an initial churn score to customers based on their behavior.
    This is used to bootstrap the model before real predictions.
    """
    customers = Customer.objects.all()

    for customer in customers:
        tenure = (now().date() - customer.registration_date).days
        last_purchase_gap = (now().date() - customer.last_purchase_date).days if customer.last_purchase_date else 365
        spending_factor = customer.spending_factor  # Simulate spending influence
        churn_score = min(1, max(0, (last_purchase_gap / (tenure + 1)) * float(spending_factor)))


        # Update churn score in database
        customer.churn_score = round(churn_score, 2)
        customer.save()

    print("✅ Initial churn scores assigned to customers.")

def train_churn_model():
    """
    Trains a Logistic Regression model using real customer churn data.
    """
    df = pd.DataFrame(list(Customer.objects.values("id", "registration_date", "last_purchase_date", "churn_score")))

    if df.empty or len(df) < 10:
        print("⚠️ Not enough customer data to train the model.")
        return None, None

    # Convert date fields to datetime, coercing errors to NaT
    df["registration_date"] = pd.to_datetime(df["registration_date"], errors="coerce")
    df["last_purchase_date"] = pd.to_datetime(df["last_purchase_date"], errors="coerce")

    # Convert now() to a timezone-naive datetime by removing tzinfo
    now_naive = now().replace(tzinfo=None)

    # Compute tenure (days since registration)
    df["tenure"] = (pd.Timestamp(now_naive) - df["registration_date"]).dt.days

    # Compute last purchase gap (days since last purchase)
    df["last_purchase_gap"] = (pd.Timestamp(now_naive) - df["last_purchase_date"]).dt.days
    df["last_purchase_gap"].fillna(365, inplace=True)
    df["last_purchase_gap"] = df["last_purchase_gap"].astype(int)

    # Encode churn as 0 (low risk) and 1 (high risk)
    df["churn"] = df["churn_score"].apply(lambda x: 1 if x and x > 0.5 else 0)

    X = df[["tenure", "last_purchase_gap"]]
    y = df["churn"]

    # Train/Test Split
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    # Scale Data
    scaler = StandardScaler()
    X_train_scaled = scaler.fit_transform(X_train)
    X_test_scaled = scaler.transform(X_test)

    # Train Logistic Regression Model
    model = LogisticRegression()
    model.fit(X_train_scaled, y_train)

    print("✅ Churn model trained successfully.")
    return model, scaler

# Train the model initially
churn_model, churn_scaler = train_churn_model()



def predict_and_update_churn():
    """
    Predicts churn probability for all customers and updates their churn score.
    """
    customers = Customer.objects.all()

    for customer in customers:
        tenure = (now().date() - customer.registration_date).days
        last_purchase_gap = (now().date() - customer.last_purchase_date).days if customer.last_purchase_date else 365

        features_array = np.array([[tenure, last_purchase_gap]])
        features_scaled = churn_scaler.transform(features_array)

        # Predict Churn Probability
        churn_probability = churn_model.predict_proba(features_scaled)[0][1]

        # Update Churn Score
        customer.churn_score = round(churn_probability, 2)
        customer.save()

    print("✅ Updated churn scores for all customers.")


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
