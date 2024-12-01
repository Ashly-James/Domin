# Sensor Data Acquisition and Processing with Flask
This project demonstrates the use of Flask for streaming sensor data to a web interface. It simulates the acquisition of sensor data, processes it, and stores the data in an SQLite database. The data is then visualised using a Flask web application.

## Features
Simulate Sensor Data: Randomized data for flow rates, temperature, pressure, and position.
Real-Time Data Acquisition: Data is captured in real-time, processed, and stored.
SQLite Database: Stores the sensor data for later retrieval.
Flask Web Interface: Displays the real-time data on a dashboard.

## API Endpoints:
/api/data: Fetches the latest 10 sensor data records in JSON format.
/start: Starts the data acquisition and processing test.
/stop: Stops the data acquisition and processing test.

## Prerequisites
To run this project, you need the following:
* Python 3.x
* Flask
* SQLite3
* (Optional) A code editor like Visual Studio Code

### Install the required dependencies:
**pip install flask**
Run the application:
In your terminal, navigate to the project directory and run:
**python Domin_option_1.py**
This will start a local Flask server at http://127.0.0.1:5000/.
# How It Works
1. Simulate Sensor Data: The simulate_sensor_data function generates random values for sensor readings (flow rates, temperature, pressure, and position) and adds them to a buffer.

2. Process and Store Data: The process_and_store_data function processes the sensor data from the buffer and stores it in an SQLite database.

3. Flask Web Server: The Flask application exposes several routes:

* / serves the main dashboard.
* /api/data provides the latest sensor data in JSON format.
* /start starts the data acquisition and processing.
* /stop stops the data acquisition and processing.
4. Database: An SQLite database (sensor_data.db) is used to store the sensor data. Each sensor reading is stored with its corresponding timestamp.

### Testing and Usage
After starting the Flask server, navigate to **http://127.0.0.1:5000/** in your browser.
Click the "**Start Test**" button to begin acquiring and processing sensor data.
The data will be displayed on the dashboard in real-time.
Click the "**Stop Test**" button to stop the process.
The latest 10 sensor readings can be accessed via the /api/data endpoint.
## Data Visualization
### Sensor Data Chart
Below the table, a line chart visualizes the latest sensor data values for Flow 1, Flow 2, and other relevant metrics. The chart is generated using Chart.js and updates dynamically as new data is acquired.

### Chart Interactivity
Interactive Labels: Each dataset (e.g., Flow 1, Flow 2) on the chart is represented by a label. You can toggle visibility of each dataset by clicking on its respective label in the chart legend.
Data Toggle: Clicking on the label for a particular dataset will hide the corresponding data line from the chart. Clicking the label again will show the line again. This allows for a more focused view of the data.
This feature is especially useful for comparing different sensor readings, allowing users to toggle data visibility for better clarity and analysis.
