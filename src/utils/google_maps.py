import requests
from rapidfuzz import fuzz
from config import settings

TYPE_TO_CATEGORY = {
    # Automotive
    "car_dealer": "Automotive",
    "car_rental": "Automotive",
    "car_repair": "Automotive",
    "car_wash": "Automotive",
    "electric_vehicle_charging_station": "Automotive",
    "gas_station": "Automotive",
    "parking": "Automotive",
    "rest_stop": "Automotive",

    # Business
    "corporate_office": "Business",
    "farm": "Business",
    "ranch": "Business",

    # Culture
    "art_gallery": "Culture",
    "art_studio": "Culture",
    "auditorium": "Culture",
    "cultural_landmark": "Culture",
    "historical_place": "Culture",
    "monument": "Culture",
    "museum": "Culture",
    "performing_arts_theater": "Culture",
    "sculpture": "Culture",

    # Education
    "library": "Education",
    "preschool": "Education",
    "primary_school": "Education",
    "school": "Education",
    "secondary_school": "Education",
    "university": "Education",

    # Food and Drink
    "acai_shop": "Food and Drink",
    "afghan_restaurant": "Food and Drink",
    "african_restaurant": "Food and Drink",
    "american_restaurant": "Food and Drink",
    "asian_restaurant": "Food and Drink",
    "bagel_shop": "Food and Drink",
    "bakery": "Food and Drink",
    "bar": "Food and Drink",
    "bar_and_grill": "Food and Drink",
    "barbecue_restaurant": "Food and Drink",
    "brazilian_restaurant": "Food and Drink",
    "breakfast_restaurant": "Food and Drink",
    "brunch_restaurant": "Food and Drink",
    "buffet_restaurant": "Food and Drink",
    "cafe": "Food and Drink",
    "cafeteria": "Food and Drink",
    "candy_store": "Food and Drink",
    "cat_cafe": "Food and Drink",
    "chinese_restaurant": "Food and Drink",
    "chocolate_factory": "Food and Drink",
    "chocolate_shop": "Food and Drink",
    "coffee_shop": "Food and Drink",
    "confectionery": "Food and Drink",
    "deli": "Food and Drink",
    "dessert_restaurant": "Food and Drink",
    "dessert_shop": "Food and Drink",
    "diner": "Food and Drink",
    "dog_cafe": "Food and Drink",
    "donut_shop": "Food and Drink",
    "fast_food_restaurant": "Food and Drink",
    "fine_dining_restaurant": "Food and Drink",
    "food_court": "Food and Drink",
    "french_restaurant": "Food and Drink",
    "greek_restaurant": "Food and Drink",
    "hamburger_restaurant": "Food and Drink",
    "ice_cream_shop": "Food and Drink",
    "indian_restaurant": "Food and Drink",
    "indonesian_restaurant": "Food and Drink",
    "italian_restaurant": "Food and Drink",
    "japanese_restaurant": "Food and Drink",
    "juice_shop": "Food and Drink",
    "korean_restaurant": "Food and Drink",
    "lebanese_restaurant": "Food and Drink",
    "meal_delivery": "Food and Drink",
    "meal_takeaway": "Food and Drink",
    "mediterranean_restaurant": "Food and Drink",
    "mexican_restaurant": "Food and Drink",
    "middle_eastern_restaurant": "Food and Drink",
    "pizza_restaurant": "Food and Drink",
    "pub": "Food and Drink",
    "ramen_restaurant": "Food and Drink",
    "restaurant": "Food and Drink",
    "sandwich_shop": "Food and Drink",
    "seafood_restaurant": "Food and Drink",
    "spanish_restaurant": "Food and Drink",
    "steak_house": "Food and Drink",
    "sushi_restaurant": "Food and Drink",
    "tea_house": "Food and Drink",
    "thai_restaurant": "Food and Drink",
    "turkish_restaurant": "Food and Drink",
    "vegan_restaurant": "Food and Drink",
    "vegetarian_restaurant": "Food and Drink",
    "vietnamese_restaurant": "Food and Drink",
    "wine_bar": "Food and Drink",

    # Finance
    "accounting": "Finance",
    "atm": "Finance",
    "bank": "Finance",

    # Health and Wellness
    "chiropractor": "Health and Wellness",
    "dental_clinic": "Health and Wellness",
    "dentist": "Health and Wellness",
    "doctor": "Health and Wellness",
    "drugstore": "Health and Wellness",
    "hospital": "Health and Wellness",
    "massage": "Health and Wellness",
    "medical_lab": "Health and Wellness",
    "pharmacy": "Health and Wellness",
    "physiotherapist": "Health and Wellness",
    "sauna": "Health and Wellness",
    "skin_care_clinic": "Health and Wellness",
    "spa": "Health and Wellness",
    "tanning_studio": "Health and Wellness",
    "wellness_center": "Health and Wellness",
    "yoga_studio": "Health and Wellness",

    # Lodging
    "hotel": "Lodging",
    "hostel": "Lodging",
    "resort_hotel": "Lodging",

    # Shopping
    "asian_grocery_store": "Shopping",
    "auto_parts_store": "Shopping",
    "bicycle_store": "Shopping",
    "book_store": "Shopping",
    "butcher_shop": "Shopping",
    "cell_phone_store": "Shopping",
    "clothing_store": "Shopping",
    "convenience_store": "Shopping",
    "department_store": "Shopping",
    "discount_store": "Shopping",
    "electronics_store": "Shopping",
    "food_store": "Shopping",
    "furniture_store": "Shopping",
    "gift_shop": "Shopping",
    "grocery_store": "Shopping",
    "hardware_store": "Shopping",
    "home_goods_store": "Shopping",
    "home_improvement_store": "Shopping",
    "jewelry_store": "Shopping",
    "liquor_store": "Shopping",
    "market": "Shopping",
    "pet_store": "Shopping",
    "shoe_store": "Shopping",
    "shopping_mall": "Shopping",
    "sporting_goods_store": "Shopping",
    "store": "Shopping",
    "supermarket": "Shopping",
    "warehouse_store": "Shopping",
    "wholesaler": "Shopping",
}

import logging

logger = logging.getLogger(__name__)

def query_google_places(merchant, city):
    """Execute text search on Google Places API."""
    if not settings.GOOGLE_PLACES_API_KEY:
        return None
        
    query = f"{merchant} {city}"
    url = "https://maps.googleapis.com/maps/api/place/textsearch/json"
    params = {
        "query": query,
        "key": settings.GOOGLE_PLACES_API_KEY
    }
    try:
        response = requests.get(url, params=params)
        response.raise_for_status()
        data = response.json()
        if data.get("results"):
            return data["results"][0]
    except Exception as e:
        logger.error(f"Error querying Google Places for {merchant}: {e}")
    return None

def score_match(merchant, result, city):
    """Calculate matching score for better categorization accuracy."""
    score = 0
    if fuzz.partial_ratio(merchant.lower(), result["name"].lower()) > 80:
        score += 40
    if city.lower() in result["formatted_address"].lower():
        score += 30
    if result.get("types") and result["types"][0] in TYPE_TO_CATEGORY:
        score += 20
    if len(result["formatted_address"].split(",")) > 3:
        score += 10
    return score

def map_types_to_category(types):
    """Map Google Places types list to defined high-level categories."""
    for t in types:
        if t in TYPE_TO_CATEGORY:
            return TYPE_TO_CATEGORY[t]
    return "Uncategorized"
