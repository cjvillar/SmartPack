from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from load_data import get_coordinates, get_forecast
import pandas as pd

app = FastAPI(title="Camp Weather API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/weather")
def weather(place: str):
    latitude, longitude = get_coordinates(place)
    if latitude is None or longitude is None: # spell out latitude because I keep adding a t and need to learn
        return {"error": "Location not found"}
    
    df = get_forecast(latitude, longitude)
    if df is None:
        return {"error": "Could not fetch forecast"}
    
    return df.to_dict(orient="records")