import read_data
import json

# Get the grouped sensor data
grouped_data = read_data.main()

# Check if data was retrieved and processed successfully
if grouped_data:
    # Do something with the data (e.g., print it, save it to a file, etc.)
    print("Data received:\n")
    print(json.dumps(grouped_data, indent=2))
else:
    print("Failed to get sensor data.")