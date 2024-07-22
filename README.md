# Tray Return Robot v2

## Overview 📙

[Our Blog](https://blogs.ntu.edu.sg/ps9888-2021-g15/)
This project involves the development of a tray-return robot designed to operate in food courts. 
The robot autonomously navigates, stops when there are nearby obstacles or people. Patrons may leave their trays on the robot, which will then return trays to the dishwashing station.


![Demostration of our Tray Return Robot](mnt-gif.gif)


## Features 💯

- **Line Tracking**: The robot follows a predefined path using line tracking sensors.
- **Weight Sensors**: Determines whether to proceed to the unloading station or continue its loop based on the weight of trays.
- **Proximity Sensors**: Stops the robot when it detects nearby motion or obstructions to prevent collisions.
- **Linear Actuators**: Lifts the tray rack to pick up trays and puts them down when unloading.

## Hardware Components 🤖

- **Microcontroller**: Raspberry Pi or any suitable microcontroller.
- **Line Tracking Sensors**: For following a predefined path.
- **Weight Sensors (Load Cells)**: To measure the weight of the trays.
- **Proximity Sensors (Ultrasonic Sensors)**: For obstacle detection.
- **Linear Actuators**: To lift and lower the tray rack.
- **Motors and Motor Drivers**: For robot movement.
- **Power Supply**: Batteries or a suitable power source.
- **Chassis**: The physical structure of the robot.

## Software Components 💻

- **Programming Language**: Python
- **Development Environment**: Any Python-compatible IDE
- **Libraries**: RPi.GPIO for GPIO control, other relevant libraries for sensor and actuator integration.

## Installation and Setup 🛠️

### Prerequisites

- A Raspberry Pi or any suitable microcontroller.
- Python installed on your Raspberry Pi.
- Basic knowledge of Python programming and hardware integration.

### Steps 📝

1. **Clone the Repository**:
    ```sh
    git clone https://github.com/e-mny/trayreturn_robot_v2.git
    cd trayreturn_robot_v2
    ```

2. **Install Required Libraries**:
    ```sh
    pip install -r requirements.txt
    ```

3. **Connect the Hardware**:
    - Connect line tracking sensors, weight sensors, proximity sensors, and linear actuators to the Raspberry Pi according to the wiring diagram provided in the repository.

4. **Configure the Software**:
    - Modify the configuration files as needed to match your hardware setup.

5. **Run the Program**:
    - Execute the main script to start the robot:
    ```sh
    cd LineTracking
    python Combine.py
    ```

## Acknowledgments

- Special thanks to all team members and mentors who contributed to this project.

