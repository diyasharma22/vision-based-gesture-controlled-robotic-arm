# Gesture Controlled Robotic Arm 🤖

![Project Banner](images/setup-demo-1.jpeg)

![Python](https://img.shields.io/badge/Python-Computer%20Vision-blue?style=for-the-badge)
![OpenCV](https://img.shields.io/badge/OpenCV-Image%20Processing-green?style=for-the-badge)
![Arduino](https://img.shields.io/badge/Arduino-Nano-teal?style=for-the-badge)
![MediaPipe](https://img.shields.io/badge/MediaPipe-Hand%20Tracking-orange?style=for-the-badge)

---

# 📌 Overview

This project presents a real-time Gesture Controlled Robotic Arm using Computer Vision and Embedded Systems. The robotic arm is controlled through hand gestures detected using a webcam.

The system uses:

- OpenCV
- MediaPipe
- Python
- Arduino Nano
- Servo Motors

to perform real-time robotic arm movements based on detected hand gestures.

Unlike traditional robotic systems that require joysticks or physical controllers, this project enables completely contactless robotic control using computer vision.

---

# 🌐 Live Project Website

🔗 https://diyasharma22.github.io/vision-based-gesture-controlled-robotic-arm/

---

# 🚀 Features

- ✋ Real-time hand gesture recognition
- 🤖 Robotic arm movement using gestures
- 🎯 MediaPipe hand landmark tracking
- 📷 Webcam-based gesture detection
- 🔌 Arduino Nano servo control
- ⚡ Real-time serial communication
- 🦾 Multi-servo robotic arm actuation
- 💻 Computer vision-based interaction
- 🔋 External SMPS power support

---

# 🧠 Technologies Used

## Software

- Python
- OpenCV
- MediaPipe
- PySerial
- Arduino IDE
- HTML
- CSS
- GitHub Pages

## Hardware

- Arduino Nano
- MG996R Servo Motors
- GS2010MG Servo Motor
- 5V 10A SMPS
- Webcam
- Breadboard
- Jumper Wires
- Robotic Arm Kit

---

# ⚙️ System Architecture

![System Architecture](images/system-architecture.png)

The webcam captures hand gestures in real time. OpenCV and MediaPipe process the video feed and identify hand landmarks. Python sends gesture commands to the Arduino Nano through serial communication, and the robotic arm performs the corresponding movement using servo motors.

---

# 🔌 Circuit Connections

![Circuit Connections](images/circuit-connections.png)

This diagram shows the overall hardware connections between the laptop, Arduino Nano, servo motors, SMPS power supply, and breadboard power rails.

---

# 🔧 Wiring Diagram

![Wiring Diagram](images/wiring-diagram.png)

The servo motors are connected to the Arduino Nano PWM pins and powered through an external 5V 10A SMPS supply.

---

# 🔄 System Flowchart

![Flowchart](images/flow-chart.png)

The workflow begins with webcam frame capture, followed by MediaPipe hand landmark detection, gesture recognition, serial communication, and robotic arm movement execution.

---

# ✋ Gesture Mapping

| Gesture | Action |
|---|---|
| ☝️ Index Finger Up | Gripper Open |
| 🤙 Pinky Finger Up | Gripper Close |
| ✌️ Index + Middle Finger Up | Arm Up |
| 🤘 Index + Pinky Up | Arm Down |
| 🤟 Three Fingers Up | Rotate Right |
| 🖐️ Four Fingers Up | Rotate Left |
| ✊ Fist | Reset All Motors |

---

# 🛠️ Hardware Components

| Component | Quantity |
|---|---|
| Arduino Nano | 1 |
| MG996R Servo Motors | 4 |
| GS2010MG Servo Motor | 1 |
| 5V 10A SMPS | 1 |
| Webcam | 1 |
| Breadboard | 1 |
| Jumper Wires | Multiple |

---

# 🔌 Servo Motor Pin Configuration

| Servo Function | Arduino Pin |
|---|---|
| Gripper | D3 |
| Wrist | D5 |
| Elbow | D6 |
| Shoulder | D9 |
| Base Rotation | D10 |

---

# 📂 Repository Structure

```text
vision-based-gesture-controlled-robotic-arm/
│
├── arduino-code/
│   ├── robotic_arm_control.ino
│   └── README.md
│
├── python-code/
│   ├── gesture_control.py
│   ├── requirements.txt
│   └── README.md
│
├── images/
│
├── index.html
├── style.css
└── README.md
```

---

# ▶️ Installation

## Clone Repository

```bash
git clone https://github.com/diyasharma22/vision-based-gesture-controlled-robotic-arm.git

cd vision-based-gesture-controlled-robotic-arm
```

---

# 📦 Install Dependencies

```bash
pip install -r python-code/requirements.txt
```

OR manually install:

```bash
pip install opencv-python mediapipe pyserial numpy
```

---

# 🔧 Upload Arduino Code

1. Open Arduino IDE
2. Connect Arduino Nano
3. Open `robotic_arm_control.ino` from `arduino-code`
4. Select correct COM port
5. Upload code to Arduino Nano

---

# ▶️ Run Python Program

```bash
python python-code/gesture_control.py
```

---

# 📷 Project Demonstration

## Full Robotic Arm Setup

![Setup Demo](images/setup-demo-2.jpeg)

---

## Gesture Recognition Demo

![Gesture Open](images/gesture-open.jpeg)

---

## Gripper Close Gesture

![Gesture Close](images/gesture-close.jpeg)

---

## Real-Time Gesture Detection

![Gesture Recognition](images/gesture-recognition.jpeg)

---

# 🧪 Working Principle

1. Webcam captures hand gestures.
2. OpenCV processes video frames.
3. MediaPipe detects hand landmarks.
4. Finger positions are analyzed.
5. Gestures are identified.
6. Python sends commands via serial communication.
7. Arduino Nano receives commands.
8. Servo motors perform robotic arm movements.

---

# 📈 Results

The system successfully achieved:

- Real-time gesture recognition
- Smooth robotic arm movement
- Stable servo control
- Accurate gesture mapping
- Reliable serial communication
- Contactless robotic interaction

---

# ⚠️ Challenges Faced

- Lighting sensitivity
- Gesture detection noise
- Servo synchronization
- Power management
- Mechanical calibration

---

# 🔮 Future Scope

- AI-based gesture learning
- Wireless robotic control
- Bluetooth/WiFi support
- Mobile application integration
- Object detection
- Autonomous robotic operation
- AR/VR robotic control

---

# 🌍 Applications

- Industrial Automation
- Human-Machine Interaction
- Assistive Robotics
- Smart Manufacturing
- Educational Robotics
- Healthcare Robotics

---

# 👩‍💻 Authors

- Diya Sharma
- Eipshita Basuli
- Richa Datta

---

# 🎓 Academic Project

Developed at  
**VIT Bhopal University**

---

# 📜 License

This project is open-source and available for educational and learning purposes.
