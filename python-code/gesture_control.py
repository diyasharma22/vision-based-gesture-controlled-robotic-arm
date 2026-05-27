import cv2
import mediapipe as mp
import os
import urllib.request
import serial
import time

# ── CHANGE THIS TO YOUR ARDUINO PORT ───────────────────────────────────────
ARDUINO_PORT = "COM5"
BAUD_RATE    = 9600
# ───────────────────────────────────────────────────────────────────────────

try:
    arduino = serial.Serial(ARDUINO_PORT, BAUD_RATE, timeout=1)
    time.sleep(2)
    print(f"Connected to Arduino on {ARDUINO_PORT}")
except Exception as e:
    print(f"Could not connect to Arduino: {e}")
    exit()

MODEL_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "hand_landmarker.task")

if not os.path.exists(MODEL_PATH):
    print("Downloading hand landmark model... please wait")
    try:
        urllib.request.urlretrieve(
            "https://storage.googleapis.com/mediapipe-models/hand_landmarker/hand_landmarker/float16/1/hand_landmarker.task",
            MODEL_PATH
        )
        print("Model downloaded!")
    except Exception as e:
        print(f"Download failed: {e}")
        exit()

BaseOptions           = mp.tasks.BaseOptions
HandLandmarker        = mp.tasks.vision.HandLandmarker
HandLandmarkerOptions = mp.tasks.vision.HandLandmarkerOptions
VisionRunningMode     = mp.tasks.vision.RunningMode

options = HandLandmarkerOptions(
    base_options=BaseOptions(model_asset_path=MODEL_PATH),
    running_mode=VisionRunningMode.VIDEO,
    num_hands=1,
    min_hand_detection_confidence=0.7,
    min_hand_presence_confidence=0.7,
    min_tracking_confidence=0.7
)

cap = cv2.VideoCapture(0)
if not cap.isOpened():
    print("Error: Could not open webcam.")
    arduino.close()
    exit()

cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)

HAND_CONNECTIONS = [
    (0,1),(1,2),(2,3),(3,4),
    (0,5),(5,6),(6,7),(7,8),
    (0,9),(9,10),(10,11),(11,12),
    (0,13),(13,14),(14,15),(15,16),
    (0,17),(17,18),(18,19),(19,20),
    (5,9),(9,13),(13,17)
]

FINGERTIPS = [4,  8,  12, 16, 20]
KNUCKLES   = [3,  6,  10, 14, 18]
WRIST      = 0

def get_finger_states(landmarks, h):
    states = []
    for tip, knuckle in zip(FINGERTIPS, KNUCKLES):
        tip_y     = landmarks[tip].y * h
        knuckle_y = landmarks[knuckle].y * h
        states.append(tip_y < knuckle_y)
    return states

def detect_gesture(landmarks, w, h):
    s = get_finger_states(landmarks, h)
    thumb  = s[0]
    index  = s[1]
    middle = s[2]
    ring   = s[3]
    pinky  = s[4]

    if not index and not middle and not ring and not pinky:
        return "RESET"

    if index and not middle and not ring and not pinky:
        return "GRIPPER_OPEN"

    if pinky and not index and not middle and not ring:
        return "GRIPPER_CLOSE"

    if index and middle and not ring and not pinky:
        return "ARM_UP"

    if index and pinky and not middle and not ring:
        return "ARM_DOWN"

    if index and middle and ring and not pinky:
        return "ROTATE_RIGHT"

    if index and middle and ring and pinky:
        return "ROTATE_LEFT"

    return "NONE"

GESTURE_COMMANDS = {
    "GRIPPER_OPEN"  : b'O',
    "GRIPPER_CLOSE" : b'C',
    "ARM_UP"        : b'U',
    "ARM_DOWN"      : b'D',
    "ROTATE_RIGHT"  : b'R',
    "ROTATE_LEFT"   : b'L',
    "RESET"         : b'H',
}

GESTURE_LABELS = {
    "GRIPPER_OPEN"  : ("INDEX UP          ->  Gripper OPEN       [Motor 1]",   (0, 255, 0)),
    "GRIPPER_CLOSE" : ("PINKY UP          ->  Gripper CLOSE      [Motor 1]",   (0, 0, 255)),
    "ARM_UP"        : ("INDEX+MIDDLE UP   ->  Arm UP             [Motors 3+4]",(255, 200, 0)),
    "ARM_DOWN"      : ("INDEX+PINKY UP    ->  Arm DOWN           [Motors 3+4]",(0, 200, 255)),
    "ROTATE_RIGHT"  : ("3 FINGERS UP      ->  Rotate RIGHT       [Motor 5]",   (200, 0, 255)),
    "ROTATE_LEFT"   : ("4 FINGERS UP      ->  Rotate LEFT        [Motor 5]",   (255, 100, 0)),
    "RESET"         : ("FIST              ->  RESET ALL MOTORS",                (200, 200, 200)),
    "NONE"          : ("Hand detected     ->  Hold a gesture",                  (150, 150, 150)),
}

print("=" * 60)
print("   ROBOTIC ARM - FINAL GESTURE CONTROL - 5 MOTORS")
print("=" * 60)
print("  Index only UP          = Gripper OPEN    (Motor 1)")
print("  Pinky only UP          = Gripper CLOSE   (Motor 1)")
print("  Index + Middle UP      = Arm UP          (Motors 3+4)")
print("  Index + Pinky UP       = Arm DOWN        (Motors 3+4)")
print("  3 Fingers UP           = Rotate RIGHT    (Motor 5)")
print("  4 Fingers UP           = Rotate LEFT     (Motor 5)")
print("  FIST                   = Reset ALL motors to default")
print("  Press Q to quit")
print("=" * 60)

last_gesture  = None
gesture_timer = 0
GESTURE_DELAY = 25

try:
    with HandLandmarker.create_from_options(options) as landmarker:
        timestamp = 0

        while True:
            success, img = cap.read()
            if not success:
                break

            img = cv2.flip(img, 1)
            h, w, c = img.shape

            mp_image = mp.Image(
                image_format=mp.ImageFormat.SRGB,
                data=cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
            )
            timestamp += 1
            result = landmarker.detect_for_video(mp_image, timestamp)

            status_text  = "No Hand Detected - Show your hand"
            status_color = (0, 165, 255)

            if result.hand_landmarks:
                for hand_landmarks in result.hand_landmarks:

                    for start, end in HAND_CONNECTIONS:
                        x1 = int(hand_landmarks[start].x * w)
                        y1 = int(hand_landmarks[start].y * h)
                        x2 = int(hand_landmarks[end].x * w)
                        y2 = int(hand_landmarks[end].y * h)
                        cv2.line(img, (x1, y1), (x2, y2), (255, 255, 255), 2)

                    for id, lm in enumerate(hand_landmarks):
                        cx = int(lm.x * w)
                        cy = int(lm.y * h)
                        if id in [4, 8, 12, 16, 20]:
                            cv2.circle(img, (cx, cy), 10, (0, 255, 0), cv2.FILLED)
                        else:
                            cv2.circle(img, (cx, cy), 5,  (0, 0, 255), cv2.FILLED)

                    gesture = detect_gesture(hand_landmarks, w, h)

                    if gesture != "NONE" and gesture in GESTURE_COMMANDS:
                        if gesture != last_gesture:
                            arduino.write(GESTURE_COMMANDS[gesture])
                            gesture_timer = 0
                            print(f"Sending: {gesture}")
                            last_gesture = gesture
                        else:
                            gesture_timer += 1
                            if gesture in ["ROTATE_RIGHT", "ROTATE_LEFT",
                                           "ARM_UP", "ARM_DOWN"] \
                                           and gesture_timer >= GESTURE_DELAY:
                                arduino.write(GESTURE_COMMANDS[gesture])
                                gesture_timer = 0

                    if gesture in GESTURE_LABELS:
                        status_text, status_color = GESTURE_LABELS[gesture]

            else:
                last_gesture  = None
                gesture_timer = 0

            cv2.rectangle(img, (0, 0), (w, 60), (0, 0, 0), -1)
            cv2.putText(img, status_text, (15, 42),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.8, status_color, 2)

            cv2.rectangle(img, (0, h - 120), (w, h), (0, 0, 0), -1)
            guide = [
                "Index=Open  Pinky=Close  [Motor1]",
                "Index+Middle=ArmUp  Index+Pinky=ArmDown  [Motors3+4]",
                "3Fingers=RotateRight  4Fingers=RotateLeft  Fist=Reset  Q=Quit"
            ]
            for i, line in enumerate(guide):
                cv2.putText(img, line, (10, h - 90 + (i * 30)),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.5, (180, 180, 180), 1)

            cv2.imshow("Robotic Arm - Final Gesture Control", img)

            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

finally:
    arduino.close()
    cap.release()
    cv2.destroyAllWindows()
    cv2.waitKey(1)
    cv2.waitKey(1)
    cv2.waitKey(1)
    print("Camera and Arduino released safely.")
