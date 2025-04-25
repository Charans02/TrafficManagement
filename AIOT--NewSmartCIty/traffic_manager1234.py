from flask import Flask, render_template, jsonify
import threading
import time
import random
import RPi.GPIO as GPIO

app = Flask(__name__)

# 7-segment display GPIO setup
SDI = 21  # Data pin
RCLK = 19  # Latch pin
SRCLK = 24  # Clock pin
segCode = [0x3f, 0x06, 0x5b, 0x4f, 0x66, 0x6d, 0x7d, 0x07, 0x7f, 0x6f]

def setup_display():
    GPIO.setmode(GPIO.BOARD)
    GPIO.setwarnings(False)
    GPIO.setup(SDI, GPIO.OUT)
    GPIO.setup(RCLK, GPIO.OUT)
    GPIO.setup(SRCLK, GPIO.OUT)
    GPIO.output(SDI, GPIO.LOW)
    GPIO.output(RCLK, GPIO.LOW)
    GPIO.output(SRCLK, GPIO.LOW)

def hc595_shift(dat):
    for bit in range(0, 16):
        GPIO.output(SDI, (0x8000 & (dat << bit)) != 0)
        GPIO.output(SRCLK, GPIO.HIGH)
        time.sleep(0.001)
        GPIO.output(SRCLK, GPIO.LOW)
    GPIO.output(RCLK, GPIO.HIGH)
    time.sleep(0.001)
    GPIO.output(RCLK, GPIO.LOW)

def display_number_on_kit(number):
    if number < 10:
        hc595_shift(segCode[number] << 8)  # Shift 1 digit
    else:
        tens = number // 10
        ones = number % 10
        hc595_shift(segCode[ones] << 8 | segCode[tens])  # Shift two digits
    time.sleep(0.1)

# Shared data for the countdown values
traffic_data = {
    "A": {"time": 0, "light": "red"}, 
    "B": {"time": 0, "light": "red"}, 
    "C": {"time": 0, "light": "red"}, 
    "D": {"time": 0, "light": "red"},
    "current": "", "remaining_time": 0, "light": "red"
}

def generate_random_values():
    A = random.randint(10, 100)
    B = random.randint(50, 70)
    C = random.randint(80, 91)
    D = random.randint(1, 20)
    return A, B, C, D

def traffic_light_simulation():
    global traffic_data
    while True:
        # Generate random values for traffic times
        A, B, C, D = generate_random_values()
        traffic_data["A"]["time"] = A
        traffic_data["B"]["time"] = B
        traffic_data["C"]["time"] = C
        traffic_data["D"]["time"] = D

        # Sort values in descending order
        sorted_values = sorted([A, B, C, D], reverse=True)
        timings = {sorted_values[0]: 60, sorted_values[1]: 50, sorted_values[2]: 40, sorted_values[3]: 30}

        # Simulate the traffic light countdown for each signal
        for value in sorted_values:
            # Set all lights to red before turning the current signal green
            traffic_data["A"]["light"] = "red"
            traffic_data["B"]["light"] = "red"
            traffic_data["C"]["light"] = "red"
            traffic_data["D"]["light"] = "red"
            
            if value == A:
                traffic_data["A"]["light"] = "green"
                traffic_data["current"] = "A"
            elif value == B:
                traffic_data["B"]["light"] = "green"
                traffic_data["current"] = "B"
            elif value == C:
                traffic_data["C"]["light"] = "green"
                traffic_data["current"] = "C"
            else:
                traffic_data["D"]["light"] = "green"
                traffic_data["current"] = "D"

            # Transition time before turning green
            traffic_data["remaining_time"] = 5  # Transition time to green
            for remaining_time in range(5, 0, -1):
                traffic_data["remaining_time"] = remaining_time
                display_number_on_kit(remaining_time)  # Show transition countdown
                time.sleep(1)

            # Main green light countdown with yellow transition when <= 5 secs
            traffic_data["remaining_time"] = timings[value]
            for remaining_time in range(timings[value], 0, -1):
                if remaining_time <= 5:  # When remaining time is 5 or less, show yellow light
                    if value == A:
                        traffic_data["A"]["light"] = "yellow"
                    elif value == B:
                        traffic_data["B"]["light"] = "yellow"
                    elif value == C:
                        traffic_data["C"]["light"] = "yellow"
                    else:
                        traffic_data["D"]["light"] = "yellow"
                
                # Continue countdown
                traffic_data["remaining_time"] = remaining_time
                display_number_on_kit(remaining_time)  # Show countdown
                time.sleep(1)

            # Reset light to red after green countdown
            if value == A:
                traffic_data["A"]["light"] = "red"
            elif value == B:
                traffic_data["B"]["light"] = "red"
            elif value == C:
                traffic_data["C"]["light"] = "red"
            else:
                traffic_data["D"]["light"] = "red"

            traffic_data["remaining_time"] = 0


@app.route('/')
def index():
    return render_template('NewTafficweb1234.html')

@app.route('/data')
def data():
    return jsonify(traffic_data)

# Setup GPIO and start the simulation in a separate thread
setup_display()
simulation_thread = threading.Thread(target=traffic_light_simulation, daemon=True)
simulation_thread.start()

if __name__ == '__main__':
    try:
        app.run(host='0.0.0.0', port=5000)
    except KeyboardInterrupt:
        GPIO.cleanup()
