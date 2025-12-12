import requests
import pandas as pd
from geopy.geocoders import Nominatim

BASE_URL = "https://api.weather.gov/points/"

def get_coordinates(place_name):
    """Converts a place name "Pinnacles National Park, CA" into Lat/Lon."""
    geolocator = Nominatim(user_agent="camp_weather_planner")
    location = geolocator.geocode(place_name)
    if location:
        return location.latitude, location.longitude
    return None, None

def get_forecast(latitude, longitude):
    """Fetches forecast data for a specific Lat/Lon."""
    url = f"{BASE_URL}{latitude},{longitude}"
    print(url)
    response = requests.get(url)
    
    if response.status_code == 200:
        data = response.json()
        forcast_url = data["properties"]["forecast"]
        forcast_url_resp =  requests.get(forcast_url)
        forcast_data = forcast_url_resp.json()
        forecast_list = []
        for entry in range(len(forcast_data)):
            forecast_list.append({
                "Time of Day": forcast_data["properties"]["periods"][entry]["name"],
                "Temp (F)": forcast_data["properties"]["periods"][entry]["temperature"],
                "Wind (mph)": forcast_data["properties"]["periods"][entry]["windSpeed"].replace(" mph",""),
                "Rain (3h)": forcast_data["properties"]["periods"][entry]["probabilityOfPrecipitation"]["value"] 
            })
        return pd.DataFrame(forecast_list)
    return None
    #return forcast_data["properties"]["periods"][0]["temperature"]
 

def get_gear_recommendations(df):
    """Analyzes the forecast dataframe and returns recomended gear list."""
    recommendations = set()
    warnings = []

    min_temp = df['Temp (F)'].min()
    
    if min_temp < 32:
        recommendations.add("❄️ 0°F Rated Sleeping Bag")
        recommendations.add("🧤 Insulated Gloves & Beanie")
        recommendations.add("🔥 Sleeping Pad with R-value > 4")
        warnings.append("Freezing conditions expected! Bring extra fuel.")
    elif min_temp < 50:
        recommendations.add("🛌 20°F Rated Sleeping Bag")
        recommendations.add("🧥 Puffy Down Jacket")
    else:
        recommendations.add("🏞️ 40°F+ Summer Sleeping Bag")


    max_rain = df['Rain (3h)'].max()
    
    if max_rain > 0:
        recommendations.add("☔ Waterproof Rainfly")
        recommendations.add("🥾 Waterproof Hiking Boots")
        recommendations.add("🎒 Pack Rain Cover")
    if max_rain > 5:  # > 5mm in 3 hours is significant
        warnings.append("Heavy rain forecast. Ensure tent footprint is tucked under tent.")

    # # 3. Wind Logic
    # max_wind = df['Wind (mph)'].max()

    # if int(max_wind) > 10:
    #     recommendations.add("💨 Extra Tent Stakes (Guy lines required)")
    # if int(max_wind) > 20:
    #     warnings.append(f"High winds ({max_wind} mph). Avoid camping near dead trees.")

    return recommendations, warnings

#To test output
if __name__ == "__main__":
    place_name = 'Pinnacles National Park, CA'
    latitude, longitude = get_coordinates(place_name)
    df = get_forecast(latitude, longitude)
    print(get_gear_recommendations(df))