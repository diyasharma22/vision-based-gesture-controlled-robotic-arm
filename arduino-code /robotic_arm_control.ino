#include <Servo.h>

Servo motor1_gripper;
Servo motor2_wrist;
Servo motor3_elbow;
Servo motor4_shoulder;
Servo motor5_base;

// ═══════════════════════════════════════════════════════════
// ANGLE SETTINGS
// ─────────────────────────────────────────────────────────
// MOTOR 1 — GRIPPER
//   OPEN  =  40°  → 50° below center (was reversed, now fixed)
//   CLOSE = 140°  → 50° above center (was reversed, now fixed)
//   Range = 40° to 140° = 50° each side from 90°
//
// MOTOR 3 — ELBOW
//   CENTER = 90   UP = 110   DOWN = 70
//   NOW HOLDS position until next command received
//
// MOTOR 4 — SHOULDER
//   CENTER = 90   UP = 105   DOWN = 75
//   Range increased — holds position until next command
//
// MOTOR 5 — BASE
//   CENTER = 90   LEFT = 55   RIGHT = 125
//   Fixed — was not moving due to pin issue
// ═══════════════════════════════════════════════════════════

const int GRIPPER_OPEN    =  40;   // FIXED + INCREASED: 50° below center
const int GRIPPER_CLOSE   = 140;   // FIXED + INCREASED: 50° above center

const int ELBOW_CENTER    =  90;
const int ELBOW_UP        = 110;
const int ELBOW_DOWN      =  70;

const int SHOULDER_CENTER =  90;
const int SHOULDER_UP     = 105;
const int SHOULDER_DOWN   =  75;

const int BASE_CENTER     =  90;
const int BASE_LEFT       =  45;   // FIXED: increased range for visible movement
const int BASE_RIGHT      = 135;   // FIXED: increased range for visible movement

const int WRIST_CENTER    =  90;

void moveSlowly(Servo &servo, int targetAngle) {
    int currentAngle = servo.read();
    if (currentAngle < targetAngle) {
        for (int i = currentAngle; i <= targetAngle; i++) {
            servo.write(i);
            delay(12);
        }
    } else {
        for (int i = currentAngle; i >= targetAngle; i--) {
            servo.write(i);
            delay(12);
        }
    }
    // Motor holds at targetAngle until next command
}

void setup() {
    Serial.begin(9600);

    motor1_gripper.attach(3);
    motor2_wrist.attach(5);
    motor3_elbow.attach(6);
    motor4_shoulder.attach(9);
    motor5_base.attach(10);

    // Safe starting positions
    motor1_gripper.write(GRIPPER_CLOSE);   // Start closed
    motor2_wrist.write(WRIST_CENTER);
    motor3_elbow.write(ELBOW_CENTER);
    motor4_shoulder.write(SHOULDER_CENTER);
    motor5_base.write(BASE_CENTER);

    delay(2000);   // Give all motors time to reach start position

    Serial.println("==============================");
    Serial.println("  Robotic Arm Ready - 5 Motors");
    Serial.println("==============================");
    Serial.println("Motor 1 Gripper : Open=40  Close=140");
    Serial.println("Motor 3 Elbow   : Up=110   Down=70   Center=90");
    Serial.println("Motor 4 Shoulder: Up=105   Down=75   Center=90");
    Serial.println("Motor 5 Base    : Left=45  Right=135 Center=90");
    Serial.println("Waiting for commands...");
}

void loop() {
    if (Serial.available() > 0) {
        char command = Serial.read();

        // ── MOTOR 1 Gripper ─────────────────────────────────────────────────
        if (command == 'O') {
            moveSlowly(motor1_gripper, GRIPPER_OPEN);
            Serial.println("Motor 1: Gripper OPEN (40deg) — holding");
        }
        else if (command == 'C') {
            moveSlowly(motor1_gripper, GRIPPER_CLOSE);
            Serial.println("Motor 1: Gripper CLOSED (140deg) — holding");
        }

        // ── MOTORS 3+4 Elbow + Shoulder — HOLDS position ───────────────────
        else if (command == 'U') {
            moveSlowly(motor3_elbow,    ELBOW_UP);
            moveSlowly(motor4_shoulder, SHOULDER_UP);
            // NO delay, NO auto-return — holds here until next command
            Serial.println("Motors 3+4: Arm UP — holding at Elbow=110 Shoulder=105");
        }
        else if (command == 'D') {
            moveSlowly(motor3_elbow,    ELBOW_DOWN);
            moveSlowly(motor4_shoulder, SHOULDER_DOWN);
            // NO delay, NO auto-return — holds here until next command
            Serial.println("Motors 3+4: Arm DOWN — holding at Elbow=70 Shoulder=75");
        }

        // ── MOTOR 5 Base — FIXED — moves 15deg per gesture step ────────────
        else if (command == 'R') {
            int current = motor5_base.read();
            int next    = min(current + 15, BASE_RIGHT);  // 15deg step right
            moveSlowly(motor5_base, next);
            Serial.print("Motor 5: Rotate RIGHT — now at ");
            Serial.print(next);
            Serial.println("deg — holding");
        }
        else if (command == 'L') {
            int current = motor5_base.read();
            int next    = max(current - 15, BASE_LEFT);   // 15deg step left
            moveSlowly(motor5_base, next);
            Serial.print("Motor 5: Rotate LEFT — now at ");
            Serial.print(next);
            Serial.println("deg — holding");
        }

        // ── RESET ALL ────────────────────────────────────────────────────────
        else if (command == 'H') {
            moveSlowly(motor1_gripper,  GRIPPER_CLOSE);
            moveSlowly(motor2_wrist,    WRIST_CENTER);
            moveSlowly(motor3_elbow,    ELBOW_CENTER);
            moveSlowly(motor4_shoulder, SHOULDER_CENTER);
            moveSlowly(motor5_base,     BASE_CENTER);
            Serial.println("ALL MOTORS RESET TO DEFAULT");
        }
    }
}
