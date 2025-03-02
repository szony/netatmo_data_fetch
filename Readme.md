# Netatmo Data Fetch

This program fetches data from Netatmo sensors using the Netatmo API. It retrieves sensor readings, prints them to the console, and saves them in a JSON file.

## Purpose

The script was written to:

1.  **Access Netatmo API:** Directly interact with the Netatmo API to retrieve sensor data.
2.  **Read Sensor Data:** Fetch data from specified Netatmo sensors.
3.  **Display Data:** Print the retrieved sensor data to the console for immediate viewing.
4.  **Save Data:** Store the sensor data in a JSON file for later analysis or use.

## Configuration

The script requires a `.secrets` file to store sensitive information.

### .secrets File

The `.secrets` file should be located in the same directory as the script and contain the following information:

*   **ATOKEN:** Your Netatmo API access token.
*   **DEVICEID:** The ID of the Netatmo device you want to read data from.

**Example .secrets file:**

```
ATOKEN=YOUR_NETATMO_ACCESS_TOKEN
DEVICEID=YOUR_NETATMO_DEVICE_ID
```

**Note:** Replace `YOUR_NETATMO_ACCESS_TOKEN` and `YOUR_NETATMO_DEVICE_ID` with your actual credentials.

## Usage

1.  Ensure you have a `.secrets` file with the correct credentials.
2.  Run the script.
3.  The data will be fetched, printed it to the console, and saved to a JSON file.

## Dependencies

*   Python 3.x
*   Requests library (for API interaction)
*   json library (for json handling)
