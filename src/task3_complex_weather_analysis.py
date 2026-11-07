import json


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


def analyze_daily_weather(day, temp_threshold=30, wind_threshold=15, humidity_threshold=70):
    """
    Analyze weather data for a single day.

    Args:
        day (dict): The weather data for the day.
        temp_threshold (float): The temperature threshold to determine a hot day.
        wind_threshold (float): The wind speed threshold to determine a windy day.
        humidity_threshold (float): The humidity threshold to determine uncomfortable weather.

    Returns:
        dict: A dictionary with analysis results for the day.
    """
    
    max_temp = day.get("max_temperature", 0.0)
    min_temp = day.get("min_temperature", 0.0)
    precipitation = day.get("precipitation", 0.0)
    wind_speed = day.get("wind_speed", 0.0)
    humidity = day.get("humidity", 0)
    description = day.get("weather_description", "")
    
    is_hot_day = max_temp > temp_threshold
    
    temperature_swing = round(abs(max_temp - min_temp), 1)
    is_significant_swing =temperature_swing > 10.0
    
    is_windy_day = wind_speed > wind_threshold
    
    is_uncomfortable_day = humidity > humidity_threshold
    
    is_rainy_day = precipitation > 0.0 or "rain" in description.lower()
    
    return {
        "date": day.get("date"),
        "description": description,
        "max_temp": max_temp,
        "min_temp": min_temp,
        "precipitation": precipitation,
        "wind_speed": wind_speed,
        "humidity": humidity,
        "is_hot_day": is_hot_day,
        "temperature_swing": temperature_swing,
        "is_significant_swing": is_significant_swing,
        "is_windy_day": is_windy_day,
        "is_uncomfortable_day": is_uncomfortable_day,
        "is_rainy_day":is_rainy_day        
    }


def generate_daily_report(analysis):
    """
    Generate a detailed report based on the analysis results for a single day.

    Args:
        analysis (dict): The analysis results for the day.

    Returns:
        str: A detailed report as a string.
    """
    
    description = analysis.get('description') or analysis.get('weather_description', '')
    max_temp = (
        analysis.get('max_temp') 
        if analysis.get('max_temp') is not None 
        else analysis.get('max_temperature', analysis.get('temperature_swing', ''))
    )
    
    lines = [
        f"Date: {analysis.get('date')}",
        f"Weather: {description}",
        f"Temperature: Max {max_temp}°C"
    ]
    
    if analysis.get('is_hot_day'):
        lines.append("It was a hot day.")
        
    if analysis.get('is_windy_day'):
        lines.append("It was a windy day.")
        
    if analysis.get('is_uncomfortable_day'):
        lines.append("The humidity made the day uncomfortable.")
        
    if analysis.get('is_rainy_day'):
        lines.append("It was a rainy day.")
    else:
        lines.append("There was no precipitation.")
        
    lines.append('\n')

    return "\n".join(lines)



def summarize_weather_analysis(analyses):
    """
    Summarize the weather analysis over multiple days.

    Args:
        analyses (list of dict): A list of daily analysis results.

    Returns:
        str: A summary report as a string.
    """
    
    if not analyses:
        return "No weather data available for summary."
    
    hottest = max(analyses, key=lambda x: x.get("max_temp", 0))
    windiest = max(analyses, key=lambda x: x.get("wind_speed", 0))
    most_humid = max(analyses, key=lambda x: x.get("humidity", 0))
    rainiest = max(analyses, key=lambda x: x.get("precipitation", 0))
    
    lines = [
        "Weather Summary:",
        f"Hottest day: {hottest.get('date')} with a maximum temperature of {hottest.get('max_temp')}°C",
        f"Windiest day: {windiest.get('date')} with wind speeds of {windiest.get('wind_speed')} km/h",
        f"Most humid day: {most_humid.get('date')} with a humidity level of {most_humid.get('humidity')}%",
        f"Rainiest day: {rainiest.get('date')} with {rainiest.get('precipitation')} mm of precipitation"
    ]

    return "\n".join(lines)


if __name__ == "__main__":
    # Load the JSON data
    weather_data = load_json("src/tokyo_weather_complex.json")

    # Analyze the weather data for each day
    analyses = [analyze_daily_weather(day) for day in weather_data['daily']]

    # Generate and print daily reports
    for analysis in analyses:
        report = generate_daily_report(analysis)
        print(report)

    # Generate and print a summary report
    summary_report = summarize_weather_analysis(analyses)
    print(summary_report)
