# Arduino Code

This folder contains the Arduino Nano program used to control the robotic arm servo motors.

## Features
- Controls 5 servo motors
- Receives commands from Python through serial communication
- Supports:
  - Gripper open/close
  - Base rotation
  - Shoulder movement
  - Elbow movement
  - System reset
- Smooth servo movement using gradual angle transitions

## Main File
- `robotic_arm_control.ino`

## Hardware Used
- Arduino Nano
- MG996R Servo Motors
- GS2010MG Servo Motor
- 5V 10A SMPS
- Breadboard & Jumper Wires

## Serial Commands

| Command | Action |
|--------|--------|
| O | Gripper Open |
| C | Gripper Close |
| U | Arm Up |
| D | Arm Down |
| R | Rotate Base Right |
| L | Rotate Base Left |
| H | Reset All Motors |

## Upload Instructions
1. Open Arduino IDE
2. Connect Arduino Nano
3. Open `robotic_arm_control.ino`
4. Select correct COM Port
5. Upload code to Arduino Nano
