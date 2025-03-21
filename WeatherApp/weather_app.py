# Creating a Weather App Using OpenWeatherApp
import requests
import tkinter as tk
from tkinter import messagebox

def get_weather():
    city = city_entry.get()
    if not city:
        messagebox.showerror("Error", "Please enter a city name")
        return

    api_key = "dbc28c6a7dd84b879c5f79262da88b29"  # Replace with your actual API key
    base_url = "http://api.openweathermap.org/data/2.5/weather"
    params = {
        "q": city,
        "appid": api_key,
        "units": "metric"
    }

    try:
        response = requests.get(base_url, params=params)
        response.raise_for_status()
        data = response.json()
        
        weather_desc = data['weather'][0]['description'].capitalize()
        temp = data['main']['temp']
        humidity = data['main']['humidity']
        wind_speed = data['wind']['speed']

        result_label.config(text=(
            f"Weather: {weather_desc}\n"
            f"Temperature: {temp}°C\n"
            f"Humidity: {humidity}%\n"
            f"Wind Speed: {wind_speed} m/s"
        ))
    
    except requests.exceptions.RequestException as e:
        messagebox.showerror("Error", "Failed to fetch data")
    except KeyError:
        messagebox.showerror("Error", "City not found. Please try again.")

# GUI Setup
root = tk.Tk()
root.title("Weather App")
root.geometry("400x300")

city_label = tk.Label(root, text="Enter City:")
city_label.pack(pady=10)

city_entry = tk.Entry(root)
city_entry.pack(pady=5)

search_button = tk.Button(root, text="Get Weather", command=get_weather)
search_button.pack(pady=10)

result_label = tk.Label(root, text="", font=("Arial", 12))
result_label.pack(pady=20)

root.mainloop()
