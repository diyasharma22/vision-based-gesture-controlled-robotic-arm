# Python Code

This folder contains the Python program responsible for real-time hand gesture detection and robotic arm control.

## Technologies Used
- Python
- OpenCV
- MediaPipe
- PySerial
- NumPy

## Features
- Real-time webcam capture
- Hand landmark detection using MediaPipe
- Gesture recognition
- Serial communication with Arduino Nano
- Gesture-to-motion mapping for robotic arm control

## Main File
- `gesture_control.py`

## Gesture Mapping

| Gesture | Action |
|---------|--------|
| Index Finger Up | Gripper Open |
| Pinky Finger Up | Gripper Close |
| Two Fingers Up | Arm Up |
| Index + Pinky | Arm Down |
| Three Fingers | Base Rotate Right |
| Four Fingers | Base Rotate Left |
| Fist | Reset All Motors |

## Required Libraries

Install dependencies using:

```bash
pip install -r requirements.txt
