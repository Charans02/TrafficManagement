from flask import Flask, jsonify, render_template
import RPi.GPIO as GPIO
import time
import threading

app = Flask(__name__)

# GPIO Setup
GPIO.setmode(GPIO.BCM)
TRIG = 19  # Trigger pin
ECHO = 26  # Echo pin
StepPins = [13, 4, 6, 5]  # GPIO pins for stepper motor

for pin in StepPins:
    GPIO.setup(pin, GPIO.OUT)
    GPIO.output(pin, False)

GPIO.setup(TRIG, GPIO.OUT)
GPIO.setup(ECHO, GPIO.IN)

# Define stepper motor sequence
Seq = [
    [1, 0, 0, 1],
    [1, 0, 0, 0],
    [1, 1, 0, 0],
    [0, 1, 0, 0],
    [0, 1, 1, 0],
    [0, 0, 1, 0],
    [0, 0, 1, 1],
    [0, 0, 0, 1]
]

StepCount = len(Seq)
StepDir = 1
WaitTime = 0.01
StepCounter = 0
motor_running = False

# Function to get distance
def get_distance():
    GPIO.output(TRIG, False)
    time.sleep(0.2)

    GPIO.output(TRIG, True)
    time.sleep(0.00001)
    GPIO.output(TRIG, False)

    while GPIO.input(ECHO) == 0:
        pulse_start = time.time()

    while GPIO.input(ECHO) == 1:
        pulse_end = time.time()

    pulse_duration = pulse_end - pulse_start
    distance = pulse_duration * 17150
    return round(distance, 2)

# Function to control the stepper motor
def run_stepper():
    global StepCounter
    for pin in range(4):
        xpin = StepPins[pin]
        GPIO.output(xpin, Seq[StepCounter][pin] == 1)
    StepCounter = (StepCounter + StepDir) % StepCount
    time.sleep(WaitTime)

# Motor automation function
def motor_automation():
    global motor_running
    while True:
        distance = get_distance()
        if 10 <= distance <= 25:
            if not motor_running:
                motor_running = True
        else:
            if motor_running:
                motor_running = False
                for pin in StepPins:
                    GPIO.output(pin, False)
        if motor_running:
            run_stepper()

# Start the motor automation in a separate thread
automation_thread = threading.Thread(target=motor_automation)
automation_thread.daemon = True
automation_thread.start()

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/status")
def status():
    distance = get_distance()
    status = "ON" if motor_running else "OFF"
    return jsonify({"distance": distance, "motor_status": status})

if __name__ == "__main__":
    try:
        app.run(host="0.0.0.0", port=5000)
    except KeyboardInterrupt:
        GPIO.cleanup()
