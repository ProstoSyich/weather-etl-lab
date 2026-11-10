import os
import requests
from dotenv import load_dotenv
load_dotenv()
def _fallback():
    city = os.getenv("GEO_API_FALLBACK_CITY", "Киров")
    return {"city": city, "lat": None, "lon": None}

def get_location():
    url = os.getenv("GEO_API_URL")
    #("DEBUG url =", repr(url))
    try:
        response = requests.get(url, timeout=10)
        if response.status_code != 200:
            return _fallback()
        data = response.json()
        city = data.get("city")
        lat = data.get("lat")
        lon = data.get("lon")
        if city and lon and lat:
            return {"city": city, "lon": lon, "lat": lat}
    except requests.RequestException:
        return _fallback()
    return _fallback()

#if __name__ == "__main__":
    print(get_location())
