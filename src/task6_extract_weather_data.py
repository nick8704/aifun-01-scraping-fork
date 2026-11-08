import csv
import re


def clean_text(line):
    """
    Clean the text line by removing non-ASCII characters and fixing known issues.

    Args:
        line (str): The line of text to clean.

    Returns:
        str: The cleaned line of text.
    """
    if not isinstance(line, str):
        return ""
    
    line = line.replace('\xa0', ' ')
    cleaned_line = line.encode("ascii", "ignore").decode("ascii")

    return cleaned_line.strip()


def extract_weather_data(text_file):
    """
    Extract weather data from a text file using regular expressions.

    Args:
        text_file (str or file-like object): Path to the text file or file-like object.

    Returns:
        list of dict: A list of dictionaries with extracted weather data.
    """
    extracted_data = []
    
    # Виправлений регулярний вираз: цифри всередині груп, а °C, % та коми — зовні
    pattern = re.compile(
        r"Date:\s*(?P<date>\d{4}-\d{2}-\d{2}),\s*"
        r"Max Temp:\s*(?P<max_temp>[\d.]+)(?:C)?,\s*"
        r"Min Temp:\s*(?P<min_temp>[\d.]+)(?:C)?,\s*"
        r"Humidity:\s*(?P<humidity>\d+)%?,\s*"
        r"Precipitation:\s*(?P<precip>[\d.]+)mm?"
    )
    
    if isinstance(text_file, str):
        with open(text_file, 'r', encoding='utf-8', errors='ignore') as f:
            lines = f.readlines()
    else:
        lines = text_file.readlines()
    
    for line in lines:
        cleaned = clean_text(line)
        
        match = pattern.search(cleaned)
        if match:
            groups = match.groupdict()
            
            date_val = groups["date"]
            max_temp = float(groups["max_temp"])
            min_temp = float(groups["min_temp"])
            humidity = int(groups["humidity"])
            precipitation = float(groups["precip"])
            
            extracted_data.append({
                "Date": date_val,
                "date": date_val,
                "Max Temp": max_temp,
                "max_temperature": max_temp,
                "Min Temp": min_temp,
                "min_temperature": min_temp,
                "Humidity": humidity,
                "humidity": humidity,
                "Precipitation": precipitation,
                "precipitation": precipitation
            })

    return extracted_data


def save_to_csv(data, filename="extracted_weather_data.csv"):
    """
    Save extracted weather data to a CSV file.

    Args:
        data (list of dict): Extracted weather data.
        filename (str): Name of the CSV file.
    """
    headers = ["Date", "Max Temperature", "Min Temperature", "Humidity", "Precipitation"]
    
    with open(filename, 'w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow(headers)
        
        for row in data:
            date_val = row.get("Date") or row.get("date", "")
            max_temp = row.get("Max Temp") if row.get("Max Temp") is not None else row.get("max_temperature", 0.0)
            min_temp = row.get("Min Temp") if row.get("Min Temp") is not None else row.get("min_temperature", 0.0)
            humidity = row.get("Humidity") if row.get("Humidity") is not None else row.get("humidity", 0.0)
            precipitation = row.get("Precipitation") if row.get("Precipitation") is not None else row.get("precipitation", 0.0)
                    
            writer.writerow([
                date_val,
                max_temp,
                min_temp,
                humidity,
                precipitation
            ])


if __name__ == "__main__":
    # Extract data from the text file
    weather_data = extract_weather_data("src/weather_report.txt")

    # Save the extracted data to a CSV file
    save_to_csv(weather_data)
    print(
        "Data has been successfully extracted and saved to extracted_weather_data.csv."
    )
