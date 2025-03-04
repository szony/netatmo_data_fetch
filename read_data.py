import requests
import json
import os
from dotenv import load_dotenv
from sys import exit as exit


# read secrets

def read_secrets():
    """
    reads variables from .secrets file
    """
    try:
        load_dotenv(".secrets")
        AccessToken = os.getenv("ATOKEN")
        DeviceID = os.getenv("DEVICEID")

        if AccessToken is None:
            print("Error: ATOKEN variable not found in .secrets file.")
            exit(1)
        if DeviceID is None:
            print("Error: DEVICEID variable not found in .secrets file.")
            exit(1)
        return AccessToken, DeviceID

    except Exception as e:
        print(f"Error reading secrets: {e}")
        exit(1)


def get_netatmo_data(access_token, device_id):
    """
    Fetch data from main device and all stations.
    """
    url = "https://api.netatmo.com/api/getstationsdata"
    headers = {
        "Authorization": f"Bearer {access_token}"
    }

    params = {
        "get_favorites": "false",
        "device_id": device_id
    }

    try:
        response = requests.get(url, headers=headers, params=params)
        response.raise_for_status()  # Raise an exception for bad status codes
        data = response.json()
        return data
    except requests.exceptions.RequestException as e:
        print(f"Error fetching data from Netatmo API: {e}")
        return None
    except json.JSONDecodeError as e:
        print(f"Error decoding JSON response: {e}")
        return None


def process_sensor_data(data):
    """
    Processes the sensor data from the Netatmo API and
    creates a JSON object grouped by sensor, excluding trends and min/max values.

    Args:
        data (dict): The JSON data from the Netatmo API.
    Returns:
        dict: The sensor data grouped by sensor, or None if an error occurred.
    """
    sensor_data = {}
    excluded_keys = ["min_temp", "max_temp", "date_min_temp", "date_max_temp", "temp_trend", "pressure_trend"]

    if data and "body" in data and "devices" in data["body"]:
        devices = data["body"]["devices"]
        for device in devices:
            device_id = device["_id"]
            device_name = device.get("station_name", "Main Device")
            sensor_data[device_id] = {"name": device_name, "readings": {}}

            # Process main device data
            if "dashboard_data" in device:
                for key, value in device["dashboard_data"].items():
                    if key != "time_utc" and key not in excluded_keys:
                        sensor_data[device_id]["readings"][key] = value

            # Process module data
            if "modules" in device:
                for module in device["modules"]:
                    module_id = module["_id"]
                    module_name = module.get("module_name", "Unknown Module")
                    sensor_data[module_id] = {"name": module_name, "readings": {}}

                    if "dashboard_data" in module:
                        for key, value in module["dashboard_data"].items():
                            if key != "time_utc" and key not in excluded_keys:
                                sensor_data[module_id]["readings"][key] = value

    else:
        print("Invalid data format or no devices found.")
        return None 

    return sensor_data


def main():
    """
    Main function to fetch and process sensor data.
    Returns the grouped sensor data.
    """
    AccessToken, DeviceID = read_secrets()
    sensor_data = get_netatmo_data(AccessToken, DeviceID)
    if sensor_data:
        data_grouped_by_sensor = process_sensor_data(sensor_data)
        return data_grouped_by_sensor
    return None


if __name__ == "__main__":
    grouped_data = main()
    if grouped_data:
        print("\n--- Grouped Sensor Data (JSON) ---")
        print(json.dumps(grouped_data, indent=2))
