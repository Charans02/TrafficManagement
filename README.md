# Smart City Traffic Management System 🚦

This project simulates a **Smart City Traffic Management System** using a **Raspberry Pi**, **Flask Web Framework**, and **hardware components** like a **7-segment display**, **ultrasonic sensor**, **stepper motor**, and **LEDs** to emulate traffic lights. It dynamically allocates traffic light timings based on random data or sensor inputs and displays the state of the system on a live **web dashboard**.

---

## 🧰 Components and Tools Required

### 🔧 Hardware
- Raspberry Pi (any recent model with GPIO support)
- 7-Segment Display with 74HC595 Shift Register
- LEDs for traffic light simulation (Red, Yellow, Green)
- Power Supply
- Ultrasonic Sensor (e.g., HC-SR04)
- Stepper Motor (e.g., 28BYJ-48 with ULN2003 driver)
- Breadboard and Jumper Wires
- Optional: Arduino board for extended functionality

### 💻 Software
- Raspberry Pi OS
- Python 3.10 or 3.11
- Visual Studio Code (VS Code) on laptop for development
- Flask (Web framework)
- Other required Python libraries (see below)

---

## 📦 Python Libraries Used

- `Flask` – for creating and serving the web application
- `RPi.GPIO` – to interact with GPIO pins
- `threading` – to handle parallel execution of simulation and web app
- `time` – for countdowns and delays
- `random` – to generate random traffic scenarios

Install these using pip:
```bash
pip install flask
```
---

## ⚙️ Setup and Configuration

1. Install Raspberry Pi OS
2. Update and Install Dependencies
```bash
sudo apt update && sudo apt upgrade
sudo apt install python3-pip
pip3 install flask
```
3.Connect the Hardware
4.Run the Flask Application
```bash
python3 smart_city.py
```
5.Access the Web Interface Open a browser and visit:
```cpp
http://<Raspberry_Pi_IP>:5000
```


## 🤝 Contribution
Feel free to fork the repository and submit pull requests to enhance the simulation – such as integrating real-time traffic APIs, data analytics, or AI-based optimization!
