import os
import requests
import matplotlib.pyplot as plt

def get_weather(city: str):
    """Return current weather dict from Open-Meteo for a city name."""
    # 1) Geocode
    geo_url = f"https://geocoding-api.open-meteo.com/v1/search?name={city}&count=1"
    geo = requests.get(geo_url, timeout=20).json()
    if not geo.get("results"):
        raise ValueError("City not found. Try a larger city or different spelling.")
    lat = geo["results"][0]["latitude"]
    lon = geo["results"][0]["longitude"]
    # 2) Weather
    wx_url = (        f"https://api.open-meteo.com/v1/forecast?latitude={lat}&longitude={lon}&current_weather=true"    )
    wx = requests.get(wx_url, timeout=20).json()
    return wx["current_weather"]

def happiness_score(temp_c: float, wind_kmh: float) -> int:
    """Simple heuristic 0..100: comfy temp and gentle wind are 'happier'."""
    score = 100
    # Temperature comfort band ~ 18–27°C
    if temp_c < 10 or temp_c > 32:
        score -= 30
    elif temp_c < 18 or temp_c > 27:
        score -= 15
    # Wind penalty
    if wind_kmh > 30:
        score -= 20
    elif wind_kmh > 15:
        score -= 10
    return max(0, min(100, score))

def visualize(city: str, score: int, out_path: str = "visuals/city_happiness_chart.png"):
    os.makedirs(os.path.dirname(out_path), exist_ok=True)
    plt.figure(figsize=(6,4))
    plt.bar([city], [score])  # use default matplotlib color
    plt.title(f"Happiness Score for {city}")
    plt.ylim(0, 100)
    plt.ylabel("Happiness Level (0–100)")
    plt.tight_layout()
    plt.savefig(out_path, dpi=200)
    # plt.show()  # Uncomment if running locally

def main():
    city = input("Enter a city name: ").strip()
    if not city:
        print("No city provided.")
        return
    wx = get_weather(city)
    temp = wx["temperature"]
    wind = wx["windspeed"]
    print(f"Temperature: {temp}°C | Wind: {wind} km/h")
    score = happiness_score(temp, wind)
    print(f"Calculated Happiness Score: {score}")
    visualize(city, score)
    print("Saved chart to visuals/city_happiness_chart.png")


if __name__ == "__main__":
    main()
