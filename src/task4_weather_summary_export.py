import json
import csv


def load_json(filename):
    """
    Load JSON data from a file.

    Args:
        filename (str): The name of the JSON file to load.

    Returns:
        dict: The loaded JSON data.
    """
    
    with open(filename, 'r', encoding='utf-8') as f:
        return json.load(f)


def summarize_weather_data(data):
    """
    Summarize the weather data across all days.

    Args:
        data (list of dict): The daily weather data.

    Returns:
        dict: A summary of the key metrics across all days.
    """
    
    total_days = len(data)
    sum_max_temp = 0.0
    sum_min_temp = 0.0
    total_precipitation = 0.0
    sum_wind_speed = 0.0
    sum_humidity = 0.0
    
    hot_days_count = 0
    windy_days_count = 0
    rainy_days_count = 0
    
    for day in data:
        max_temp = day.get("max_temperature", 0.0)
        min_temp = day.get("min_temperature", 0.0)
        precipitation = day.get("precipitation", 0.0)
        wind_speed = day.get("wind_speed", 0.0)
        humidity = day.get("humidity", 0)
        description = day.get("weather_description", "").lower()
        
        sum_max_temp += max_temp
        sum_min_temp += min_temp
        total_precipitation += precipitation
        sum_wind_speed += wind_speed
        sum_humidity += humidity
        
        if max_temp > 30.0:
            hot_days_count += 1
        if wind_speed > 15.0:
            windy_days_count += 1
        if precipitation > 0.0 or "rain" in description:
            rainy_days_count += 1
            
        avg_max_temp = round(sum_max_temp / total_days, 2)
        avg_min_temp = round(sum_min_temp / total_days, 2)
        avg_wind_speed = round(sum_wind_speed / total_days, 2)
        avg_humidity = round(sum_humidity / total_days, 2)
        total_precipitation = round(total_precipitation, 2)

    return {
        "average_max_temp": avg_max_temp,
        "average_min_temp": avg_min_temp,
        "total_precipitation": total_precipitation,
        "average_wind_speed": avg_wind_speed,
        "average_humidity": avg_humidity,
        "hot_days": hot_days_count,
        "windy_days": windy_days_count,
        "rainy_days": rainy_days_count,
        "total_days": total_days
    }


def export_to_csv(data, file):
    """
    Export the summarized weather data to a CSV file or file-like object.

    Args:
        data (list of dict): The daily weather data to export.
        file (str or file-like object): The name of the CSV file to save the data in, or a file-like object.
    """
    
    headers = [
        "Date", "Max Temperature", "Min Temperature", "Precipitation", "Wind Speed", "Humidity", "Weather Description", "Is Hot Day", "Is Windy Day", "Is Rainy Day"
    ]
    
    def write_data(f):
        writer = csv.writer(f)
        writer.writerow(headers)
        
        for day in data:
            max_temp = day.get("max_temperature", 0.0)
            min_temp = day.get("min_temperature", 0.0)
            precipitation = day.get("precipitation", 0.0)
            wind_speed = day.get("wind_speed", 0.0)
            humidity = day.get("humidity", 0)
            description = day.get("weather_description", "")
            
            is_hot = day.get("is_hot_day", max_temp > 30.0)
            is_windy = day.get("is_windy_day", wind_speed > 15.0)
            is_rainy = day.get("is_rainy_day", precipitation > 0.0 or "rain" in description.lower())
            
            writer.writerow([
                day.get("date"),
                max_temp,
                min_temp,
                precipitation,
                wind_speed,
                humidity,
                description,
                is_hot,
                is_windy,
                is_rainy
            ])
            
    if isinstance(file, str):
        with open(file, 'w', newline='', encoding='utf-8') as f:
            write_data(f)
    else:
        write_data(file)
            


if __name__ == "__main__":
    # Load the JSON data
    weather_data = load_json("src/tokyo_weather_complex.json")

    # Summarize the weather data
    summary = summarize_weather_data(weather_data['daily'])

    # Print the summary for verification
    print("Weather Data Summary:")
    for key, value in summary.items():
        print(f"{key}: {value}")

    # Export the summarized data to a CSV file
    export_to_csv(weather_data['daily'], "tokyo_weather_summary.csv")

    print("Data successfully exported to tokyo_weather_summary.csv")
