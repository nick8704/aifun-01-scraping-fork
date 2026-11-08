import xml.etree.ElementTree as ET
import csv


def parse_weather_xml(xml_file):
    """
    Parse weather data from an XML file.

    Args:
        xml_file (str): Path to the XML file.

    Returns:
        list of dict: A list of dictionaries with parsed weather data.
    """
    
    tree = ET.parse(xml_file)
    root = tree.getroot()
    
    weather_data = []
    
    for day in root.findall('day'):  
        weather_data.append({
            "date": day.find('date').text,
            "temperature": float(day.find('temperature').text),
            "humidity": int(day.find('humidity').text),
            "precipitation": float(day.find('precipitation').text),
            "Date": day.find('date').text,
            "Temperature": float(day.find('temperature').text),
            "Humidity": int(day.find('humidity').text),
            "Precipitation": float(day.find('precipitation').text),
        })

    return weather_data


def save_to_csv(data, filename="parsed_weather_data.csv"):
    """
    Save parsed weather data to a CSV file.

    Args:
        data (list of dict): Parsed weather data.
        filename (str): Name of the CSV file.
    """
    headers = ["Date", "Temperature", "Humidity", "Precipitation"]
    
    with open(filename, 'w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow(headers)
        
        for row in data:
            date_val = row.get("Date") or row.get("date", "")
            temp_val = row.get("Temperature") if row.get("Temperature") is not None else row.get("temperature", 0.0)
            humidity_val = row.get("Humidity") if row.get("Humidity") is not None else row.get("humidity", 0)
            precip_val = row.get("Precipitation") if row.get("Precipitation") is not None else row.get("precipitation", 0.0)
            
            writer.writerow([
                date_val,
                temp_val,
                humidity_val,
                precip_val
            ])


if __name__ == "__main__":
    # Parse the XML file
    weather_data = parse_weather_xml("src/weather_data.xml")

    # Save the parsed data to a CSV file
    save_to_csv(weather_data)
    print(
        "Data has been successfully parsed and saved to parsed_weather_data.csv."
    )
