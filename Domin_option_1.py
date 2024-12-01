# Importing necessary Libraries
import random
import time
from collections import deque
import sqlite3
import threading
from flask import Flask, jsonify, render_template, request
import signal
import sys

# Function to handle graceful exit on Ctrl+C (SIGINT)
def signal_handler(sig, frame):
    print('Exiting gracefully...')
    sys.exit(0)

# Set the signal handler for SIGINT (Ctrl+C)
signal.signal(signal.SIGINT, signal_handler)

# Simulating Sensor Data Acquisition
def simulate_sensor_data(buffer, running_event):
    while running_event.is_set():  # This ensures the loop runs while 'Start' is active
        flow_1 = random.uniform(0, 100)  # Liters per minute
        flow_2 = random.uniform(0, 100)
        temperature = random.uniform(20, 80)  # Degrees Celsius
        pressures = [random.uniform(10, 200) for _ in range(4)]  # 4 Pressure values
        position = random.uniform(0, 50)  # Linear Encoder for position 

        # Add the sensor readings to the buffer
        buffer.append({
            "flow_1": flow_1,
            "flow_2": flow_2,
            "temperature": temperature,
            "pressures": pressures,
            "position": position,
            "timestamp": time.time()  # Record the time
        })
        time.sleep(1)  # Simulate a 1 Hz sampling rate

# Data Processing and Storing in Database
def process_and_store_data(buffer, db_conn, running_event):
    data_counter = 0  # Counter to control print frequency
    while running_event.is_set():  # This ensures the loop runs while 'Start' is active
        if buffer:
            data = buffer.popleft()

            avg_pressure = sum(data["pressures"]) / len(data["pressures"])

            cursor = db_conn.cursor()
            cursor.execute("""
                INSERT INTO sensor_data (flow_1, flow_2, temperature, avg_pressure, position, timestamp)
                VALUES (?, ?, ?, ?, ?, ?)
            """, (data["flow_1"], data["flow_2"], data["temperature"], avg_pressure, data["position"], data["timestamp"]))
            db_conn.commit()

            data_counter += 1
            if data_counter % 10 == 0:
                print(f"Stored Data: {data}")

        time.sleep(0.1)  # Avoid busy waiting

# Flask Web Server for Streaming to a UI
app = Flask(__name__)

# Database connection
db_conn = sqlite3.connect("sensor_data.db", check_same_thread=False)

# Route for the main dashboard page
@app.route("/")
def dashboard():
    # Render the main HTML file (dashboard.html) for the dashboard
    return render_template("dashboard.html")

# API route to fetch the latest sensor data
@app.route("/api/data")
# Create a cursor to execute database queries
def api_data():
    cursor = db_conn.cursor()
    # Query to get the 10 most recent rows from the sensor_data table, ordered by timestamp
    cursor.execute("SELECT * FROM sensor_data ORDER BY timestamp DESC LIMIT 10")
    rows = cursor.fetchall()
    # Convert rows into a list of dictionaries for easy JSON formatting
    data = [{"flow_1": row[1], "flow_2": row[2], "temperature": row[3], "avg_pressure": row[4], "position": row[5], "timestamp": row[6]} for row in rows]
    # Return the data as a JSON response
    return jsonify(data)

#  API route to start the data acquisition and processing test
@app.route("/start", methods=["POST"])
def start_test():
    # Declare the global variables that will be modified
    global acquisition_thread, processing_thread, running_event
     # Check if the running event is not already set (test not running)
    if not running_event.is_set():
        # Set the running event to signal that the test is active
        running_event.set()
        
        acquisition_thread = threading.Thread(target=simulate_sensor_data, args=(buffer, running_event))  # Start the sensor data acquisition thread
        processing_thread = threading.Thread(target=process_and_store_data, args=(buffer, db_conn, running_event)) # Start the data processing and storing thread
        acquisition_thread.start()
        processing_thread.start()

        return jsonify({"status": "Test started"})
    
    return jsonify({"status": "Test already running"})

# API route to stop the data acquisition and processing test
@app.route("/stop", methods=["POST"])
def stop_test():
    global running_event

    running_event.clear()  # Clear the running event to signal the threads to stop

    # Wait for both threads to finish before proceeding
    acquisition_thread.join()
    processing_thread.join()

    return jsonify({"status": "Test stopped"})

# Main function
if __name__ == "__main__":
    # Create a buffer for data acquisition
    buffer = deque(maxlen=100)

    # Set up the database
    conn = sqlite3.connect("sensor_data.db", check_same_thread=False)
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS sensor_data (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            flow_1 REAL,
            flow_2 REAL,
            temperature REAL,
            avg_pressure REAL,
            position REAL,
            timestamp REAL
        )
    """)
    conn.commit()

    # Global event to control start/stop
    running_event = threading.Event()

    # Start the Flask app
    app.run(debug=True)
