from django.contrib import admin
from .models import (
    CustomerSegment, Customer, Product, PriceHistory, 
    Order, OrderItem, Review, ChurnPrediction, SalesForecast
)

# --------------------------
# Custom Admin Configurations
# --------------------------

@admin.register(Customer)
class CustomerAdmin(admin.ModelAdmin):
    list_display = ('first_name', 'last_name', 'email', 'segment', 'churn_score', 'last_purchase_date')
    search_fields = ('first_name', 'last_name', 'email')
    list_filter = ('segment',)
    ordering = ('-last_purchase_date',)

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'category', 'price', 'rating', 'inventory')
    search_fields = ('name', 'category')
    list_filter = ('category',)
    ordering = ('-price',)

@admin.register(PriceHistory)
class PriceHistoryAdmin(admin.ModelAdmin):
    list_display = ('product', 'platform', 'price', 'scraped_date')
    list_filter = ('platform', 'product')
    ordering = ('-scraped_date',)

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('order_number', 'customer', 'order_date', 'total_amount', 'status')
    list_filter = ('status',)
    search_fields = ('order_number', 'customer__first_name', 'customer__last_name')
    ordering = ('-order_date',)

@admin.register(OrderItem)
class OrderItemAdmin(admin.ModelAdmin):
    list_display = ('order', 'product', 'quantity', 'price_at_purchase')
    search_fields = ('order__order_number', 'product__name')
    ordering = ('order',)

@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ('customer', 'product', 'rating', 'sentiment_score', 'review_date')
    search_fields = ('customer__first_name', 'customer__last_name', 'product__name')
    list_filter = ('rating',)
    ordering = ('-review_date',)

@admin.register(ChurnPrediction)
class ChurnPredictionAdmin(admin.ModelAdmin):
    list_display = ('customer', 'churn_probability', 'prediction_date')
    search_fields = ('customer__first_name', 'customer__last_name')
    ordering = ('-prediction_date',)

@admin.register(SalesForecast)
class SalesForecastAdmin(admin.ModelAdmin):
    list_display = ('forecast_date', 'predicted_sales', 'period', 'created_at')
    list_filter = ('period',)
    ordering = ('-forecast_date',)

# --------------------------
# Register Simple Models
# --------------------------
admin.site.register(CustomerSegment)
