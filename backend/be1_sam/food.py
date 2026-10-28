"""Sam: public venue discovery. Metta: ingredient exclusion, no safety certification."""
import math
import time
import httpx
from .health_catalog import ALLERGIES

_places_cache = {}
RECIPES = [
    ("Plain steamed rice with cooked vegetables", "rice, carrot, green beans, water, olive oil", set()),
    ("Lentil and vegetable bowl", "lentils, carrot, spinach, rice, water, olive oil", set()),
    ("Egg and rice bowl", "egg, rice, carrot, olive oil", {"egg"}),
    ("Plain yogurt with banana", "milk yogurt, banana", {"milk"}),
    ("Chickpea and cucumber bowl", "chickpeas, cucumber, tomato, lemon, olive oil", set()),
    ("Tofu with rice and vegetables", "soy tofu, rice, carrot, olive oil", {"soy"}),
]

def meal_ideas(profile):
    names = [ALLERGIES[a] for a in profile.allergy_ids if a in ALLERGIES]
    if profile.other_allergy.strip():
        return [], "You listed another allergy. Automated meal suggestions are paused because its ingredients cannot be reliably checked."
    if {"C03","C06"}.intersection(profile.condition_ids):
        return [], "Your selected heart/kidney condition may require a personalised diet. Use your existing clinician or dietitian plan; automatic meal selection is paused."
    ideas = [{"name":name,"ingredients":ingredients,"note":"Based only on these listed ingredients. Confirm substitutions, cooking oils, sauces and cross-contact before ordering."} for name,ingredients,allergens in RECIPES if not allergens.intersection(profile.allergy_ids)]
    note = "Meal ideas exclude selected allergens from their listed ingredients only; they are not verified restaurant dishes or medical diet prescriptions."
    if names: note += " Tell staff about: " + ", ".join(names) + "."
    return ideas[:4],note

def distance(lat, lon, a, b):
    r1,r2=math.radians(lat),math.radians(a)
    h=math.sin((r2-r1)/2)**2+math.cos(r1)*math.cos(r2)*math.sin(math.radians(b-lon)/2)**2
    return 6371*2*math.asin(min(1,math.sqrt(h)))

async def nearby_places(lat,lon):
    key=(round(lat,2),round(lon,2))
    cached=_places_cache.get(key)
    if cached and time.monotonic()-cached[0]<1800: return cached[1]
    query=f'[out:json][timeout:12];nwr["amenity"~"^(restaurant|cafe|fast_food)$"]["name"](around:3000,{key[0]},{key[1]});out center 60;'
    try:
        async with httpx.AsyncClient(timeout=17) as client:
            response=await client.post("https://overpass-api.de/api/interpreter",data={"data":query},headers={"User-Agent":"WeatherWise-Prototype/1.1"})
            response.raise_for_status(); payload=response.json()
        if payload.get("remark"): raise ValueError("Incomplete provider query")
        places=[]
        for item in payload.get("elements",[]):
            point=item.get("center",item); tags=item.get("tags",{})
            if "lat" not in point or "lon" not in point: continue
            places.append({"name":tags.get("name","Food place"),"cuisine":tags.get("cuisine","Cuisine not listed").replace(";",", "),
                "distance_km":round(distance(*key,point["lat"],point["lon"]),1),
                "url":f'https://www.openstreetmap.org/{item["type"]}/{item["id"]}',
                "allergen_status":"Unknown - ask the venue", "opening_status":"Not verified"})
        result={"status":"available","places":sorted(places,key=lambda p:p["distance_km"])[:6],"message":"Nearby public listings, not endorsements. Distance is from your approximate location. Allergen controls and opening hours are unverified."}
        if len(_places_cache)>=128: _places_cache.pop(next(iter(_places_cache)))
        _places_cache[key]=(time.monotonic(),result)
        return result
    except (httpx.HTTPError,ValueError,KeyError,TypeError):
        return {"status":"unavailable","places":[],"message":"Nearby listings are temporarily unavailable. No restaurant results have been invented."}
