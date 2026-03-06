# ==============================
# main.py
# Airspace Safety Monitoring System (LIVE RADAR VERSION)
# ==============================

import signal
import sys
import random
import os
import platform
import pygame
import matplotlib.pyplot as plt

from ultralytics import YOLO
import cv2

from src.tracker import TargetTracker
from src.detection import detect_object
from src.frame_generator import FrameGenerator
from src.trajectory import restricted_airspace_violation
from src.risk_assessment import assess_risk
from src.alert_system import issue_alert
from src.advanced_radar import AdvancedRadar


# ------------------------------
# YOLO MODEL (optional)
# ------------------------------
USE_YOLO = False   # change to True if using camera

if USE_YOLO:
    yolo_model = YOLO("yolov8n.pt")


# ------------------------------
# GLOBAL CONFIGURATION
# ------------------------------
restricted_zone_center = (0, 0, 150)
radius = 150

HEADLESS = (
    os.environ.get("CODESPACES") == "true"
    or (
        platform.system() == "Linux"
        and os.environ.get("DISPLAY") is None
    )
)


# ------------------------------
# SYSTEM MODE
# ------------------------------
SYSTEM_MODE = "military"
# options:
# "military"
# "civilian"


# ------------------------------
# TARGET TRACKING SYSTEM
# ------------------------------
target_counter = 1000
tracked_targets = {}

def generate_target_id():
    global target_counter
    target_counter += 1
    return f"TGT-{target_counter}"


# ------------------------------
# SIMULATED MOTION
# ------------------------------
def generate_simulated_motion():

    current_position = (
        random.randint(-120, 120),
        random.randint(-120, 120),
        random.randint(50, 200)
    )

    next_position = (
        current_position[0] + random.randint(-20, 20),
        current_position[1] + random.randint(-20, 20),
        current_position[2]
    )

    speed = random.randint(20, 200)
    altitude_change = random.randint(5, 80)
    speed_change = random.randint(5, 100)

    return current_position, next_position, speed, altitude_change, speed_change


# ------------------------------
# YOLO DETECTION
# ------------------------------
def detect_with_yolo():

    cap = cv2.VideoCapture(0)

    ret, frame = cap.read()

    if not ret:
        return "unknown"

    results = yolo_model(frame)

    for r in results:
        for box in r.boxes:

            cls = int(box.cls)
            label = yolo_model.names[cls]

            if label in ["airplane", "bird", "drone"]:
                return label

    return "unknown"


# ------------------------------
# STOP HANDLER
# ------------------------------
def signal_handler(sig, frame):
    print("\nStopping Airspace Monitoring System...")
    pygame.quit()
    plt.close('all')
    sys.exit(0)


# ------------------------------
# MAIN FUNCTION
# ------------------------------
def main():

    signal.signal(signal.SIGINT, signal_handler)

    # ==========================
    # HEADLESS MODE
    # ==========================
    if HEADLESS:

        print("Headless Mode → Generating 2D Map Frames")

        generator = FrameGenerator(radius=radius)

        for frame in range(300):

            current_position, next_position, speed, altitude_change, speed_change = generate_simulated_motion()

            generator.generate(
                current_position,
                next_position,
                frame
            )

        print("2D Frames Generated Successfully!")
        return


    # ==========================
    # GUI MODE
    # ==========================
    print("GUI Mode → Advanced Radar Activated")

    radar = AdvancedRadar()
    tracker = TargetTracker()
    clock = pygame.time.Clock()

    threat_timer = 0


    while True:

        clock.tick(60)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        # ----------------------------------
        # Slow down detection to 1 second
        # ----------------------------------
        threat_timer += 1

        if threat_timer >= 60:

            threat_timer = 0

            print("\n==============================")
            print(" Airspace Safety Monitoring ")
            print("==============================\n")


            # ------------------------------
            # DETECTION
            # ------------------------------
            if USE_YOLO:
                detected_object = detect_with_yolo()
                threat_type = "THREAT"
            else:
                detected_object, threat_type = detect_object()


            # ------------------------------
            # TARGET ID
            # ------------------------------
            target_id = generate_target_id()

            print("Detected Object:", detected_object)
            print("Target ID:", target_id)


            # ------------------------------
            # CIVILIAN MODE
            # ------------------------------
            if SYSTEM_MODE == "civilian":

                print("Civilian Airspace Monitoring")

                if random.random() < 0.2:
                    print("⚠ Collision Warning Between Aircraft")


            # ------------------------------
            # NON THREAT
            # ------------------------------
            if threat_type == "NON-THREAT":

                print("Status: Natural Activity")
                radar.update(None)


            # ------------------------------
            # THREAT ANALYSIS
            # ------------------------------
            else:

                current_position, next_position, speed, altitude_change, speed_change = generate_simulated_motion()

                print("Predicted Path:", next_position)

                violation = restricted_airspace_violation(
                    next_position,
                    restricted_zone_center,
                    radius
                )

                risk = assess_risk(speed, violation, altitude_change, speed_change)

                actions = issue_alert(risk)

                print("Risk Level:", risk)

                for act in actions:
                    print("-", act)

                tracker.update_target(target_id, current_position) 
                targets = tracker.get_targets()  
                for tid in targets:      
                    pos = targets[tid]["position"]      
                    radar.update(pos)


        # Radar animation
        radar.run_frame()


# ------------------------------
# PROGRAM ENTRY
# ------------------------------
if __name__ == "__main__":
    main()
