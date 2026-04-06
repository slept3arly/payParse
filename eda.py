import pandas as pd
import requests
from rapidfuzz import fuzz
import os

# === CONFIG ===
API_KEY = "AIzaSyB-tN7psn5qD3eSo4awVNxTfnWJBGwrqCM"
USER_CITY = "Vellore, Tamil Nadu"
CACHE_FILE = "Assets/merchant_cache.csv"
CONFIDENCE_THRESHOLD = 70

columns = [
    "merchant_name", "city", "place_id", "name",
    "formatted_address", "types", "confidence_score", "category"
]
pd.DataFrame(columns=columns).to_csv("Assets/merchant_cache.csv", index=False)


# === CATEGORY MAPPING ===
type_to_category = {
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

    # Geographical Areas
    "administrative_area_level_1": "Geographical Areas",
    "administrative_area_level_2": "Geographical Areas",
    "country": "Geographical Areas",
    "locality": "Geographical Areas",
    "postal_code": "Geographical Areas",
    "school_district": "Geographical Areas",

    # Government
    "city_hall": "Government",
    "courthouse": "Government",
    "embassy": "Government",
    "fire_station": "Government",
    "government_office": "Government",
    "local_government_office": "Government",
    "neighborhood_police_station": "Government", # (Japan only)
    "police": "Government",
    "post_office": "Government",

    # Entertainment and Recreation
    "adventure_sports_center": "Entertainment and Recreation",
    "amphitheatre": "Entertainment and Recreation",
    "amusement_center": "Entertainment and Recreation",
    "amusement_park": "Entertainment and Recreation",
    "aquarium": "Entertainment and Recreation",
    "banquet_hall": "Entertainment and Recreation",
    "barbecue_area": "Entertainment and Recreation",
    "botanical_garden": "Entertainment and Recreation",
    "bowling_alley": "Entertainment and Recreation",
    "casino": "Entertainment and Recreation",
    "childrens_camp": "Entertainment and Recreation",
    "comedy_club": "Entertainment and Recreation",
    "community_center": "Entertainment and Recreation",
    "concert_hall": "Entertainment and Recreation",
    "convention_center": "Entertainment and Recreation",
    "cultural_center": "Entertainment and Recreation",
    "cycling_park": "Entertainment and Recreation",
    "dance_hall": "Entertainment and Recreation",
    "dog_park": "Entertainment and Recreation",
    "event_venue": "Entertainment and Recreation",
    "ferris_wheel": "Entertainment and Recreation",
    "garden": "Entertainment and Recreation",
    "hiking_area": "Entertainment and Recreation",
    "historical_landmark": "Entertainment and Recreation",
    "internet_cafe": "Entertainment and Recreation",
    "karaoke": "Entertainment and Recreation",
    "marina": "Entertainment and Recreation",
    "movie_rental": "Entertainment and Recreation",
    "movie_theater": "Entertainment and Recreation",
    "national_park": "Entertainment and Recreation",
    "night_club": "Entertainment and Recreation",
    "observation_deck": "Entertainment and Recreation",
    "off_roading_area": "Entertainment and Recreation",
    "opera_house": "Entertainment and Recreation",
    "park": "Entertainment and Recreation",
    "philharmonic_hall": "Entertainment and Recreation",
    "picnic_ground": "Entertainment and Recreation",
    "planetarium": "Entertainment and Recreation",
    "plaza": "Entertainment and Recreation",
    "roller_coaster": "Entertainment and Recreation",
    "skateboard_park": "Entertainment and Recreation",
    "state_park": "Entertainment and Recreation",
    "tourist_attraction": "Entertainment and Recreation",
    "video_arcade": "Entertainment and Recreation",
    "visitor_center": "Entertainment and Recreation",
    "water_park": "Entertainment and Recreation",
    "wedding_venue": "Entertainment and Recreation",
    "wildlife_park": "Entertainment and Recreation",
    "wildlife_refuge": "Entertainment and Recreation",
    "zoo": "Entertainment and Recreation",

    # Facilities
    "public_bath": "Facilities",
    "public_bathroom": "Facilities",
    "stable": "Facilities",

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

    # Housing
    "apartment_building": "Housing",
    "apartment_complex": "Housing",
    "condominium_complex": "Housing",
    "housing_complex": "Housing",

    # Lodging
    "bed_and_breakfast": "Lodging",
    "budget_japanese_inn": "Lodging",
    "campground": "Lodging",
    "camping_cabin": "Lodging",
    "cottage": "Lodging",
    "extended_stay_hotel": "Lodging",
    "farmstay": "Lodging",
    "guest_house": "Lodging",
    "hostel": "Lodging",
    "hotel": "Lodging",
    "inn": "Lodging",
    "japanese_inn": "Lodging",
    "lodging": "Lodging",
    "mobile_home_park": "Lodging",
    "motel": "Lodging",
    "private_guest_room": "Lodging",
    "resort_hotel": "Lodging",
    "rv_park": "Lodging",

    # Natural Features
    "beach": "Natural Features",

    # Places of Worship
    "church": "Places of Worship",
    "hindu_temple": "Places of Worship",
    "mosque": "Places of Worship",
    "synagogue": "Places of Worship",

    # Services
    "astrologer": "Services",
    "barber_shop": "Services",
    "beautician": "Services",
    "beauty_salon": "Services",
    "body_art_service": "Services",
    "catering_service": "Services",
    "cemetery": "Services",
    "child_care_agency": "Services",
    "consultant": "Services",
    "courier_service": "Services",
    "electrician": "Services",
    "florist": "Services",
    "food_delivery": "Services",
    "foot_care": "Services",
    "funeral_home": "Services",
    "hair_care": "Services",
    "hair_salon": "Services",
    "insurance_agency": "Services",
    "laundry": "Services",
    "lawyer": "Services",
    "locksmith": "Services",
    "makeup_artist": "Services",
    "moving_company": "Services",
    "nail_salon": "Services",
    "painter": "Services",
    "plumber": "Services",
    "psychic": "Services",
    "real_estate_agency": "Services",
    "roofing_contractor": "Services",
    "storage": "Services",
    "summer_camp_organizer": "Services",
    "tailor": "Services",
    "telecommunications_service_provider": "Services",
    "tour_agency": "Services",
    "tourist_information_center": "Services",
    "travel_agency": "Services",
    "veterinary_care": "Services",

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

    # Sports
    "arena": "Sports",
    "athletic_field": "Sports",
    "fishing_charter": "Sports",
    "fishing_pond": "Sports",
    "fitness_center": "Sports",
    "golf_course": "Sports",
    "gym": "Sports",
    "ice_skating_rink": "Sports",
    "playground": "Sports",
    "ski_resort": "Sports",
    "sports_activity_location": "Sports",
    "sports_club": "Sports",
    "sports_coaching": "Sports",
    "sports_complex": "Sports",
    "stadium": "Sports",
    "swimming_pool": "Sports",

    # Transportation
    "airport": "Transportation",
    "airstrip": "Transportation",
    "bus_station": "Transportation",
    "bus_stop": "Transportation",
    "ferry_terminal": "Transportation",
    "heliport": "Transportation",
    "international_airport": "Transportation",
    "light_rail_station": "Transportation",
    "park_and_ride": "Transportation",
    "subway_station": "Transportation",
    "taxi_stand": "Transportation",
    "train_station": "Transportation",
    "transit_depot": "Transportation",
    "transit_station": "Transportation",
    "truck_stop": "Transportation"
}

# === LOAD CACHE ===
if os.path.exists(CACHE_FILE):
    cache_df = pd.read_csv(CACHE_FILE)
else:
    cache_df = pd.DataFrame(columns=[
        "merchant_name", "city", "place_id", "name",
        "formatted_address", "types", "confidence_score", "category"
    ])

def is_cached(merchant, city):
    return not cache_df[(cache_df["merchant_name"] == merchant) & (cache_df["city"] == city)].empty

def get_cached_category(merchant, city):
    row = cache_df[(cache_df["merchant_name"] == merchant) & (cache_df["city"] == city)]
    return row.iloc[0]["category"] if not row.empty else None

def store_in_cache(entry):
    global cache_df
    cache_df = pd.concat([cache_df, pd.DataFrame([entry])], ignore_index=True)
    cache_df.to_csv(CACHE_FILE, index=False)

def score_match(merchant, result, city):
    score = 0
    if fuzz.partial_ratio(merchant.lower(), result["name"].lower()) > 80:
        score += 40
    if city.lower() in result["formatted_address"].lower():
        score += 30
    if result.get("types") and result["types"][0] in type_to_category:
        score += 20
    if len(result["formatted_address"].split(",")) > 3:
        score += 10
    return score

def query_google_places(merchant, city):
    query = f"{merchant} {city}"
    url = "https://maps.googleapis.com/maps/api/place/textsearch/json"
    params = {
        "query": query,
        "key": API_KEY
    }
    response = requests.get(url, params=params)
    data = response.json()
    if data.get("results"):
        return data["results"][0]  # Take top result
    return None

def categorize_merchant(merchant, city=USER_CITY):
    if is_cached(merchant, city):
        return get_cached_category(merchant, city)

    result = query_google_places(merchant, city)
    if not result:
        return "Uncategorized"

    score = score_match(merchant, result, city)
    category = "Uncategorized"
    if score >= CONFIDENCE_THRESHOLD:
        types = result.get("types", [])
        for t in types:
            if t in type_to_category:
                category = type_to_category[t]
                break

    entry = {
        "merchant_name": merchant,
        "city": city,
        "place_id": result.get("place_id", ""),
        "name": result.get("name", ""),
        "formatted_address": result.get("formatted_address", ""),
        "types": ",".join(result.get("types", [])),
        "confidence_score": score,
        "category": category
    }


    store_in_cache(entry)
    return category

# === TEST API CONNECTION ===
if __name__ == "__main__":
    test_merchant = "Dominos"
    test_category = categorize_merchant(test_merchant)
    print(f"Test result for '{test_merchant}': {test_category}")