from django.db import models

# -----------------------------
# Customer & Segmentation
# -----------------------------
class CustomerSegment(models.Model):
    """
    Represents a customer segment (e.g., High Value, Medium Value, Low Value)
    that can be used for targeted marketing and segmentation analysis.
    """
    name = models.CharField(max_length=50)
    description = models.TextField(blank=True, null=True)
    
    def __str__(self):
        return self.name

class Customer(models.Model):
    """
    Stores customer details along with engagement data used for churn prediction,
    customer segmentation, and personalized recommendations.
    """
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=20, blank=True, null=True)
    registration_date = models.DateField(auto_now_add=True)
    last_purchase_date = models.DateField(blank=True, null=True)
    # A predicted churn score between 0 and 1 (can be updated via ML predictions)
    churn_score = models.DecimalField(max_digits=4, decimal_places=2, blank=True, null=True)
    # Link to a segmentation category
    segment = models.ForeignKey(CustomerSegment, on_delete=models.SET_NULL, blank=True, null=True, related_name='customers')
    
    def __str__(self):
        return f"{self.first_name} {self.last_name}"

# -----------------------------
# Product & Pricing
# -----------------------------
class Product(models.Model):
    """
    Represents a product available for sale. Used in product recommendations,
    sales analysis, and dynamic pricing insights.
    """
    name = models.CharField(max_length=100)
    category = models.CharField(max_length=50)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    description = models.TextField(blank=True, null=True)
    # Average rating computed from reviews
    rating = models.FloatField(blank=True, null=True)
    # Available inventory count
    inventory = models.PositiveIntegerField(default=0)
    
    def __str__(self):
        return self.name

class PriceHistory(models.Model):
    """
    Tracks historical pricing data from various e-commerce platforms.
    Useful for dynamic pricing insights and trend analysis.
    """
    PLATFORM_CHOICES = (
        ('Amazon', 'Amazon'),
        ('Flipkart', 'Flipkart'),
        ('Other', 'Other'),
    )
    
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='price_history')
    platform = models.CharField(max_length=20, choices=PLATFORM_CHOICES)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    scraped_date = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.product.name} on {self.platform} @ {self.price}"

# -----------------------------
# Orders & Order Items
# -----------------------------
class Order(models.Model):
    """
    Represents a customer order. Aggregates order items and records key sales data.
    """
    STATUS_CHOICES = (
        ('Pending', 'Pending'),
        ('Completed', 'Completed'),
        ('Cancelled', 'Cancelled'),
    )
    order_number = models.CharField(max_length=20, unique=True)
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, related_name='orders')
    order_date = models.DateTimeField(auto_now_add=True)
    total_amount = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='Pending')
    
    def __str__(self):
        return self.order_number

class OrderItem(models.Model):
    """
    An individual item within an order, linking products to a particular order.
    """
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='items')
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    # Price of the product at the time of purchase
    price_at_purchase = models.DecimalField(max_digits=10, decimal_places=2)
    
    def __str__(self):
        return f"{self.product.name} in {self.order.order_number}"

# -----------------------------
# Reviews & Sentiment
# -----------------------------
class Review(models.Model):
    """
    Customer reviews for products, including rating and sentiment analysis.
    """
    RATING_CHOICES = [(i, str(i)) for i in range(1, 6)]
    
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, related_name='reviews')
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='reviews')
    rating = models.PositiveSmallIntegerField(choices=RATING_CHOICES)
    comment = models.TextField(blank=True, null=True)
    review_date = models.DateTimeField(auto_now_add=True)
    # Optional: A computed sentiment score (e.g., from sentiment analysis on the comment)
    sentiment_score = models.DecimalField(max_digits=4, decimal_places=2, blank=True, null=True)
    
    def __str__(self):
        return f"Review by {self.customer} for {self.product}"

# -----------------------------
# ML Predictions & Forecasts
# -----------------------------
class ChurnPrediction(models.Model):
    """
    Stores the results of churn prediction models for a customer.
    """
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, related_name='churn_predictions')
    # Predicted churn probability (0 to 1)
    churn_probability = models.FloatField()
    prediction_date = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"Churn prediction for {self.customer} on {self.prediction_date}"

class SalesForecast(models.Model):
    """
    Records forecasted sales data over a given period.
    """
    forecast_date = models.DateField(help_text="Date for which the sales forecast applies")
    predicted_sales = models.DecimalField(max_digits=12, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)
    period = models.CharField(max_length=20, help_text="Forecast period (e.g., Daily, Weekly, Monthly)")
    
    def __str__(self):
        return f"Forecast for {self.forecast_date} ({self.period})"
