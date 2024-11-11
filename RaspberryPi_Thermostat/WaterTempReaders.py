import os
import glob
import time
import json
import RPi.GPIO as GPIO
from influxdb_client import InfluxDBClient, Point

# InfluxDB details
token = "IfYouHaveToAskYoullNeverKnow."
org = "WaterSensors" #ORG_Name on Influx
bucket = "WaterSensorBucket" #Bucket on InfluxDB
url = "IfYouKnowYoullNeverHaveToAsk"  #URL FOR INFLUX DB ENDPOINT

client = InfluxDBClient(url=url, token=token, org=org)
write_api = client.write_api()

# Set up the GPIO pins for the sensors
SENSOR_PINS = [17, 18, 22]  # You can change these to whatever you want. 

# Setup GPIO
GPIO.setmode(GPIO.BCM)  # Use BCM pin numbering
for pin in SENSOR_PINS:
    GPIO.setup(pin, GPIO.IN)

# Local log file for queued data - need to double_check that this works. 
log_file = "/home/pi/sensor_data_log.json"

# Function to discover connected sensors, sorting them by their unique IDs for consistent GPIO assignment
def discover_sensors():
    sensor_base_dir = '/sys/bus/w1/devices/'
    sensor_folders = sorted(glob.glob(sensor_base_dir + '28-*'))  # Sort sensors alphabetically by their ID
    return sensor_folders

# Function to read the raw temperature data from a sensor
def read_temp_raw(sensor_path):
    try:
        with open(sensor_path + "/w1_slave", 'r') as f:
            lines = f.readlines()
        return lines
    except FileNotFoundError:
        return None

# Function to parse temperature from sensor data
def read_temp(sensor_path):
    lines = read_temp_raw(sensor_path)
    if lines and lines[0].strip()[-3:] == 'YES':
        equals_pos = lines[1].find('t=')
        if equals_pos != -1:
            temp_string = lines[1][equals_pos+2:]
            temp_c = float(temp_string) / 1000.0
            temp_f = temp_c * 9.0 / 5.0 + 32.0
            return temp_c, temp_f
    return None

# Function to log data to local file (when InfluxDB is down)
def log_data_locally(sensor_id, temp_c, temp_f):
    timestamp = time.strftime('%Y-%m-%dT%H:%M:%SZ', time.gmtime())
    data_point = {"sensor_id": sensor_id, "time": timestamp, "temp_celsius": temp_c, "temp_fahrenheit": temp_f}
    
    if not os.path.exists(log_file):
        with open(log_file, 'w') as f:
            json.dump([data_point], f)
    else:
        with open(log_file, 'r+') as f:
            data = json.load(f)
            data.append(data_point)
            f.seek(0)
            json.dump(data, f)
    
    print(f"Queued data locally for sensor {sensor_id}: {temp_f} °F / {temp_c} °C")

# Function to send queued data to InfluxDB
def send_queued_data():
    if os.path.exists(log_file):
        with open(log_file, 'r') as f:
            data = json.load(f)
        for entry in data:
            point = Point("temperature").tag("sensor", entry['sensor_id']).field("temp_celsius", entry['temp_celsius']).field("temp_fahrenheit", entry['temp_fahrenheit']).time(entry['time'])
            try:
                write_api.write(bucket=bucket, org=org, record=point)
                print(f"Sent queued data for sensor {entry['sensor_id']}: {entry['temp_fahrenheit']} °F / {entry['temp_celsius']} °C")
            except Exception as e:
                print(f"Failed to send queued data: {e}")
                break  # Stop if there are issues sending
        else:
            # If all data was sent successfully, clear the log file
            os.remove(log_file)
            print("Cleared queued data after successful send")

# Main loop to continuously read temperatures and send to InfluxDB
try:
    while True:
        sensor_paths = discover_sensors()
        
        if not sensor_paths:
            print("No sensors found.")
        else:
            for i, sensor_path in enumerate(sensor_paths):
                if i < len(SENSOR_PINS):
                    sensor_name = os.path.basename(sensor_path)  # Get the sensor ID from the path
                    GPIO_PIN = SENSOR_PINS[i]  # Assign corresponding GPIO pin based on sorted order
                    
                    # Read from the GPIO pin
                    if GPIO.input(GPIO_PIN):
                        temperature_data = read_temp(sensor_path)
                        if temperature_data:
                            temp_c, temp_f = temperature_data
                            point = Point("temperature").tag("sensor", sensor_name).field("temp_celsius", temp_c).field("temp_fahrenheit", temp_f)
                            try:
                                # Send data to InfluxDB
                                write_api.write(bucket=bucket, org=org, record=point)
                                print(f"Temperature for sensor {sensor_name}: {temp_f} °F / {temp_c} °C sent to InfluxDB")
                                
                                # After a successful send, try to send any queued data
                                send_queued_data()

                            except Exception as e:
                                # If InfluxDB is unreachable, log the data locally
                                print(f"InfluxDB connection failed: {e}")
                                log_data_locally(sensor_name, temp_c, temp_f)

        time.sleep(10)  # Adjust this to the desired interval between readings

except KeyboardInterrupt:
    print("Program terminated.")

finally:
    client.close()
    GPIO.cleanup()

