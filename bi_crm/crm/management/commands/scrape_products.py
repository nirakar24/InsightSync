import http.client
import json
import re

from django.core.management.base import BaseCommand
from django.utils import timezone
from crm.models import Product

# List of ASINs to process
ASIN_LIST = [
    'B09RGJCVW6'
]

def parse_decimal_value(value):
    """
    Parses a string to a float after removing commas and extraneous characters.
    Returns None if conversion fails.
    """
    if value is None:
        return None
    # Remove any non-digit characters except for '.' and '-' (to allow for decimals and negative numbers)
    cleaned = re.sub(r"[^\d\.\-]", "", value)
    try:
        return float(cleaned)
    except Exception as e:
        return None

def scrape_and_store_products(asins):
    API_HOST = "real-time-amazon-data.p.rapidapi.com"
    API_KEY = "9fa072cae9msh01977b14300cdcep12c7abjsnb055998d42ca"
    headers = {
        'x-rapidapi-key': API_KEY,
        'x-rapidapi-host': API_HOST
    }

    for asin in asins:
        try:
            conn = http.client.HTTPSConnection(API_HOST)
            endpoint = f"/product-details?asin={asin}&country=IN"
            conn.request("GET", endpoint, headers=headers)
            res = conn.getresponse()
            data = res.read()
            json_data = json.loads(data.decode("utf-8"))

            if json_data.get("status") == "OK":
                product_data = json_data.get("data", {})

                # Use parse_decimal_value to clean up the price strings.
                product_price = parse_decimal_value(product_data.get("product_price"))
                original_price = parse_decimal_value(product_data.get("product_original_price"))

                # Update or create product record using the scraped data.
                product, created = Product.objects.update_or_create(
                    asin=product_data.get("asin"),
                    defaults={
                        "name": product_data.get("product_title"),
                        "category": product_data.get("category", ""),
                        "price": product_price,
                        "original_price": product_data.get("product_original_price"),  # Keeping original text if needed
                        "currency": product_data.get("currency"),
                        "country": product_data.get("country"),
                        "description": product_data.get("product_description"),
                        "product_byline": product_data.get("product_byline"),
                        "product_byline_link": product_data.get("product_byline_link"),
                        "rating": float(product_data.get("product_star_rating", 0)) if product_data.get("product_star_rating") else None,
                        "product_num_ratings": product_data.get("product_num_ratings"),
                        "product_url": product_data.get("product_url"),
                        "product_photo": product_data.get("product_photo"),
                        "product_num_offers": product_data.get("product_num_offers"),
                        "product_availability": product_data.get("product_availability"),
                        "is_best_seller": product_data.get("is_best_seller", False),
                        "is_amazon_choice": product_data.get("is_amazon_choice", False),
                        "is_prime": product_data.get("is_prime", False),
                        "climate_pledge_friendly": product_data.get("climate_pledge_friendly", False),
                        "sales_volume": product_data.get("sales_volume"),
                        "customers_say": product_data.get("customers_say"),
                        "product_information": product_data.get("product_information"),
                        "product_details": product_data.get("product_details") or {},
                        "product_photos": product_data.get("product_photos"),
                        "product_videos": product_data.get("product_videos"),
                        "video_thumbnail": product_data.get("video_thumbnail"),
                        "has_video": product_data.get("has_video", False),
                        "delivery": product_data.get("delivery"),
                        "primary_delivery_time": product_data.get("primary_delivery_time"),
                        "category_path": product_data.get("category_path"),
                        "product_variations": product_data.get("product_variations"),
                        "deal_badge": product_data.get("deal_badge"),
                        "has_aplus": product_data.get("has_aplus", False),
                        "has_brandstory": product_data.get("has_brandstory", False),
                        "more_info": product_data.get("more_info")
                    }
                )
                self_msg = f"Product {asin} stored. Created: {created}"
                print(self_msg)
            else:
                print(f"Failed to fetch data for ASIN: {asin}. Response: {json_data}")
        except Exception as e:
            print(f"Error processing ASIN {asin}: {str(e)}")

class Command(BaseCommand):
    help = "Scrapes product data for a list of ASINs and stores/updates Product records."

    def handle(self, *args, **options):
        self.stdout.write("Starting product scraping for ASINs...")
        scrape_and_store_products(ASIN_LIST)
        self.stdout.write(self.style.SUCCESS("Product scraping completed."))
